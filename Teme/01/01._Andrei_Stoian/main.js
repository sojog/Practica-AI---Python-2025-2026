document.addEventListener("DOMContentLoaded", () => {
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const navMenu = document.getElementById("nav-menu");

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener("click", () => {
      navMenu.classList.toggle("active");
    });
  }

  // Lightbox Logic
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const captionText = document.getElementById("caption");
  const closeBtn = document.querySelector(".close-lightbox");
  const galleryItems = document.querySelectorAll(".gallery-item");

  if (lightbox) {
    galleryItems.forEach((item) => {
      item.addEventListener("click", () => {
        const placeholder = item.querySelector(".gallery-img-placeholder");
        const title = item.querySelector("h3").innerText;

        // In a real scenario, we'd get the src from an img tag.
        // Here we'll just use a placeholder color or text for demo since we don't have real images.
        // For demo purposes, let's just show the title in the lightbox or a generic placeholder.
        lightbox.style.display = "block";
        // lightboxImg.src = ...; // Set image source
        captionText.innerHTML = title;
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        lightbox.style.display = "none";
      });
    }

    window.addEventListener("click", (e) => {
      if (e.target == lightbox) {
        lightbox.style.display = "none";
      }
    });
  }
});
