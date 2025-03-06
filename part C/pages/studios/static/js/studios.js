// studios.js - קובץ JavaScript לדף הסטודיו

document.addEventListener('DOMContentLoaded', function() {
    // פונקציה לבדיקה אם אלמנט נראה במסך
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // פונקציה להוספת קלאס לאלמנטים שנראים במסך
    function handleScroll() {
        const items = document.querySelectorAll('.studio-card, .facility-item');

        items.forEach(item => {
            if (isElementInViewport(item)) {
                item.classList.add('visible');
            }
        });
    }

    // הפעלת הפונקציה בטעינה ובגלילה
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // בדיקה ראשונית בטעינת הדף

    // אפקט hover לתמונות הסטודיו
    const studioImages = document.querySelectorAll('.studio-image');
    studioImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            const overlay = this.querySelector('.studio-image-overlay');
            if (overlay) {
                overlay.style.opacity = '1';
            }
        });

        image.addEventListener('mouseleave', function() {
            const overlay = this.querySelector('.studio-image-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
            }
        });
    });

    // אנימציה נוספת לפריטי התקני הסטודיו
    const facilityItems = document.querySelectorAll('.facility-item');
    facilityItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const img = this.querySelector('img');
            if (img) {
                img.style.transform = 'scale(1.05)';
            }
        });

        item.addEventListener('mouseleave', function() {
            const img = this.querySelector('img');
            if (img) {
                img.style.transform = 'scale(1)';
            }
        });
    });

    // אנימציה לרשימת האמניטיס
    const amenityItems = document.querySelectorAll('.amenities-list li');
    amenityItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});