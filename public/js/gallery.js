function scrollGallery(direction) {
    const gallery = document.getElementById('instagram-gallery');
    const scrollAmount = 340; // Slightly more than post width for smooth scrolling

    if (direction === 'left') {
        gallery.scrollLeft -= scrollAmount;
    } else {
        gallery.scrollLeft += scrollAmount;
    }
}


// Auto-hide arrows when at start/end
function updateArrowVisibility() {
    const gallery = document.getElementById('instagram-gallery');
    const leftArrow = document.querySelector('.absolute.left-2');
    const rightArrow = document.querySelector('.absolute.right-2');

    if (!gallery || !leftArrow || !rightArrow) return;

    const isAtStart = gallery.scrollLeft <= 0;
    const isAtEnd = gallery.scrollLeft >= gallery.scrollWidth - gallery.clientWidth;

    // Update opacity and pointer events
    leftArrow.style.opacity = isAtStart ? '0.3' : '0.7';
    rightArrow.style.opacity = isAtEnd ? '0.3' : '0.7';

    leftArrow.style.pointerEvents = isAtStart ? 'none' : 'auto';
    rightArrow.style.pointerEvents = isAtEnd ? 'none' : 'auto';
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function () {
    const gallery = document.getElementById('instagram-gallery');
    if (gallery) {
        gallery.addEventListener('scroll', updateArrowVisibility);
        updateArrowVisibility(); // Initial check
    }
});

// Touch/swipe support for mobile
let startX = 0;
let scrollLeft = 0;

document.addEventListener('DOMContentLoaded', function () {
    const gallery = document.getElementById('instagram-gallery');
    if (!gallery) return;

    gallery.addEventListener('touchstart', function (e) {
        startX = e.touches[0].pageX;
        scrollLeft = this.scrollLeft;
    });

    gallery.addEventListener('touchmove', function (e) {
        e.preventDefault();
        const x = e.touches[0].pageX;
        const walk = (x - startX) * 2;
        this.scrollLeft = scrollLeft - walk;
    });
});
