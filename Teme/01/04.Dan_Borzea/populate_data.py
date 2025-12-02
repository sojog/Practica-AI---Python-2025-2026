"""
Script pentru popularea bazei de date cu date de test
"""
from accounts.models import CustomUser
from tours.models import Tour, Location, LocationImage
from django.utils.text import slugify

# Get admin user
try:
    admin = CustomUser.objects.get(username='admin')
except CustomUser.DoesNotExist:
    admin = CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    print("✓ Created admin user")

# Create tours
tours_data = [
    {
        'name': 'Centrul Istoric București',
        'description': 'Descoperă istoria capitală României prin locurile sale emblematice. Un tur fascinant prin centrul vechi al Bucureștiului.',
        'category': 'istoric',
        'duration': 120,
        'difficulty': 'usor',
        'is_premium': False,
        'locations': [
            {'name': 'Palatul Parlamentului', 'lat': 44.4268, 'lng': 26.0873, 'desc': 'Cea mai mare clădire administrativă din lume'},
            {'name': 'Centrul Vechi', 'lat': 44.4321, 'lng': 26.1007, 'desc': 'Zona pietonală cu restaurante și baruri'},
            {'name': 'Ateneul Român', 'lat': 44.4413, 'lng': 26.0973, 'desc': 'Sala de concerte emblematică'},
        ]
    },
    {
        'name': 'Tur Gastronomic Cluj-Napoca',
        'description': 'Explorează cele mai bune localuri și restaurante din Cluj. O experiență culinară de neuitat.',
        'category': 'gastronomic',
        'duration': 180,
        'difficulty': 'usor',
        'is_premium': True,
        'price': 150.00,
        'locations': [
            {'name': 'Piața Unirii', 'lat': 46.7704, 'lng': 23.5899, 'desc': 'Centrul orașului Cluj'},
            {'name': 'Grădina Botanică', 'lat': 46.7673, 'lng': 23.5847, 'desc': 'Cel mai frumos loc pentru relaxare'},
        ]
    },
    {
        'name': 'Brașov - Orașul Coroanei',
        'description': 'Tur cultural prin orașul medieval Brașov. Istorie, cultură și panorame spectaculoase.',
        'category': 'cultural',
        'duration': 150,
        'difficulty': 'mediu',
        'is_premium': False,
        'locations': [
            {'name': 'Piața Sfatului', 'lat': 45.6427, 'lng': 25.5887, 'desc': 'Inima orașului vechi'},
            {'name': 'Biserica Neagră', 'lat': 45.6417, 'lng': 25.5888, 'desc': 'Cea mai mare biserică gotică din România'},
            {'name': 'Tampa', 'lat': 45.6389, 'lng': 25.5961, 'desc': 'Muntele care domină orașul'},
        ]
    },
    {
        'name': 'Viața de Noapte Timișoara',
        'description': 'Descoperă barurile și cluburile din Timișoara. Perfect pentru o seară memorabilă.',
        'category': 'viata_noapte',
        'duration': 240,
        'difficulty': 'usor',
        'is_premium': True,
        'price': 100.00,
        'locations': [
            {'name': 'Piața Victoriei', 'lat': 45.7539, 'lng': 21.2267, 'desc': 'Centrul nocturn al orașului'},
            {'name': 'Piața Unirii', 'lat': 45.7574, 'lng': 21.2298, 'desc': 'Zona centrală cu restaurante'},
        ]
    },
    {
        'name': 'Sibiu - Capitala Culturală',
        'description': 'Explorează frumusețea arhitecturii săsești și tradițiile Sibiului.',
        'category': 'cultural',
        'duration': 135,
        'difficulty': 'usor',
        'is_premium': False,
        'locations': [
            {'name': 'Piața Mare', 'lat': 45.7972, 'lng': 24.1522, 'desc': 'Piața centrală cu Turnul Sfatului'},
            {'name': 'Podul Minciunilor', 'lat': 45.7961, 'lng': 24.1516, 'desc': 'Primul pod din fier forjat'},
            {'name': 'Catedrala Evanghelică', 'lat': 45.7965, 'lng': 24.1511, 'desc': 'Monument istoric impresionant'},
        ]
    },
    {
        'name': 'Iași - Orașul celor 7 Coline',
        'description': 'Tur istoric prin capitala Moldovei. Descoperă monumentele și poveștile orașului.',
        'category': 'istoric',
        'duration': 165,
        'difficulty': 'mediu',
        'is_premium': False,
        'locations': [
            {'name': 'Palatul Culturii', 'lat': 47.1585, 'lng': 27.5872, 'desc': 'Simbolul orașului Iași'},
            {'name': 'Teatrul Național', 'lat': 47.1597, 'lng': 27.5878, 'desc': 'Cel mai vechi teatru din România'},
            {'name': 'Universitatea Al.I. Cuza', 'lat': 47.1738, 'lng': 27.5741, 'desc': 'Prima universitate din România'},
        ]
    },
]

print("\n🗺️ Creez tururi și locații...\n")

for tour_data in tours_data:
    locations_data = tour_data.pop('locations')
    
    tour, created = Tour.objects.get_or_create(
        name=tour_data['name'],
        defaults={
            **tour_data,
            'slug': slugify(tour_data['name']),
            'created_by': admin,
            'price': tour_data.get('price', 0)
        }
    )
    
    if created:
        print(f"✓ Creat tur: {tour.name}")
        
        # Create locations
        for i, loc_data in enumerate(locations_data, 1):
            location = Location.objects.create(
                tour=tour,
                name=loc_data['name'],
                description=loc_data['desc'],
                latitude=loc_data['lat'],
                longitude=loc_data['lng'],
                order=i,
                duration_minutes=15,
                historical_info=f"Informații detaliate despre {loc_data['name']}. Acest loc are o istorie bogată și este un punct important în {tour.name}."
            )
            print(f"  ✓ Adăugată locație: {location.name}")
    else:
        print(f"⊘ Turul '{tour.name}' există deja")

print("\n✅ Procesul s-a finalizat cu succes!")
print(f"\n📊 Total tururi în baza de date: {Tour.objects.count()}")
print(f"📍 Total locații în baza de date: {Location.objects.count()}")
print("\n🔐 Credențiale admin:")
print("   Username: admin")
print("   Password: admin123")
print("\n🌐 Accesează aplicația la: http://127.0.0.1:8000")
print("🔧 Admin panel: http://127.0.0.1:8000/admin")
