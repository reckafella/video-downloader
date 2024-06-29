document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const content = document.querySelector('.content');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('expanded');
        content.classList.toggle('menu-open');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const accountsToggle = document.getElementById('profile-pic');
    const userMenuContent = document.querySelector('.user-menu-content');

    accountsToggle.addEventListener('click', function() {
        userMenuContent.classList.toggle('active');
    });
});
