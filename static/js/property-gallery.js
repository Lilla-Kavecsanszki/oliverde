document.addEventListener("DOMContentLoaded", () => {
  const triggers = Array.from(
    document.querySelectorAll(".property-gallery-trigger")
  );

  const lightbox = document.getElementById("property-lightbox");

  if (!triggers.length || !lightbox) {
    return;
  }

  const image = lightbox.querySelector(".lightbox-image");
  const caption = lightbox.querySelector(".lightbox-caption");
  const section = lightbox.querySelector(".lightbox-section");
  const counter = lightbox.querySelector(".lightbox-counter");

  const closeButton = lightbox.querySelector(".lightbox-close");
  const previousButton = lightbox.querySelector(".lightbox-previous");
  const nextButton = lightbox.querySelector(".lightbox-next");

  let currentIndex = 0;
  let lastFocusedElement = null;

  function displayImage(index) {
    currentIndex = (index + triggers.length) % triggers.length;

    const trigger = triggers[currentIndex];
    const imageUrl = trigger.dataset.galleryImage;
    const imageCaption = trigger.dataset.galleryCaption || "";
    const imageSection = trigger.dataset.gallerySection || "";

    image.classList.remove("is-loaded");

    image.src = imageUrl;
    image.alt = imageCaption;
    caption.textContent = imageCaption;
    section.textContent = imageSection;
    counter.textContent = `${currentIndex + 1} / ${triggers.length}`;
  }

  function openLightbox(index) {
    lastFocusedElement = document.activeElement;

    displayImage(index);

    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");

    closeButton.focus();
  }

  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("lightbox-open");

    if (lastFocusedElement) {
      lastFocusedElement.focus();
    }
  }

  function showPrevious() {
    displayImage(currentIndex - 1);
  }

  function showNext() {
    displayImage(currentIndex + 1);
  }

  triggers.forEach((trigger, index) => {
    trigger.addEventListener("click", () => {
      openLightbox(index);
    });
  });

  closeButton.addEventListener("click", closeLightbox);
  previousButton.addEventListener("click", showPrevious);
  nextButton.addEventListener("click", showNext);

  /*
   * Clicking the enlarged photograph again closes the viewer.
   * It never advances or starts an automatic slideshow.
   */
  image.addEventListener("click", closeLightbox);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!lightbox.classList.contains("is-open")) {
      return;
    }

    if (event.key === "Escape") {
      closeLightbox();
    }

    if (event.key === "ArrowLeft") {
      showPrevious();
    }

    if (event.key === "ArrowRight") {
      showNext();
    }
  });

  /*
   * Subtle staggered appearance as each chapter enters the viewport.
   */
  const revealItems = document.querySelectorAll(".gallery-reveal");

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries, galleryObserver) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          galleryObserver.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
      }
    );

    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => {
      item.classList.add("is-visible");
    });
  }
});