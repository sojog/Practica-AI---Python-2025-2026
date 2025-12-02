from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model cu rol pentru sistemul de tururi"""
    
    ROLE_CHOICES = [
        ('tourist', 'Turist'),
        ('guide', 'Ghid'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='tourist',
        verbose_name='Rol'
    )
    bio = models.TextField(blank=True, verbose_name='Biografie')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    
    class Meta:
        verbose_name = 'Utilizator'
        verbose_name_plural = 'Utilizatori'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    """Profil utilizator cu statistici"""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    total_tours_completed = models.IntegerField(default=0, verbose_name='Tururi completate')
    total_reviews = models.IntegerField(default=0, verbose_name='Review-uri date')
    joined_date = models.DateTimeField(auto_now_add=True, verbose_name='Data înregistrării')
    
    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiluri'
    
    def __str__(self):
        return f"Profil {self.user.username}"
