document.addEventListener('DOMContentLoaded', () => {
    // בדיקה אם המשתמש כבר מחובר
    const signedInUser = JSON.parse(localStorage.getItem('signedInUser'));
    if (signedInUser) {
        window.location.href = 'search-classes.html';
        return;
    }
 
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const msgDiv = document.querySelector('.msg');
 
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
 
    function handleLogin(e) {
        e.preventDefault();
        
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
 
        if (!validateInputs(email, password)) {
            return;
        }
 
        const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers')) || [];
        const user = registeredUsers.find(user => user.email === email && user.password === password);
 
        if (user) {
            localStorage.setItem('signedInUser', JSON.stringify(user));
            window.location.href = "search-classes.html";
        } else {
            showError("Invalid email or password.");
        }
    }
 
    function validateInputs(email, password) {
        if (!email) {
            showError("Please enter your email");
            return false;
        }
 
        if (!isValidEmail(email)) {
            showError("Please enter a valid email address");
            return false;
        }
 
        if (!password) {
            showError("Please enter your password");
            return false;
        }
 
        return true;
    }
 
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
 
    function showError(message) {
        msgDiv.textContent = message;
        msgDiv.className = 'msg error';
        msgDiv.style.display = 'block';
        
        setTimeout(() => {
            msgDiv.style.display = 'none';
            msgDiv.textContent = '';
            msgDiv.className = 'msg';
        }, 3000);
    }
 });