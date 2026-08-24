document.addEventListener("DOMContentLoaded", () => {

  const selects = document.querySelectorAll("[data-custom-select]");

  if (!selects.length) {
    return;
  }


  const closeSelect = (select) => {

    const trigger = select.querySelector(".custom-select-trigger");

    select.classList.remove("open");

    if (trigger) {
      trigger.setAttribute("aria-expanded", "false");
    }

  };


  const closeAllSelects = (except = null) => {

    selects.forEach((select) => {

      if (select !== except) {
        closeSelect(select);
      }

    });

  };


  selects.forEach((select) => {

    const trigger = select.querySelector(".custom-select-trigger");
    const value = select.querySelector(".custom-select-value");
    const input = select.querySelector("[data-custom-select-input]");
    const options = Array.from(
      select.querySelectorAll(".custom-select-option")
    );


    if (!trigger || !value || !input || !options.length) {
      return;
    }


    /* ---------- OPEN / CLOSE ---------- */

    trigger.addEventListener("click", () => {

      const isOpen = select.classList.contains("open");

      closeAllSelects(select);

      if (isOpen) {

        closeSelect(select);

      } else {

        select.classList.add("open");
        trigger.setAttribute("aria-expanded", "true");

      }

    });


    /* ---------- SELECT OPTION ---------- */

    options.forEach((option) => {

      option.addEventListener("click", () => {

        const newValue = option.dataset.value ?? "";

        input.value = newValue;
        value.textContent = option.textContent.trim();


        options.forEach((item) => {

          item.classList.remove("selected");
          item.setAttribute("aria-selected", "false");

        });


        option.classList.add("selected");
        option.setAttribute("aria-selected", "true");


        closeSelect(select);


        /*
          Submit the existing GET filter form.
          Destination and sort remain normal query parameters.
        */

        if (input.form) {
          input.form.submit();
        }

      });

    });


    /* ---------- KEYBOARD SUPPORT ---------- */

    trigger.addEventListener("keydown", (event) => {

      if (
        event.key === "ArrowDown" ||
        event.key === "ArrowUp"
      ) {

        event.preventDefault();

        closeAllSelects(select);

        select.classList.add("open");
        trigger.setAttribute("aria-expanded", "true");


        const selectedOption =
          select.querySelector(".custom-select-option.selected") ||
          options[0];

        selectedOption.focus();

      }

    });


    options.forEach((option, index) => {

      option.addEventListener("keydown", (event) => {

        if (event.key === "ArrowDown") {

          event.preventDefault();

          const next =
            options[index + 1] ||
            options[0];

          next.focus();

        }


        if (event.key === "ArrowUp") {

          event.preventDefault();

          const previous =
            options[index - 1] ||
            options[options.length - 1];

          previous.focus();

        }


        if (event.key === "Escape") {

          event.preventDefault();

          closeSelect(select);
          trigger.focus();

        }


        if (event.key === "Tab") {

          closeSelect(select);

        }

      });

    });

  });


  /* ---------- CLICK OUTSIDE ---------- */

  document.addEventListener("click", (event) => {

    selects.forEach((select) => {

      if (!select.contains(event.target)) {
        closeSelect(select);
      }

    });

  });


  /* ---------- GLOBAL ESCAPE ---------- */

  document.addEventListener("keydown", (event) => {

    if (event.key !== "Escape") {
      return;
    }


    selects.forEach((select) => {

      if (select.classList.contains("open")) {

        const trigger =
          select.querySelector(".custom-select-trigger");

        closeSelect(select);

        if (trigger) {
          trigger.focus();
        }

      }

    });

  });

});