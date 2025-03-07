// studios.js

document.addEventListener('DOMContentLoaded', function() {
    // Function to check if element is visible in viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        // Check if ANY part of the element is in viewport, not just the entire element
        return (
            (rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
             rect.bottom >= 0) &&
            (rect.left <= (window.innerWidth || document.documentElement.clientWidth) &&
             rect.right >= 0)
        );
    }

    // Function to add class to elements visible in viewport
    function handleScroll() {
        const items = document.querySelectorAll('.studio-card, .facility-item');

        // Automatically show all items on small screens
        if (window.innerWidth <= 992) {
            items.forEach(item => {
                item.classList.add('visible');
            });
            return;
        }

        // Regular viewport check for larger screens
        items.forEach(item => {
            if (isElementInViewport(item)) {
                item.classList.add('visible');
            }
        });
    }

    // Execute function on load, scroll and resize
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleScroll); // Also check when window is resized
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