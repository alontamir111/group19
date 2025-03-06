// contact-us.js - קובץ JavaScript לדף צור קשר

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

    // הוספת אנימציות לאלמנטים בדף

    // אנימציית כניסה לפריטי מידע
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('visible');
        }, 200 * index);
    });

    // הוספת אפקט hover לתמונה
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

    // התאמת גובה הטופס לחלק המידע
    function adjustFormHeight() {
        const formSection = document.querySelector('.contact-form-section');
        const infoSection = document.querySelector('.contact-info-section');

        // איפוס הגובה קודם כל
        if (formSection) {
            formSection.style.height = 'auto';
        }

        // התאמת גובה רק אם יש את שני האלמנטים ורוחב המסך מספיק גדול
        if (formSection && infoSection && window.innerWidth > 992) {
            const infoHeight = infoSection.offsetHeight;
            formSection.style.height = `${infoHeight}px`;
        }
    }

    // הפעלת פונקציית התאמת הגובה בטעינה ובשינוי גודל מסך
    adjustFormHeight();
    window.addEventListener('resize', adjustFormHeight);

    // אפקט לשדות הטופס - הדגשת התווית בעת פוקוס
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

    // בדיקת תקינות דואר אלקטרוני
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (this.value && !emailRegex.test(this.value)) {
                this.classList.add('invalid');

                // הוספת הודעת שגיאה אם לא קיימת
                let errorMessage = this.nextElementSibling;
                if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                    errorMessage = document.createElement('span');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = 'Please enter a valid email address';
                    this.parentNode.insertBefore(errorMessage, this.nextSibling);
                }
            } else {
                this.classList.remove('invalid');

                // הסרת הודעת שגיאה אם קיימת
                const errorMessage = this.nextElementSibling;
                if (errorMessage && errorMessage.classList.contains('error-message')) {
                    errorMessage.remove();
                }
            }
        });
    }
});