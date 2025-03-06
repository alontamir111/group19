// register.js - JavaScript for registration form validation
document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const msgDiv = document.querySelector('.msg');

    // Form inputs
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const cityInput = document.getElementById('city');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const ageInput = document.getElementById('age');
    // שינוי מאלמנט select לקבוצת radio buttons
    const genderRadios = document.querySelectorAll('input[name="gender"]');
    const termsCheckbox = document.getElementById('terms');

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

    // Add form submit handler
    if (registrationForm) {
        registrationForm.addEventListener('submit', (e) => {
            if (!validateForm()) {
                e.preventDefault();
            }
        });

        // Add real-time validation to inputs
        firstNameInput.addEventListener('input', () => validateName(firstNameInput, 'First name'));
        lastNameInput.addEventListener('input', () => validateName(lastNameInput, 'Last name'));
        emailInput.addEventListener('input', validateEmail);
        phoneInput.addEventListener('input', validatePhone);
        cityInput.addEventListener('input', validateCity);
        passwordInput.addEventListener('input', validatePassword);
        confirmPasswordInput.addEventListener('input', validateConfirmPassword);
        ageInput.addEventListener('input', validateAge);

        // שינוי מאזנה לselect לאזנה ל-radio buttons
        genderRadios.forEach(radio => {
            radio.addEventListener('change', validateGender);
        });

        termsCheckbox.addEventListener('change', validateTerms);
    }

    function validateForm() {
        let isValid = true;

        // Validate all fields
        if (!validateName(firstNameInput, 'First name')) isValid = false;
        if (!validateName(lastNameInput, 'Last name')) isValid = false;
        if (!validateEmail()) isValid = false;
        if (!validatePhone()) isValid = false;
        if (!validateCity()) isValid = false;
        if (!validatePassword()) isValid = false;
        if (!validateConfirmPassword()) isValid = false;
        if (!validateAge()) isValid = false;
        if (!validateGender()) isValid = false;
        if (!validateTerms()) isValid = false;

        return isValid;
    }

    function validateName(input, fieldName) {
        const name = input.value.trim();
        const errorElement = input.nextElementSibling;

        if (!name) {
            showError(input, errorElement, `${fieldName} is required`);
            return false;
        }

        if (name.length < 3) {
            showError(input, errorElement, `${fieldName} must be at least 3 characters`);
            return false;
        }

        clearError(input, errorElement);
        return true;
    }

    function validateEmail() {
        const email = emailInput.value.trim();
        const errorElement = emailInput.nextElementSibling;

        if (!email) {
            showError(emailInput, errorElement, 'Email is required');
            return false;
        }

        if (!isValidEmail(email)) {
            showError(emailInput, errorElement, 'Please enter a valid email address');
            return false;
        }

        clearError(emailInput, errorElement);
        return true;
    }

    function validatePhone() {
        const phone = phoneInput.value.trim();
        const errorElement = phoneInput.nextElementSibling;

        if (!phone) {
            showError(phoneInput, errorElement, 'Phone number is required');
            return false;
        }

        // Israeli phone format validation (05X-XXXXXXX or 05XXXXXXXX)
        const phoneRegex = /^05\d(-?\d{7})$/;
        if (!phoneRegex.test(phone.replace('-', ''))) {
            showError(phoneInput, errorElement, 'Please enter a valid Israeli phone number');
            return false;
        }

        clearError(phoneInput, errorElement);
        return true;
    }

    function validateCity() {
        const city = cityInput.value.trim();
        const errorElement = cityInput.nextElementSibling;

        if (!city) {
            showError(cityInput, errorElement, 'City is required');
            return false;
        }

        clearError(cityInput, errorElement);
        return true;
    }

    function validatePassword() {
        const password = passwordInput.value;
        const errorElement = passwordInput.nextElementSibling;

        if (!password) {
            showError(passwordInput, errorElement, 'Password is required');
            return false;
        }

        if (password.length < 6) {
            showError(passwordInput, errorElement, 'Password must be at least 6 characters');
            return false;
        }

        clearError(passwordInput, errorElement);
        return true;
    }

    function validateConfirmPassword() {
        const confirmPassword = confirmPasswordInput.value;
        const password = passwordInput.value;
        const errorElement = confirmPasswordInput.nextElementSibling;

        if (!confirmPassword) {
            showError(confirmPasswordInput, errorElement, 'Please confirm your password');
            return false;
        }

        if (confirmPassword !== password) {
            showError(confirmPasswordInput, errorElement, 'Passwords do not match');
            return false;
        }

        clearError(confirmPasswordInput, errorElement);
        return true;
    }

    function validateAge() {
        const age = ageInput.value;
        const errorElement = ageInput.nextElementSibling;

        if (!age) {
            showError(ageInput, errorElement, 'Age is required');
            return false;
        }

        const ageNum = parseInt(age);
        if (isNaN(ageNum) || ageNum < 16 || ageNum > 120) {
            showError(ageInput, errorElement, 'Age must be between 16 and 120');
            return false;
        }

        clearError(ageInput, errorElement);
        return true;
    }

    function validateGender() {
        // שינוי מבדיקת select לבדיקת radio buttons
        const selectedGender = document.querySelector('input[name="gender"]:checked');
        // אנחנו צריכים למצוא את אלמנט השגיאה - הוא נמצא אחרי קבוצת הרדיו באטנס
        const errorElement = document.querySelector('.gender-selection .error-message');

        if (!selectedGender) {
            showError(document.querySelector('.radio-group'), errorElement, 'Please select a gender');
            return false;
        }

        clearError(document.querySelector('.radio-group'), errorElement);
        return true;
    }

    function validateTerms() {
        const terms = termsCheckbox.checked;
        const errorElement = termsCheckbox.nextElementSibling.nextElementSibling;

        if (!terms) {
            showError(termsCheckbox, errorElement, 'You must accept the Terms and Conditions');
            return false;
        }

        clearError(termsCheckbox, errorElement);
        return true;
    }

    function isValidEmail(email) {
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

    // Format phone number as user types
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, ''); // Remove non-digits

        if (value.length > 3) {
            value = value.substring(0, 3) + '-' + value.substring(3, 10);
        }

        e.target.value = value;
    });

    // הוספת פונקציונליות למודל תנאי השימוש
    const termsLink = document.querySelector('.terms-link');
    const termsModal = document.getElementById('termsModal');
    const closeButton = document.querySelector('.close');
    const acceptTermsButton = document.getElementById('acceptTerms');

    if (termsLink) {
        termsLink.addEventListener('click', function(e) {
            e.preventDefault();
            termsModal.style.display = 'block';
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', function() {
            termsModal.style.display = 'none';
        });
    }

    if (acceptTermsButton) {
        acceptTermsButton.addEventListener('click', function() {
            termsCheckbox.checked = true;
            validateTerms();
            termsModal.style.display = 'none';
        });
    }

    // סגירת המודל בלחיצה מחוץ לתוכן
    window.addEventListener('click', function(e) {
        if (e.target === termsModal) {
            termsModal.style.display = 'none';
        }
    });
});