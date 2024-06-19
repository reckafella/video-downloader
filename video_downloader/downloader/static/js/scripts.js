document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('expanded');
    });
});
/* 
function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const content = document.querySelector('.content');
    navMenu.classList.toggle('active');
    content.classList.toggle('menu-open');
} */

document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const content = document.querySelector('.content');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        content.classList.toggle('menu-open');
    });
});
