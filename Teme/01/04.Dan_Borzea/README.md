# Walking Tour Romania 🗺️

Aplicație web pentru tururi ghidate virtuale cu Django backend, GPS tracking, și funcționalități interactive.

## Caracteristici

- 🗺️ **Tururi Interactive** cu hărți Leaflet.js și marcaje GPS
- 👥 **3 Tipuri de Utilizatori**: Turiști, Ghizi, Administratori
- ⭐ **Sistem de Rating și Review-uri**
- ❤️ **Favorite și Comentarii**
- 📥 **Acces Offline** pentru conținut descărcat
- 💎 **Tururi Premium** cu marcare manuală
- 📊 **Analytics** pentru tracking vizualizări și comportament
- 📱 **Design Responsiv** modern

## Instalare

```bash
# Instalează dependențele
pip install -r requirements.txt

# Rulează migrările (deja făcute)
python manage.py migrate

# Creează superuser
python manage.py createsuperuser

# Rulează serverul
python manage.py runserver
```

## Acces

- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Structură

- `accounts/` - Autentificare și profile utilizatori
- `tours/` - Tururi, locații, reviews, favorite
- `analytics/` - Tracking vizualizări și completări
- `templates/` - Template-uri Django
- `static/` - CSS și JavaScript

## Categorii Tururi

1. 🏛️ **Istoric** - Locuri istorice și monumente
2. 🎭 **Cultural** - Muzee, teatre, artă
3. 🍽️ **Gastronomic** - Restaurante și experiențe culinare
4. 🌃 **Viață de Noapte** - Baruri, cluburi, evenimente

## Tehnologii

- **Backend**: Django 5.1.6, SQLite
- **Frontend**: Django Templates, HTML5, CSS3, JavaScript
- **Hărți**: Leaflet.js (OpenStreetMap)
- **Design**: Modern, responsive, mobile-first

## Planuri Viitoare

- [ ] Ghiduri audio pentru locații
- [ ] Integrare PayPal pentru tururi premium
- [ ] Migrare la PostgreSQL
- [ ] Suport multi-limbă
- [ ] Notificări pentru tururi noi
- [ ] App mobilă nativă

## Dezvoltare

Creat cu ❤️ pentru explorarea României pas cu pas!
