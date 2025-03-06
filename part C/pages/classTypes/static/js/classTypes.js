// classes.js - קובץ JavaScript לדף סוגי שיעורים

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
        const items = document.querySelectorAll('.class-card');

        items.forEach(item => {
            if (isElementInViewport(item)) {
                item.classList.add('visible');
            }
        });
    }

    // הוספת אנימציות לכרטיסיות כאשר גוללים
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // בדיקה ראשונית בטעינת הדף

    // הוספת אפקט hover לתמונות
    const classImages = document.querySelectorAll('.class-image');
    classImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.querySelector('.class-image-overlay').style.opacity = '1';
        });

        image.addEventListener('mouseleave', function() {
            this.querySelector('.class-image-overlay').style.opacity = '0';
        });
    });

    // הוספת אנימציות לאלמנטים של ציוד
    const equipmentItems = document.querySelectorAll('.equipment-list li');
    equipmentItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // הוספת אירוע לחיצה על הדיפיקלטי
    const difficultyBadges = document.querySelectorAll('.difficulty-badge');
    difficultyBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            const difficulty = this.classList[1]; // לקיחת הקלאס השני שהוא סוג הקושי

            // הצגת חלונית עם הסבר על רמת הקושי
            const difficulties = {
                'beginner': 'Perfect for newcomers to yoga. Focus on basic poses and proper alignment.',
                'intermediate': 'For practitioners with some experience. Includes more challenging poses and sequences.',
                'advanced': 'Designed for experienced yogis. Features complex poses and intense sequences.',
                'all-levels': 'Suitable for everyone. Instructors offer modifications for different experience levels.'
            };

            alert(`${this.textContent} Level: ${difficulties[difficulty] || 'A suitable yoga class for your practice.'}`);
        });
    });
});