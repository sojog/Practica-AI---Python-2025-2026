# To Do — Site prezentare pentru un cizmar

**Scop:** Construiește un site simplu, clar și performant care prezintă serviciile cizmarului, galerie cu lucrări, posibilitate de contact/rezervare și informații de bază (program, adresă, telefon).

**Pași principali (ordine recomandată):**

1. Cercetare & brief client

   - **Discuție client:** Notează ce servicii oferă (reparații, restaurări, confecții), prețuri orientative, ore de lucru, locație.
   - **Concurență:** Adună 2–3 site-uri/conturi Instagram locale pentru inspirație.

2. Stabilire conținut și mesaje

   - **Listează paginile esențiale:** `Home`, `Servicii`, `Galerie`, `Despre`, `Contact` (+ `Testimoniale` opțional).
   - **Texte:** Scrie titluri scurte pentru hero, descriere servicii (bulleted), descriere despre cizmar (poveste, experiență).

3. Colectare active

   - **Fotografii:** 10-15 imagini optimizate cu lucrări înainte/după; solicită imagini în lumină bună.
   - **Logo & contact:** Logo (sau nume în font simplu), număr de telefon, adresă, e-mail, link harta.

4. Sitemap & wireframes

   - **Sitemap scurt:** `Home` (hero, servicii, galerie, testimonial, CTA), `Servicii` (detaliat), `Galerie`, `Contact`.
   - **Wireframe:** Schițe simple pentru `Home` și `Servicii` (desktop + mobile).

5. Design vizual

   - **Paletă & fonturi:** Alege 2 culori principale, un font pentru titluri și unul pentru text; păstrează designul curat.
   - **Mockup minimal:** Pagina Home aprox. (imagini, buton programare, apel click-to-call).

6. Pregătire fișiere

   - **Optimizează imagini:** export JPG/WEBP la dimensiuni potrivite (ex: preview 1200px, thumbs 600px), comprimare.
   - **Export logo:** SVG/PNG.

7. Implementare (static)

   - **Structură fișiere:** `index.html`, `services.html`, `gallery.html`, `contact.html`, `css/style.css`, `js/main.js` (dacă e nevoie).
   - **Header/Footer:** meniu simplu, footer cu date de contact și link hartă.
   - **Galerie:** grid responsive cu lightbox (poate o soluție JS mică sau CSS-only).

8. Funcționalități practice

   - **Formular contact:** trimite pe e-mail (backend simplu) sau folosește Google Forms / Formspree dacă nu ai server.
   - **Click-to-call:** buton pentru apel pe mobil și link adresă către Google Maps.

9. Responsivitate & accesibilitate

   - **Mobile-first:** testează pe ecran mic; meniu hamburger dacă e nevoie.
   - **Accesibilitate:** `alt` pentru imagini, contrast text, focus states pentru linkuri.

10. SEO & performanță

    - **Meta tags:** `title`, `description` pentru fiecare pagină; schema `LocalBusiness` minim.
    - **Optimizare:** minifică CSS/JS, lazy-load pentru imagini, cache headers la hosting.

11. Testare & QA

    - **Test cross-browser:** Chrome, Edge, Firefox; verifică formularul și link-urile.
    - **Verificări:** viteza, imagini încărcate, text tăiat pe mobile.

12. Lansare & hosting

    - **Alegere hosting:** Netlify/Vercel pentru static (gratuit + SSL), sau hostingul clientului.
    - **DNS & SSL:** configurează domeniu și verifică HTTPS.

13. Mentenanță & analitică
    - **Instrumente:** configurează Google Analytics & Search Console.
    - **Plan mentenanță:** update imagini, actualizare program/servicii, backup lunar.

**Sarcini detaliate imediate (prima zi):**

- Sună/întâlnește clientul și notează: servicii, program, adresa, 5 fotografii urgente.
- Scrie textul pentru `Home` și lista de servicii (bullets).
- Alege paleta de culori și fontul principal.

**Criterii de finalizare:**

- Siteul afișează corect paginile esențiale, formularul trimite mesaj, butonul apel funcționează pe mobil, imaginile se încarcă optim.

Dacă vrei, pot: 1) genera un wireframe HTML/CSS minimal, 2) crea template-ul `index.html` inițial, sau 3) pregăti textul final pentru fiecare pagină. Spune-mi ce preferi mai întâi.
