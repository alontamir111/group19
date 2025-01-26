class User {
    constructor(firstName, lastName, email, phoneNumber, city, password, age, gender, terms, joinDate) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.phoneNumber = phoneNumber;
        this.city = city;
        this.password = password;
        this.age = age;
        this.gender = gender;
        this.terms = terms;
        this.joinDate = joinDate;
    }
}
class RegisterManager {
    constructor() {
        if (!this.checkAuthAndUpdateUI()) return;
        this.setupRegisterForm();
    }

    setupRegisterForm() {
        const form = document.getElementById('registrationForm');
        if (!form) return;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = this.validateForm();
            if (user) {
                this.handleRegistration(user);
            }
        });
    }

    validateForm() {
        const firstName = document.querySelector('input[name="firstName"]').value.trim();
        const lastName = document.querySelector('input[name="lastName"]').value.trim();
        const email = document.querySelector('input[name="email"]').value.trim();
        const phoneNumber = document.querySelector('input[name="phone"]').value.trim();
        const city = document.querySelector('input[name="city"]').value.trim();
        const password = document.querySelector('input[name="password"]').value;
        const confirmPassword = document.querySelector('input[name="confirmPassword"]').value;
        const age = document.querySelector('input[name="age"]').value;
        const terms = document.querySelector('input[name="terms"]').checked;
        const gender = document.querySelector('select[name="gender"]').value;
    
        if (!this.isValidName(firstName)) {
            this.showError("First name must be at least 3 characters");
            return null;
        }

        if (!this.isValidName(lastName)) {
            this.showError("Last name must be at least 3 characters");
            return null;
        }

        if (!this.isValidEmail(email)) {
            this.showError("Invalid email format");
            return null;
        }

        if (!this.isValidPhone(phoneNumber)) {
            this.showError("Invalid phone number");
            return null;
        }

        if (!city) {
            this.showError("City is required");
            return null;
        }

        if (password.length < 6) {
            this.showError("Password must be at least 6 characters");
            return null;
        }

        if (password !== confirmPassword) {
            this.showError("Passwords do not match");
            return null;
        }

        if (age < 16 || age > 120) {
            this.showError("Age must be between 16 and 120");
            return null;
        }
        if (!terms) {
            this.showError("You must accept the Terms and Conditions");
            return null;
        }
    
        if (!gender) {
            this.showError("Please select a gender");
            return null;
        }

        return new User(firstName, lastName, email, phoneNumber, city, password, age, gender, terms, new Date().toISOString());
    }

    handleRegistration(user) {
        const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers')) || [];
        
        if (registeredUsers.some(existingUser => existingUser.email === user.email)) {
            this.showError('Email already exists');
            return;
        }

        registeredUsers.push(user);
        localStorage.setItem('registeredUsers', JSON.stringify(registeredUsers));
        this.showSuccess('Registration successful!');
        
        setTimeout(() => {
            window.location.href = 'Login.html';
        }, 2000);
    }

    isValidName(name) {
        return name.length >= 3;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    isValidPhone(phone) {
        return /^05\d{8}$/.test(phone);
    }

    showError(message) {
        const msgDiv = document.querySelector('.msg');
        msgDiv.textContent = message;
        msgDiv.className = 'msg error';
        setTimeout(() => msgDiv.className = 'msg', 3000);
    }

    showSuccess(message) {
        const msgDiv = document.querySelector('.msg');
        msgDiv.textContent = message;
        msgDiv.className = 'msg success';
    }

    checkAuthAndUpdateUI() {
        if (JSON.parse(localStorage.getItem('signedInUser'))) {
            window.location.href = 'home.html';
            return false;
        }
        return true;
    }
}

document.addEventListener('DOMContentLoaded', () => new RegisterManager());