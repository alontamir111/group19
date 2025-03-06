// classes.js - JavaScript file for class types page

document.addEventListener('DOMContentLoaded', function() {
    // Function to check if element is visible on screen
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Function to add class to elements visible on screen
    function handleScroll() {
        const items = document.querySelectorAll('.class-card');

        items.forEach(item => {
            if (isElementInViewport(item)) {
                item.classList.add('visible');
            }
        });
    }

    // Add animations to cards when scrolling
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check on page load

    // Add hover effect to images
    const classImages = document.querySelectorAll('.class-image');
    classImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.querySelector('.class-image-overlay').style.opacity = '1';
        });

        image.addEventListener('mouseleave', function() {
            this.querySelector('.class-image-overlay').style.opacity = '0';
        });
    });

    // Add animations to equipment elements
    const equipmentItems = document.querySelectorAll('.equipment-list li');
    equipmentItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add click event to difficulty badges
    const difficultyBadges = document.querySelectorAll('.difficulty-badge');
    difficultyBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            const difficulty = this.classList[1]; // Take the second class which is the difficulty type

            // Show popup with explanation about difficulty level
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