"""
Script pentru popularea database-ului cu tururi pentru orașe din România
Usage: python3 populate_tours_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walking_tour_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from tours.models import Tour, Location

User = get_user_model()

def populate_tours():
    """Populează database-ul cu tururi pentru orașe din România"""
    
    # Obține sau creează admin user pentru tururi
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@walkingtour.ro', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Created admin user")
    
    tours_data = [
        # BUCUREȘTI
        {
            'name': 'Centrul Vechi București - Istorie și Arhitectură',
            'city': 'bucuresti',
            'category': 'istoric',
            'difficulty': 'usor',
            'duration': 150,
            'price': 0,
            'description': '''Descoperă inima istorică a Bucureștiului într-un tur fascinant prin Centrul Vechi! 
            
Vei explora străzile pavate cu pietre cubice, clădirile istorice restaurate și piețele vii care definesc caracterul unic al capitalei României. Turul include vizite la Hanul lui Manuc (cel mai vechi han păstrat în București), Biserica Stavropoleos (un exemplu remarcabil de arhitectură brâncovenească), și strada Lipscani - arteria comercială principală din Bucureștiul medieval.

Ghidul tău local îți va povesti despre transformarea spectaculoasă a acestei zone: de la cartier comercial în epoca medievală, la zona distrugerii din perioada comunistă, până la renovarea modernă care a transformat-o în cel mai vibrant cartier al orașului. Vei afla povești despre negustorii greci și armeni care au dat numele străzilor, despre revoluția din 1989, și despre cultura cafelei din București.

Puncte de interes: Hanul lui Manuc, Biserica Stavropoleos, Strada Lipscani, Pasajul Macca-Villacrosse, Banca Națională a României.''',
            'cover_image': 'tours/bucharest_old_town_1768561283187.png',
            'locations': [
                {'name': 'Hanul lui Manuc', 'lat': 44.4268, 'lng': 26.1025},
                {'name': 'Biserica Stavropoleos', 'lat': 44.4315, 'lng': 26.1028},
                {'name': 'Strada Lipscani', 'lat': 44.4322, 'lng': 26.1019},
            ]
        },
        {
            'name': 'Palatele București - Communist & Royal Heritage',
            'city': 'bucuresti',
            'category': 'cultural',
            'difficulty': 'mediu',
            'duration': 180,
            'price': 0,
            'description': '''Un tur captivant care explorează contrastul dramatic între moștenirea regală și cea comunistă a Bucureștiului.

Vei vizita impresionantul Palat al Parlamentului - a doua cea mai mare clădire administrativă din lume după Pentagon. Construit în timpul regimului lui Nicolae Ceaușescu, acest palat gigantic este un testament al megalomaniei comuniste, dar și un exemplu remarcabil de artizanat românesc. Fiecare sală este decorată cu marmură, lemn sculptat și candelabre masive.

Turul continuă către fosta Piață a Palatului Regal (azi Piața Revoluției), unde vei afla despre evenimentele dramatice din decembrie 1989. Vei vedea fostul sediu al Partidului Comunist, Palatul Regal, și Ateneul Român - simbolul culturii românești.

Ideal pentru: pasionați de istorie, fotografi, cei interesați de arhitectură monumentală.''',
            'cover_image': 'tours/bucharest_old_town_1768561283187.png',
            'locations': [
                {'name': 'Palatul Parlamentului', 'lat': 44.4276, 'lng': 26.0874},
                {'name': 'Piața Revoluției', 'lat': 44.4396, 'lng': 26.0970},
                {'name': 'Ateneul Român', 'lat': 44.4413, 'lng': 26.0973},
            ]
        },
        {
            'name': 'Food Tour București - Savori Tradiționale',
            'city': 'bucuresti',
            'category': 'gastronomic',
            'difficulty': 'usor',
            'duration': 180,
            'price': 150,
            'description': '''Descoperă bucătăria tradițională românească într-un tur gastronomic autentic prin București!

Vei degusta preparate clasice românești în restaurante și bodegi selectate cu grijă: sarmale (rulouri de varză umplute cu carne și orez), mici (cârnați tradițional), mămăligă cu brânză și smântână, și desertul tradițional cozonac. Fiecare oprire vine cu povești despre originea preparatelor și semnificația lor culturală.

Turul include și o vizită la Piața Obor sau Piața Dorobanți, unde vei vedea produse locale proaspete și vei interacționa cu vânzătorii locali. Vei învăța despre ingredientele autentice românești și cum să le recunoști.

Turul se încheie într-o cramă tradițională unde vei degusta vinuri românești însoțite de brânzeturi locale. Ghidul tău te va învăța despre reînvierea industriei vinicole românești și despre regiunile viticole principale.

Prețul include: toate degustările, băuturile, și un booklet cu rețete tradiționale.''',
            'cover_image': 'tours/bucharest_old_town_1768561283187.png',
            'locations': [
                {'name': 'Caru cu Bere', 'lat': 44.4312, 'lng': 26.1022},
                {'name': 'Piața Obor', 'lat': 44.4495, 'lng': 26.1256},
                {'name': 'Hanul Berarilor', 'lat': 44.4318, 'lng': 26.1015},
            ]
        },
        
        # CLUJ-NAPOCA
        {
            'name': 'Cluj Historic Walking Tour - Heart of Transylvania',
            'city': 'cluj',
            'category': 'istoric',
            'difficulty': 'usor',
            'duration': 120,
            'price': 0,
            'description': '''Explorează centrul istoric al Clujului, capitala neoficială a Transilvaniei!

Turul începe în Piața Unirii, piața centrală din Cluj, dominată de impozanta Catedrală Sf. Mihail - un exemplu superb de arhitectură gotică din secolul XIV. Vei afla despre istoria multietnică a Clujului: maghiari, români, germani sași, și evrei care au coexistent aici secole la rând.

Vei vizita Biserica Reformată din Piața Museion, Bastionul Croitorilor (parte din fortificațiile medievale), și strada Matei Corvin - una dintre cele mai frumoase străzi din Cluj. Ghidul tău îți va povesti despre Matei Corvin (Matthias Corvinus), regele renascentist născut aici, și despre transformarea Clujului într-un centru academic și IT.

Puncte de interes: Biserica Sf. Mihail, Statuia Matei Corvin, Bastionul Croitorilor, Palatul Bánffy.

Perfect pentru: first-time visitors, history buffs, fotografi urbani.''',
            'cover_image': 'tours/cluj_center_1768561297340.png',
            'locations': [
                {'name': 'Piața Unirii', 'lat': 46.7693, 'lng': 23.5899},
                {'name': 'Biserica Sf. Mihail', 'lat': 46.7700, 'lng': 23.5898},
                {'name': 'Bastionul Croitorilor', 'lat': 46.7672, 'lng': 23.5854},
            ]
        },
        {
            'name': 'Art & Culture Cluj - Museums and Galleries',
            'city': 'cluj',
            'category': 'cultural',
            'difficulty': 'usor',
            'duration': 150,
            'price': 0,
            'description': '''Un tur cultural care explorează scena artistică vibrantă a Clujului.

Cluj-Napoca s-a transformat într-un centru cultural major în ultimii ani. Vei vizita Muzeul Național de Artă (în Palatul Bánffy), unde vei admira opere de artă românească și europeană. Turul continuă prin cartierul artistic unde vei descoperi galerii contemporane, street art, și instalații urbane.

Vei afla despre evenimentele culturale majore ale Clujului: TIFF (Transilvania International Film Festival), Electric Castle festival, și Jazz in the Park. Ghidul tău te va plimba prin cele mai Instagram-able spots din Cluj și îți va recomanda cafenele și librării independente.

Include și o vizită la Grădina Botanică "Alexandru Borza" - o oază de liniște cu peste 10,000 de specii de plante.''',
            'cover_image': 'tours/cluj_center_1768561297340.png',
            'locations': [
                {'name': 'Muzeul de Artă Cluj', 'lat': 46.7707, 'lng': 23.5912},
                {'name': 'Grădina Botanică', 'lat': 46.7658, 'lng': 23.5851},
                {'name': 'Piața Muzeului', 'lat': 46.7706, 'lng': 23.5865},
            ]
        },
        
        # BRAȘOV  
        {
            'name': 'Medieval Brașov - Fortresses & Legends',
            'city': 'brasov',
            'category': 'istoric',
            'difficulty': 'mediu',
            'duration': 180,
            'price': 0,
            'description': '''Călătorie în timp prin Brașovul medieval, unul dintre cele mai bine păstrate orașe medievale din Europa!

Turul începe în Piața Sfatului, inima Brașovului, unde vei vedea Casa Sfatului (acum Muzeul de Istorie). De aici, vei urma străzile înguste pavate către Biserica Neagră - cea mai mare biserică gotică din România, numită astfel după incendiul din 1689 care a înnegrit zidurile.

Vei explora strada Sforii - una dintre cele mai înguste străzi din Europa (doar 1.3m lățime!), și vei urca către Bastionul Țesătorilor pentru vederi panoramice. Ghidul tău îți va povesti despre coloniștii sași care au construit Brașovul în secolul XIII, despre atacurile otomane, și despre cum orașul a devenit un centru comercial important.

Turul include și povestea despre Dracula - vei afla adevărul despre Vlad Țepeș și legătura sa cu Brașovul. 

Dificultate medie datorită urcușurilor pe străzi pavate.''',
            'cover_image': 'tours/brasov_council_square_1768561310934.png',
            'locations': [
                {'name': 'Piața Sfatului', 'lat': 45.6427, 'lng': 25.5887},
                {'name': 'Biserica Neagră', 'lat': 45.6397, 'lng': 25.5889},
                {'name': 'Bastionul Țesătorilor', 'lat': 45.6453, 'lng': 25.5976},
            ]
        },
        
        # SIBIU
        {
            'name': 'Sibiu Fairy Tale - Piețe și Poduri',
            'city': 'sibiu',
            'category': 'istoric',
            'difficulty': 'usor',
            'duration': 120,
            'price': 0,
            'description': '''Descoperă farmecul medieval al Sibiului, Capitala Culturală Europeană 2007!

Sibiul este cunoscut pentru "ochii" săi - ferestrele din acoperișurile caselor vechi care par să privească spre tine. Turul începe în Piața Mare, cea mai impresionantă piață din Transilvania, înconjurată de palate baroque colorate și dominată de Turnul Sfatului.

Vei traversa Podul Minciunilor (legenda spune că se prăbușește dacă spui minciuni pe el!), vei explora Piața Mică cu atelierele de artizani, și vei vizita Catedrala Evanghelică cu turnul său impozant. 

Ghidul îți va povesti despre coloniștii sași care au fondat Sibiul în secolul XII, despre cele 39 de bresle care făceau societatea medievală, și despre transformarea Sibiului într-un oraș cosmopolit modern.

Ideal pentru: familii, fotografi, romantic getaways.''',
            'cover_image': 'tours/sibiu_grande_square_1768561322684.png',
            'locations': [
                {'name': 'Piața Mare Sibiu', 'lat': 45.7970, 'lng': 24.1519},
                {'name': 'Podul Minciunilor', 'lat': 45.7964, 'lng': 24.1506},
                {'name': 'Turnul Sfatului', 'lat': 45.7963, 'lng': 24.1521},
            ]
        },
        
        # TIMIȘOARA
        {
            'name': 'Timișoara Revolution Tour - 1989 & Beyond',
            'city': 'timisoara',
            'category': 'istoric',
            'difficulty': 'usor',
            'duration': 150,
            'price': 0,
            'description': '''Un tur emoționant prin orașul unde a început Revoluția Română din 1989!

Timișoara a fost primul oraș liber de comunism din România. Turul începe la Biserica Reformată din Piața Maria, unde protestele au început pe 15 decembrie 1989. Vei afla povestile celor care au participat la revoluție, vei vedea Memorialul Revoluției, și vei înțelege evenimentele care au dus la căderea regimului Ceaușescu.

Turul continuă prin Piața Unirii și Piața Libertății, unde vei admira arhitectura baroque colorată care i-a adus Timișoarei porecla de "Mica Vienă". Vei vizita Catedrala Mitropolitană Ortodoxă și Bastionul Maria Therezia.

Ghidul tău îți va povești despre multiculturalismul Timișoarei - români, germani, sârbi, maghiari care au coexistent pașnic aici. Vei afla despre transformarea orașului post-revoluție și despre nominalizarea sa ca Capitală Culturală Europeană 2023.

Extrem de recomandat pentru: cei interesați de istorie recent, politics, sociologie.''',
            'cover_image': 'tours/timisoara_union_square_1768561338007.png',
            'locations': [
                {'name': 'Piața Victoriei', 'lat': 45.7537, 'lng': 21.2255},
                {'name': 'Catedrala Mitropolitană', 'lat': 45.7521, 'lng': 21.2296},
                {'name': 'Piața Unirii', 'lat': 45.7588, 'lng': 21.2298},
            ]
        },
        
        # IAȘI
        {
            'name': 'Iași Cultural Capital - Churches & Palaces',
            'city': 'iasi',
            'category': 'cultural',
            'difficulty': 'mediu',
            'duration': 180,
            'price': 0,
            'description': '''Explorează bogăția culturală a Iașului, fosta capitală a Moldovei și orașul celor 100 de biserici!

Turul începe la impresionantul Palat al Culturii - un edificiu neo-gothic maiestuos care adăpostește patru muzee. Vei afla despre domnitorii Moldovei care au guvernat de aici, despre Unirea Principatelor din 1859, și despre transformarea Iașului într-un centru cultural major.

Vei vizita Biserica Trei Ierarhi - un exemplu unic de arhitectură moldovenească cu fațada acoperită de ornamente sculptate în piatră. Ghidul îți va povesti despre Vasile Lupu și Dimitrie Cantemir, despre scriitori celebri ieșeni (Mihai Eminescu, Ion Creangă), și despre Universitatea "Alexandru Ioan Cuza" - prima universitate modernă din România.

Turul include și Boulevard Ștefan cel Mare - arteria principală cu clădiri elegante și monumente istorice.

Dificultate medie datorită distanțelor mai lungi între obiective.''',
            'cover_image': 'tours/iasi_palace_culture_1768561351999.png',
            'locations': [
                {'name': 'Palatul Culturii', 'lat': 47.1583, 'lng': 27.5869},
                {'name': 'Biserica Trei Ierarhi', 'lat': 47.1594, 'lng': 27.5889},
                {'name': 'Bulevardul Ștefan cel Mare', 'lat': 47.1628, 'lng': 27.5744},
            ]
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for tour_data in tours_data:
        # Extrage datele pentru locații
        locations_data = tour_data.pop('locations', [])
        
        # Creează sau actualizează turul
        tour, created = Tour.objects.update_or_create(
            name=tour_data['name'],
            defaults={
                **tour_data,
                'created_by': admin_user,
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {tour.name} ({tour.get_city_display()})")
        else:
            updated_count += 1
            print(f"↻ Updated: {tour.name} ({tour.get_city_display()})")
        
        # Creează locații pentru tur
        for loc_data in locations_data:
            Location.objects.get_or_create(
                tour=tour,
                name=loc_data['name'],
                defaults={
                    'latitude': loc_data['lat'],
                    'longitude': loc_data['lng'],
                    'order': locations_data.index(loc_data) + 1
                }
            )
    
    print(f"\n✅ Populare completă!")
    print(f"   📊 {created_count} tururi noi create")
    print(f"   🔄 {updated_count} tururi actualizate")
    print(f"   📍 {sum(len(t.get('locations', [])) for t in tours_data)} locații adăugate")
    print(f"\n🎯 Total tururi în database: {Tour.objects.count()}")
    print(f"   București: {Tour.objects.filter(city='bucuresti').count()}")
    print(f"   Cluj-Napoca: {Tour.objects.filter(city='cluj').count()}")
    print(f"   Brașov: {Tour.objects.filter(city='brasov').count()}")
    print(f"   Sibiu: {Tour.objects.filter(city='sibiu').count()}")
    print(f"   Timișoara: {Tour.objects.filter(city='timisoara').count()}")
    print(f"   Iași: {Tour.objects.filter(city='iasi').count()}")

if __name__ == '__main__':
    print("🚀 Starting tour population...\n")
    populate_tours()
    print("\n✨ Done! Visit http://127.0.0.1:8001/tours/ to see the tours!")
