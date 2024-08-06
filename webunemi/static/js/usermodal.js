document.addEventListener('DOMContentLoaded', function() {
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userMenu = document.getElementById('user-menu');

    // Toggle menu visibility on button click
    userMenuBtn.addEventListener('click', function() {
        userMenu.classList.toggle('hidden');
    });

    // Close menu when clicking outside of it
    document.addEventListener('click', function(event) {
        if (!userMenuBtn.contains(event.target)) {
            userMenu.classList.add('hidden');
        }
    });
});