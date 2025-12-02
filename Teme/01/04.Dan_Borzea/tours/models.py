from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Tour(models.Model):
    """Model pentru tururi turistice"""
    
    CATEGORY_CHOICES = [
        ('istoric', 'Istoric'),
        ('cultural', 'Cultural'),
        ('gastronomic', 'Gastronomic'),
        ('viata_noapte', 'Viață de noapte'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('usor', 'Ușor'),
        ('mediu', 'Mediu'),
        ('dificil', 'Dificil'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nume')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug URL')
    description = models.TextField(verbose_name='Descriere')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Categorie')
    is_premium = models.BooleanField(default=False, verbose_name='Premium')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Preț (RON)')
    duration = models.IntegerField(help_text='Durată în minute', verbose_name='Durată')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='usor', verbose_name='Dificultate')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tours', verbose_name='Creat de')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ultima actualizare')
    is_active = models.BooleanField(default=True, verbose_name='Activ')
    cover_image = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name='Imagine de copertă')
    
    class Meta:
        verbose_name = 'Tur'
        verbose_name_plural = 'Tururi'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        """Calculează rating-ul mediu"""
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0
    
    @property
    def total_reviews(self):
        """Returnează numărul total de review-uri"""
        return self.reviews.count()


class Location(models.Model):
    """Model pentru locațiile dintr-un tur"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='locations', verbose_name='Tur')
    name = models.CharField(max_length=200, verbose_name='Nume locație')
    description = models.TextField(verbose_name='Descriere')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitudine')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitudine')
    order = models.IntegerField(default=0, verbose_name='Ordine')
    historical_info = models.TextField(blank=True, verbose_name='Informații istorice')
    duration_minutes = models.IntegerField(default=10, verbose_name='Durată estimată (minute)')
    
    class Meta:
        verbose_name = 'Locație'
        verbose_name_plural = 'Locații'
        ordering = ['tour', 'order']
    
    def __str__(self):
        return f"{self.tour.name} - {self.name}"


class LocationImage(models.Model):
    """Model pentru imaginile unei locații"""
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='images', verbose_name='Locație')
    image = models.ImageField(upload_to='locations/', verbose_name='Imagine')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Legendă')
    order = models.IntegerField(default=0, verbose_name='Ordine')
    
    class Meta:
        verbose_name = 'Imagine locație'
        verbose_name_plural = 'Imagini locații'
        ordering = ['location', 'order']
    
    def __str__(self):
        return f"{self.location.name} - Imagine {self.order}"


class Review(models.Model):
    """Model pentru review-uri și rating-uri"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name='Tur')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Utilizator')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Rating')
    comment = models.TextField(blank=True, verbose_name='Comentariu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ultima actualizare')
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Review-uri'
        ordering = ['-created_at']
        unique_together = ['tour', 'user']  # Un utilizator poate da un singur review per tur
    
    def __str__(self):
        return f"{self.user.username} - {self.tour.name} ({self.rating}★)"


class Favorite(models.Model):
    """Model pentru tururile favorite ale utilizatorilor"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Utilizator')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Tur')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data adăugării')
    
    class Meta:
        verbose_name = 'Favorit'
        verbose_name_plural = 'Favorite'
        unique_together = ['user', 'tour']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"


class Comment(models.Model):
    """Model pentru comentarii la tururi"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments', verbose_name='Tur')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Utilizator')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Răspuns la')
    content = models.TextField(verbose_name='Conținut')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    
    class Meta:
        verbose_name = 'Comentariu'
        verbose_name_plural = 'Comentarii'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} pe {self.tour.name}"


class OfflineContent(models.Model):
    """Model pentru conținut descărcat offline"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='offline_downloads', verbose_name='Tur')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offline_content', verbose_name='Utilizator')
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Data descărcării')
    expiry_date = models.DateTimeField(null=True, blank=True, verbose_name='Data expirării')
    
    class Meta:
        verbose_name = 'Conținut offline'
        verbose_name_plural = 'Conținut offline'
        unique_together = ['user', 'tour']
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tour.name} (offline)"
