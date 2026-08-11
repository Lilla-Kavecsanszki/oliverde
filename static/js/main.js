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

const testimonialCard = document.querySelector(".testimonial-card");

if (testimonialCard) {
  const slides = Array.from(
    testimonialCard.querySelectorAll(".testimonial-slide")
  );

  const dots = Array.from(
    testimonialCard.querySelectorAll(".testimonial-dots .dot")
  );

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  let current = 0;
  let carouselTimer = null;

  let pointerStartX = 0;
  let pointerStartY = 0;
  let pointerCurrentX = 0;
  let pointerCurrentY = 0;
  let isPointerDown = false;
  let isHorizontalDrag = false;

  const swipeThreshold = 50;


  // ---------------------------------------------------------------------------
  // Show testimonial
  // ---------------------------------------------------------------------------

  const showTestimonial = (index) => {
    if (!slides.length) {
      return;
    }

    current = (Number(index) + slides.length) % slides.length;

    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === current;

      slide.classList.toggle("active", active);
      slide.setAttribute("aria-hidden", String(!active));
    });

    dots.forEach((dot, dotIndex) => {
      const active = dotIndex === current;

      dot.classList.toggle("active", active);

      if (active) {
        dot.setAttribute("aria-current", "true");
      } else {
        dot.removeAttribute("aria-current");
      }
    });
  };


  // ---------------------------------------------------------------------------
  // Previous / next
  // ---------------------------------------------------------------------------

  const showNextTestimonial = () => {
    showTestimonial(current + 1);
  };


  const showPreviousTestimonial = () => {
    showTestimonial(current - 1);
  };


  // ---------------------------------------------------------------------------
  // Automatic carousel
  // ---------------------------------------------------------------------------

  const startCarousel = () => {
    if (
      prefersReducedMotion ||
      slides.length <= 1 ||
      carouselTimer
    ) {
      return;
    }

    carouselTimer = window.setInterval(() => {
      showNextTestimonial();
    }, 6000);
  };


  const stopCarousel = () => {
    if (!carouselTimer) {
      return;
    }

    window.clearInterval(carouselTimer);
    carouselTimer = null;
  };


  const restartCarousel = () => {
    stopCarousel();
    startCarousel();
  };


  // ---------------------------------------------------------------------------
  // Pagination dots
  // ---------------------------------------------------------------------------

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      showTestimonial(index);
      restartCarousel();
    });
  });


  // ---------------------------------------------------------------------------
  // Mouse + touch swipe / drag
  // ---------------------------------------------------------------------------

  testimonialCard.addEventListener("pointerdown", (event) => {
    /*
      Ignore pointer dragging if the visitor is actually clicking
      one of the carousel controls.
    */
    if (event.target.closest(".testimonial-dots")) {
      return;
    }

    isPointerDown = true;
    isHorizontalDrag = false;

    pointerStartX = event.clientX;
    pointerStartY = event.clientY;

    pointerCurrentX = event.clientX;
    pointerCurrentY = event.clientY;

    testimonialCard.classList.add("is-dragging");

    stopCarousel();

    if (testimonialCard.setPointerCapture) {
      testimonialCard.setPointerCapture(event.pointerId);
    }
  });


  testimonialCard.addEventListener("pointermove", (event) => {
    if (!isPointerDown) {
      return;
    }

    pointerCurrentX = event.clientX;
    pointerCurrentY = event.clientY;

    const deltaX = pointerCurrentX - pointerStartX;
    const deltaY = pointerCurrentY - pointerStartY;

    /*
      Only treat the gesture as a carousel drag when horizontal
      movement is clearly stronger than vertical movement.

      This means normal vertical page scrolling still works on mobile.
    */
    if (
      Math.abs(deltaX) > 8 &&
      Math.abs(deltaX) > Math.abs(deltaY)
    ) {
      isHorizontalDrag = true;
    }
  });


  const finishSwipe = () => {
    if (!isPointerDown) {
      return;
    }

    const deltaX = pointerCurrentX - pointerStartX;

    testimonialCard.classList.remove("is-dragging");

    if (
      isHorizontalDrag &&
      Math.abs(deltaX) >= swipeThreshold
    ) {
      if (deltaX < 0) {
        /*
          Swipe / drag left:
          show the next testimonial.
        */
        showNextTestimonial();
      } else {
        /*
          Swipe / drag right:
          show the previous testimonial.
        */
        showPreviousTestimonial();
      }
    }

    isPointerDown = false;
    isHorizontalDrag = false;

    restartCarousel();
  };


  testimonialCard.addEventListener(
    "pointerup",
    finishSwipe
  );


  testimonialCard.addEventListener(
    "pointercancel",
    finishSwipe
  );


  testimonialCard.addEventListener(
    "lostpointercapture",
    finishSwipe
  );


  // ---------------------------------------------------------------------------
  // Pause while interacting
  // ---------------------------------------------------------------------------

  testimonialCard.addEventListener(
    "mouseenter",
    stopCarousel
  );


  testimonialCard.addEventListener(
    "mouseleave",
    () => {
      if (!isPointerDown) {
        startCarousel();
      }
    }
  );


  testimonialCard.addEventListener(
    "focusin",
    stopCarousel
  );


  testimonialCard.addEventListener(
    "focusout",
    startCarousel
  );


  // ---------------------------------------------------------------------------
  // Initialise
  // ---------------------------------------------------------------------------

  showTestimonial(0);
  startCarousel();
}