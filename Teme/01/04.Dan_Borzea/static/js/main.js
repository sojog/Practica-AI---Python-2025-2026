// Main JavaScript functionality

// AJAX for favoriting tours
document.addEventListener('DOMContentLoaded', function () {
    // Favorite form handling
    const favoriteForm = document.getElementById('favoriteForm');
    if (favoriteForm) {
        favoriteForm.addEventListener('submit', function (e) {
            e.preventDefault();

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const button = this.querySelector('button');
                        button.innerHTML = data.is_favorite ? '❤️ Favorite' : '🤍 Favorite';
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // Get user's current location for map
    if (navigator.geolocation && document.getElementById('map')) {
        navigator.geolocation.getCurrentPosition(function (position) {
            console.log('User location:', position.coords.latitude, position.coords.longitude);
            // This can be used to show user's position on map
        });
    }
});

// Simple animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
});
