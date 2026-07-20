// -----------------------------------------------------------------------------
// Scroll Reveal
// -----------------------------------------------------------------------------

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        entry.target.classList.add("in");
        revealObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.15,
    }
  );

  revealItems.forEach((item) => revealObserver.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("in"));
}


// -----------------------------------------------------------------------------
// Header scroll state
// -----------------------------------------------------------------------------

const header = document.querySelector(".site-header");

if (header) {
  const updateHeaderState = () => {
    header.classList.toggle("nav-scrolled", window.scrollY > 60);
  };

  updateHeaderState();

  window.addEventListener("scroll", updateHeaderState, {
    passive: true,
  });
}


// -----------------------------------------------------------------------------
// Mobile Navigation
// -----------------------------------------------------------------------------

const menuToggle = document.getElementById("menuToggle");
const menuClose = document.getElementById("menuClose");
const mobileNav = document.getElementById("mobileNav");

const openMobileMenu = () => {
  if (!mobileNav || !menuToggle) return;

  mobileNav.classList.add("open");
  mobileNav.setAttribute("aria-hidden", "false");
  menuToggle.setAttribute("aria-expanded", "true");

  document.body.classList.add("menu-open");
};

const closeMobileMenu = () => {
  if (!mobileNav || !menuToggle) return;

  mobileNav.classList.remove("open");
  mobileNav.setAttribute("aria-hidden", "true");
  menuToggle.setAttribute("aria-expanded", "false");

  document.body.classList.remove("menu-open");
};

if (menuToggle) {
  menuToggle.addEventListener("click", openMobileMenu);
}

if (menuClose) {
  menuClose.addEventListener("click", closeMobileMenu);
}


// -----------------------------------------------------------------------------
// Close menu when clicking outside
// -----------------------------------------------------------------------------

document.addEventListener("click", (event) => {
  if (
    mobileNav &&
    menuToggle &&
    mobileNav.classList.contains("open") &&
    !mobileNav.contains(event.target) &&
    !menuToggle.contains(event.target)
  ) {
    closeMobileMenu();
  }
});


// -----------------------------------------------------------------------------
// Close menu with Escape
// -----------------------------------------------------------------------------

document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    mobileNav &&
    mobileNav.classList.contains("open")
  ) {
    closeMobileMenu();
    menuToggle.focus();
  }
});


// -----------------------------------------------------------------------------
// Mobile submenu accordions
// -----------------------------------------------------------------------------

document.querySelectorAll(".mobile-submenu-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const submenu = button.nextElementSibling;

    if (!submenu) return;

    const isOpen = submenu.classList.toggle("open");

    button.setAttribute("aria-expanded", String(isOpen));

    const icon = button.querySelector("span");

    if (icon) {
      icon.textContent = isOpen ? "−" : "+";
    }
  });
});


// -----------------------------------------------------------------------------
// Close mobile menu after navigation
// -----------------------------------------------------------------------------

if (mobileNav) {
  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });
}


// -----------------------------------------------------------------------------
// Testimonial Carousel
// -----------------------------------------------------------------------------

const testimonialCard = document.getElementById("testimonialCard");

if (testimonialCard) {
  const slides = testimonialCard.querySelectorAll(".testimonial-slide");
  const dots = testimonialCard.querySelectorAll(".dot");

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  let current = 0;
  let carouselTimer = null;

  const showTestimonial = (index) => {
    current = Number(index);

    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === current;

      slide.classList.toggle("active", active);
      slide.setAttribute("aria-hidden", String(!active));
    });

    dots.forEach((dot, dotIndex) => {
      const active = dotIndex === current;

      dot.classList.toggle("active", active);
      dot.setAttribute("aria-current", active ? "true" : "false");
    });
  };

  const startCarousel = () => {
    if (
      prefersReducedMotion ||
      slides.length <= 1 ||
      carouselTimer
    ) {
      return;
    }

    carouselTimer = window.setInterval(() => {
      showTestimonial((current + 1) % slides.length);
    }, 6000);
  };

  const stopCarousel = () => {
    if (!carouselTimer) return;

    clearInterval(carouselTimer);
    carouselTimer = null;
  };

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      stopCarousel();
      showTestimonial(index);
      startCarousel();
    });
  });

  testimonialCard.addEventListener("mouseenter", stopCarousel);
  testimonialCard.addEventListener("mouseleave", startCarousel);

  testimonialCard.addEventListener("focusin", stopCarousel);
  testimonialCard.addEventListener("focusout", startCarousel);

  showTestimonial(0);
  startCarousel();
}