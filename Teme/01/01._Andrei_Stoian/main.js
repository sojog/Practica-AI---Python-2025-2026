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
        // Get the background image url from the style attribute
        const bgImage = placeholder.style.backgroundImage
          .slice(4, -1)
          .replace(/"/g, "");
        const title = item.querySelector("h3").innerText;

        lightbox.style.display = "block";
        lightboxImg.src = bgImage;
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

  // Translation Logic
  const translations = {
    en: {
      "nav-home": "Home",
      "nav-services": "Services",
      "nav-gallery": "Gallery",
      "nav-contact": "Contact",
      "footer-desc":
        "Crafting excellence for your feet. Premium repair and custom designs.",
      "footer-quick-links": "Quick Links",
      "footer-contact-us": "Contact Us",
      "footer-rights": "&copy; 2025 Glorious Shoemaker. All rights reserved.",

      // Home Page
      "hero-title": "Walk with Confidence",
      "hero-desc":
        "Master craftsmanship for your favorite shoes. Repair, restoration, and custom designs.",
      "hero-btn": "View Services",
      "about-title": "The Art of Shoemaking",
      "about-desc-1":
        "At Glorious Shoemaker, we believe that every pair of shoes tells a story. With over 20 years of experience, we combine traditional techniques with modern care to bring your footwear back to life.",
      "about-desc-2":
        "Whether it's a simple heel repair or a complete restoration of a vintage pair, we treat every shoe with the respect it deserves.",
      "about-btn": "Get in Touch",
      "featured-title": "Our Expertise",
      "service-repair": "Repair",
      "service-repair-desc":
        "Heels, soles, and stitching. We fix the wear and tear so you can keep walking.",
      "service-restoration": "Restoration",
      "service-restoration-desc":
        "Deep cleaning, color restoration, and leather conditioning for a like-new look.",
      "service-custom": "Custom Design",
      "service-custom-desc":
        "Bespoke modifications and custom-made footwear tailored to your style.",
      "all-services-btn": "All Services",

      // Services Page
      "services-title": "Our Services",
      "services-subtitle": "Comprehensive care for your footwear.",
      "srv-heel": "Heel Repair",
      "srv-heel-desc":
        "Worn down heels can affect your posture and comfort. We replace heel tips and blocks to restore balance.",
      "srv-sole": "Sole Replacement",
      "srv-sole-desc":
        "Full or half sole replacement using premium leather or rubber to extend the life of your favorite shoes.",
      "srv-clean": "Deep Cleaning & Polish",
      "srv-clean-desc":
        "Professional cleaning and polishing to remove stains, scuffs, and restore the leather's natural shine.",
      "srv-stretch": "Stretching",
      "srv-stretch-desc":
        "Shoes too tight? We can professionally stretch them for a perfect, comfortable fit.",
      "srv-color": "Color Restoration",
      "srv-color-desc":
        "Faded leather? We can match and restore the original color or dye them a new shade.",
      "srv-stitch": "Custom Stitching",
      "srv-stitch-desc":
        "Repairing loose stitching or adding decorative stitches to personalize your footwear.",
      "ask-price": "Ask for price",

      // Gallery Page
      "gallery-title": "Our Work",
      "gallery-subtitle": "A showcase of our finest craftsmanship.",
      "gal-leather": "Leather Restoration",
      "gal-heel": "Heel Replacement",
      "gal-stitch": "Custom Stitching",
      "gal-sole": "Sole Repair",
      "gal-polish": "Boot Polish",
      "gal-resole": "Full Resole",

      // Contact Page
      "contact-title": "Get in Touch",
      "contact-subtitle": "We'd love to hear from you.",
      "visit-us": "Visit Us",
      "visit-desc":
        "Come by our shop for a consultation or drop off your shoes.",
      "address-title": "Address",
      "hours-title": "Hours",
      "hours-desc":
        "Mon - Fri: 9:00 AM - 6:00 PM<br>Sat: 10:00 AM - 4:00 PM<br>Sun: Closed",
      "contact-info-title": "Contact",
      "send-msg": "Send a Message",
      "form-name": "Name",
      "form-email": "Email",
      "form-phone": "Phone (Optional)",
      "form-msg": "Message",
      "form-btn": "Send Message",
    },
    es: {
      "nav-home": "Inicio",
      "nav-services": "Servicios",
      "nav-gallery": "Galería",
      "nav-contact": "Contacto",
      "footer-desc":
        "Excelencia artesanal para tus pies. Reparación premium y diseños personalizados.",
      "footer-quick-links": "Enlaces Rápidos",
      "footer-contact-us": "Contáctanos",
      "footer-rights":
        "&copy; 2025 Glorious Shoemaker. Todos los derechos reservados.",

      // Home Page
      "hero-title": "Camina con Confianza",
      "hero-desc":
        "Maestría artesanal para tus zapatos favoritos. Reparación, restauración y diseños personalizados.",
      "hero-btn": "Ver Servicios",
      "about-title": "El Arte de la Zapatería",
      "about-desc-1":
        "En Glorious Shoemaker, creemos que cada par de zapatos cuenta una historia. Con más de 20 años de experiencia, combinamos técnicas tradicionales con el cuidado moderno para devolverle la vida a tu calzado.",
      "about-desc-2":
        "Ya sea una simple reparación de tacón o una restauración completa de un par vintage, tratamos cada zapato con el respeto que merece.",
      "about-btn": "Ponte en Contacto",
      "featured-title": "Nuestra Experiencia",
      "service-repair": "Reparación",
      "service-repair-desc":
        "Tacones, suelas y costuras. Arreglamos el desgaste para que sigas caminando.",
      "service-restoration": "Restauración",
      "service-restoration-desc":
        "Limpieza profunda, restauración de color y acondicionamiento de cuero para una apariencia como nueva.",
      "service-custom": "Diseño Personalizado",
      "service-custom-desc":
        "Modificaciones a medida y calzado personalizado adaptado a tu estilo.",
      "all-services-btn": "Todos los Servicios",

      // Services Page
      "services-title": "Nuestros Servicios",
      "services-subtitle": "Cuidado integral para tu calzado.",
      "srv-heel": "Reparación de Tacones",
      "srv-heel-desc":
        "Los tacones desgastados pueden afectar tu postura y comodidad. Reemplazamos tapas y bloques para restaurar el equilibrio.",
      "srv-sole": "Reemplazo de Suelas",
      "srv-sole-desc":
        "Reemplazo total o parcial de suelas utilizando cuero o goma premium para extender la vida de tus zapatos favoritos.",
      "srv-clean": "Limpieza Profunda y Pulido",
      "srv-clean-desc":
        "Limpieza y pulido profesional para eliminar manchas, rasguños y restaurar el brillo natural del cuero.",
      "srv-stretch": "Ensanchado",
      "srv-stretch-desc":
        "¿Zapatos muy apretados? Podemos ensancharlos profesionalmente para un ajuste perfecto y cómodo.",
      "srv-color": "Restauración de Color",
      "srv-color-desc":
        "¿Cuero desteñido? Podemos igualar y restaurar el color original o teñirlos de un nuevo tono.",
      "srv-stitch": "Costura Personalizada",
      "srv-stitch-desc":
        "Reparación de costuras sueltas o adición de costuras decorativas para personalizar tu calzado.",
      "ask-price": "Consultar precio",

      // Gallery Page
      "gallery-title": "Nuestro Trabajo",
      "gallery-subtitle": "Una muestra de nuestra mejor artesanía.",
      "gal-leather": "Restauración de Cuero",
      "gal-heel": "Reemplazo de Tacón",
      "gal-stitch": "Costura Personalizada",
      "gal-sole": "Reparación de Suela",
      "gal-polish": "Pulido de Botas",
      "gal-resole": "Resuelado Completo",

      // Contact Page
      "contact-title": "Ponte en Contacto",
      "contact-subtitle": "Nos encantaría saber de ti.",
      "visit-us": "Visítanos",
      "visit-desc":
        "Pasa por nuestra tienda para una consulta o para dejar tus zapatos.",
      "address-title": "Dirección",
      "hours-title": "Horario",
      "hours-desc":
        "Lun - Vie: 9:00 AM - 6:00 PM<br>Sáb: 10:00 AM - 4:00 PM<br>Dom: Cerrado",
      "contact-info-title": "Contacto",
      "send-msg": "Enviar Mensaje",
      "form-name": "Nombre",
      "form-email": "Correo Electrónico",
      "form-phone": "Teléfono (Opcional)",
      "form-msg": "Mensaje",
      "form-btn": "Enviar Mensaje",
    },
  };

  const langToggleBtn = document.getElementById("lang-toggle");
  let currentLang = localStorage.getItem("site-lang") || "en";

  function updateLanguage(lang) {
    const elements = document.querySelectorAll("[data-i18n]");
    elements.forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (translations[lang][key]) {
        // Check if it's an input placeholder or standard text
        if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
          el.placeholder = translations[lang][key];
        } else {
          el.innerHTML = translations[lang][key];
        }
      }
    });

    // Update button text
    if (langToggleBtn) {
      langToggleBtn.innerText = lang === "en" ? "EN | ES" : "ES | EN";
    }

    localStorage.setItem("site-lang", lang);
    currentLang = lang;
  }

  // Initialize
  if (langToggleBtn) {
    updateLanguage(currentLang);

    langToggleBtn.addEventListener("click", () => {
      const newLang = currentLang === "en" ? "es" : "en";
      updateLanguage(newLang);
    });
  }
});
