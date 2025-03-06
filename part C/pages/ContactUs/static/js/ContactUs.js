// contact-us.js - JavaScript file for Contact Us page

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const formStatus = document.getElementById('formStatus');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Display loading state
            formStatus.textContent = 'Sending your message...';
            formStatus.className = 'form-status loading';

            // Get form data
            const formData = new FormData(contactForm);

            // Send the form data using fetch
            fetch('/contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    formStatus.textContent = 'Thank you! Your message has been sent successfully.';
                    formStatus.className = 'form-status success';
                    contactForm.reset();
                } else {
                    formStatus.textContent = data.message || 'There was an error sending your message. Please try again.';
                    formStatus.className = 'form-status error';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                formStatus.textContent = 'There was an error sending your message. Please try again.';
                formStatus.className = 'form-status error';
            });
        });
    }

    // Add animations to page elements

    // Entry animation for info items
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('visible');
        }, 200 * index);
    });

    // Add hover effect to image
    const contactImage = document.querySelector('.contact-image img');
    if (contactImage) {
        contactImage.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.03)';
            this.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.15)';
        });

        contactImage.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    }

    // Adjust form height to match info section
    function adjustFormHeight() {
        const formSection = document.querySelector('.contact-form-section');
        const infoSection = document.querySelector('.contact-info-section');

        // Reset height first
        if (formSection) {
            formSection.style.height = 'auto';
        }

        // Adjust height only if both elements exist and screen is wide enough
        if (formSection && infoSection && window.innerWidth > 992) {
            const infoHeight = infoSection.offsetHeight;
            formSection.style.height = `${infoHeight}px`;
        }
    }

    // Run height adjustment function on load and window resize
    adjustFormHeight();
    window.addEventListener('resize', adjustFormHeight);

    // Effect for form fields - highlight label on focus
    const formInputs = document.querySelectorAll('.form-group input, .form-group textarea, .form-group select');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            const label = this.previousElementSibling;
            if (label && label.tagName === 'LABEL') {
                label.style.color = 'var(--accent-dark)';
                label.style.fontWeight = '600';
            }
        });

        input.addEventListener('blur', function() {
            const label = this.previousElementSibling;
            if (label && label.tagName === 'LABEL') {
                label.style.color = '';
                label.style.fontWeight = '';
            }
        });
    });

    // Email validation
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (this.value && !emailRegex.test(this.value)) {
                this.classList.add('invalid');

                // Add error message if it doesn't exist
                let errorMessage = this.nextElementSibling;
                if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                    errorMessage = document.createElement('span');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = 'Please enter a valid email address';
                    this.parentNode.insertBefore(errorMessage, this.nextSibling);
                }
            } else {
                this.classList.remove('invalid');

                // Remove error message if it exists
                const errorMessage = this.nextElementSibling;
                if (errorMessage && errorMessage.classList.contains('error-message')) {
                    errorMessage.remove();
                }
            }
        });
    }
});