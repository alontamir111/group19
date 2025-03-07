// signin.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const msgDiv = document.querySelector('.msg');

    // Flash messages handling (from server)
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        // Auto-hide flash messages after 5 seconds
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.display = 'none';
            });
        }, 5000);
    }

    // Client-side form validation
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            // We'll allow the form to submit to the server but validate basic fields first
            if (!validateForm()) {
                e.preventDefault();
            }
        });

        // Add input event listeners for real-time validation
        emailInput.addEventListener('input', () => validateEmail());
        passwordInput.addEventListener('input', () => validatePassword());
    }

    function validateForm() {
        let isValid = true;

        if (!validateEmail()) isValid = false;
        if (!validatePassword()) isValid = false;

        return isValid;
    }

    function validateEmail() {
        const email = emailInput.value.trim();
        const emailError = emailInput.nextElementSibling;

        if (!email) {
            showError(emailInput, emailError, 'Email is required');
            return false;
        }

        if (!isValidEmail(email)) {
            showError(emailInput, emailError, 'Please enter a valid email address');
            return false;
        }

        clearError(emailInput, emailError);
        return true;
    }

    function validatePassword() {
        const password = passwordInput.value;
        const passwordError = passwordInput.nextElementSibling;

        if (!password) {
            showError(passwordInput, passwordError, 'Password is required');
            return false;
        }

        clearError(passwordInput, passwordError);
        return true;
    }

    function isValidEmail(email) {
        // Basic email validation regex
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showError(input, errorElement, message) {
        input.classList.add('error');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    function clearError(input, errorElement) {
        input.classList.remove('error');
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }

    // Show custom message (if needed)
    function showMessage(message, type = 'error') {
        if (msgDiv) {
            msgDiv.textContent = message;
            msgDiv.className = `msg ${type}`;
            msgDiv.style.display = 'block';

            setTimeout(() => {
                msgDiv.style.display = 'none';
            }, 5000);
        }
    }
});