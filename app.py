from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import cv2
import dlib
import numpy as np
import time
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '123456'

# MongoDB Connection
MONGO_URI = "mongodb+srv://reddycherish76:Cherish1302@dataleak.zr189.mongodb.net/?retryWrites=true&w=majority&appName=dataleak"
client = MongoClient(MONGO_URI)
db = client['smart_lms']

def detect_face(frame):
    detector = dlib.get_frontal_face_detector()
    faces = detector(frame)
    return len(faces) > 0

def detect_attention(audio_level):
    return audio_level > 0.3

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = db.users.find_one({'email': data['email']})
    if user and check_password_hash(user['password'], data['password']):
        session['user'] = user['email']
        return jsonify({'message': 'Login successful', 'user': user['email']})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if db.users.find_one({'email': data['email']}):
        return jsonify({'status': 'exists'})
    
    hashed_password = generate_password_hash(data['password'])
    db.users.insert_one({'email': data['email'], 'password': hashed_password})
    
    return jsonify({'status': 'registered'})
  
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    subjects = db.subjects.find()
    return render_template('dashboard.html', subjects=subjects, user=session['user'])

@app.route('/track', methods=['POST'])
def track():
    cap = cv2.VideoCapture(0)
    attentive_time = 0
    total_time = 0
    
    start_time = time.time()
    while total_time < 60:
        ret, frame = cap.read()
        if not ret:
            break
        if detect_face(frame):
            attentive_time += 1
        total_time = time.time() - start_time
    
    cap.release()
    db.reports.insert_one({'user': session['user'], 'attentive_time': attentive_time, 'total_time': total_time})
    return jsonify({'attentive_time': attentive_time, 'total_time': total_time})

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('home'))
    reports = db.reports.find()
    subjects = db.subjects.find()
    return render_template('admin.html', reports=reports, subjects=subjects)

@app.route('/add_subject', methods=['POST'])
def add_subject():
    if 'user' not in session or session['user'] != 'admin':
        return jsonify({'status': 'unauthorized'})
    data = request.json
    db.subjects.insert_one({'name': data['name'], 'chapters': data['chapters']})
    return jsonify({'status': 'added'})

if __name__ == '__main__':
    app.run(debug=True)