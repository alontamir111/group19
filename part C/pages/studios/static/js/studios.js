// studios.js - JavaScript file for the studios page

document.addEventListener('DOMContentLoaded', function() {
    // Function to check if element is visible in viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Function to add class to elements visible in viewport
    function handleScroll() {
        const items = document.querySelectorAll('.studio-card, .facility-item');

        items.forEach(item => {
            if (isElementInViewport(item)) {
                item.classList.add('visible');
            }
        });
    }

    // Execute function on load and scroll
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check on page load

    // Hover effect for studio images
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

    // Additional animation for studio facility items
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

    // Animation for amenities list
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