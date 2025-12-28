/**
 * SecureBank - Home Page Scripts
 * Purpose: Scroll reveal animations
 */

document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       SCROLL REVEAL
       =============================== */

    const revealElements = document.querySelectorAll(".reveal");

    if (!("IntersectionObserver" in window)) {
        // Fallback: show everything immediately
        revealElements.forEach(el => el.classList.add("visible"));
        return;
    }

    const revealObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target); // reveal once
                }
            });
        },
        {
            threshold: 0.15
        }
    );

    revealElements.forEach(el => revealObserver.observe(el));

});
