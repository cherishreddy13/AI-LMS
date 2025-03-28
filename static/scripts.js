document.addEventListener("DOMContentLoaded", function () {
   const loginForm = document.getElementById("loginForm");
   const registerForm = document.getElementById("registerForm");
   const logoutButton = document.getElementById("logoutButton");
   const startButtons = document.querySelectorAll(".startTracking");

   // Handle Login Form Submission
   if (loginForm) {
       loginForm.addEventListener("submit", async (e) => {
           e.preventDefault();
           const email = document.getElementById("email").value;
           const password = document.getElementById("password").value;

           const response = await fetch("/login", {
               method: "POST",
               headers: { "Content-Type": "application/json" },
               body: JSON.stringify({ email, password })
           });

           const data = await response.json();
           if (response.ok) {
               window.location.href = "/dashboard";
           } else {
               document.getElementById("errorMsg").innerText = data.error;
           }
       });
   }

   // Handle Registration Form Submission
   if (registerForm) {
       registerForm.addEventListener("submit", async (e) => {
           e.preventDefault();
           const email = document.getElementById("email").value;
           const password = document.getElementById("password").value;

           const response = await fetch("/register", {
               method: "POST",
               headers: { "Content-Type": "application/json" },
               body: JSON.stringify({ email, password })
           });

           const data = await response.json();
           if (data.status === "registered") {
               alert("Registration successful! Please login.");
               window.location.href = "/";
           } else {
               document.getElementById("registerMsg").innerText = "User already exists!";
           }
       });
   }

   // Logout Function
   if (logoutButton) {
       logoutButton.addEventListener("click", () => {
           fetch("/logout", { method: "POST" }).then(() => {
               window.location.href = "/";
           });
       });
   }

   // Start Tracking Button
   startButtons.forEach(button => {
       button.addEventListener("click", async () => {
           const response = await fetch("/track", { method: "POST" });
           const data = await response.json();
           alert(`Tracking started!\nAttentive Time: ${data.attentive_time} sec`);
       });
   });
});
