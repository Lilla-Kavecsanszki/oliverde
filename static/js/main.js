const items = document.querySelectorAll('.reveal');
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });
items.forEach(i => io.observe(i));

// Mobile menu open/close
const menuToggle = document.getElementById('menuToggle');
const menuClose = document.getElementById('menuClose');
const mobileNav = document.getElementById('mobileNav');
if (menuToggle && mobileNav) {
  menuToggle.addEventListener('click', () => mobileNav.classList.add('open'));
}
if (menuClose && mobileNav) {
  menuClose.addEventListener('click', () => mobileNav.classList.remove('open'));
}

// Mobile Portfolio submenu accordion
document.querySelectorAll('.mobile-submenu-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const submenu = btn.nextElementSibling;
    if (submenu) submenu.classList.toggle('open');
  });
});