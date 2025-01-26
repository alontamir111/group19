class ContactManager {
    constructor() {
        this.contactForm = document.getElementById('contactForm');
        this.nameInput = document.getElementById('name');
        this.emailInput = document.getElementById('email');
        this.messageInput = document.getElementById('message');
        this.subjectInput = document.getElementById('subject');
        this.initialize();
    }

    initialize() {
        this.setupFormValidation();
    }

    setupFormValidation() {
        if (!this.contactForm) return;

        // Form submission
        this.contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (this.validateForm()) {
                this.handleSubmit();
            }
        });

        // Real-time validation
        const inputs = this.contactForm.querySelectorAll('input[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => {
                const errorDiv = input.nextElementSibling;
                errorDiv.style.display = 'none';
                input.classList.remove('error');
            });
        });
    }

    validateField(field) {
        const errorDiv = field.nextElementSibling;
        let isValid = true;
        let errorMessage = '';

        switch(field.id) {
            case 'name':
                if (field.value.trim().length < 2) {
                    isValid = false;
                    errorMessage = 'Name must be at least 2 characters';
                } else if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
                    isValid = false;
                    errorMessage = 'Name should contain only letters and spaces';
                }
                break;

            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(field.value.trim())) {
                    isValid = false;
                    errorMessage = 'Please enter a valid email address';
                }
                break;

            case 'message':
                if (field.value.trim().length < 10) {
                    isValid = false;
                    errorMessage = 'Message must be at least 10 characters';
                }
                break;
        }

        this.showFieldError(field, errorDiv, isValid, errorMessage);
        return isValid;
    }

    validateForm() {
        const requiredFields = this.contactForm.querySelectorAll('input[required], textarea[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    showFieldError(field, errorDiv, isValid, message = '') {
        if (!isValid) {
            field.classList.add('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        } else {
            field.classList.remove('error');
            errorDiv.style.display = 'none';
        }
    }

    handleSubmit() {
        const submitBtn = this.contactForm.querySelector('.submit-btn');
        const formData = {
            name: this.nameInput.value.trim(),
            email: this.emailInput.value.trim(),
            subject: this.subjectInput.value,
            message: this.messageInput.value.trim(),
            timestamp: new Date().toISOString()
        };

        submitBtn.classList.add('loading');

        // שמירה ב-localStorage
        let messages = JSON.parse(localStorage.getItem('contactMessages') || '[]');
        messages.push(formData);
        localStorage.setItem('contactMessages', JSON.stringify(messages));

        setTimeout(() => {
            this.showMessage('Message sent successfully!', 'success');
            this.contactForm.reset();
            submitBtn.classList.remove('loading');
        }, 1500);
    }

    showMessage(message, type = 'success') {
        const msgDiv = this.contactForm.querySelector('.msg');
        msgDiv.textContent = message;
        msgDiv.className = `msg ${type}`;
        msgDiv.style.display = 'block';

        setTimeout(() => {
            msgDiv.style.display = 'none';
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ContactManager();
});