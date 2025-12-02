from django.db import models
from django.contrib.auth import get_user_model
from tours.models import Tour

User = get_user_model()


class TourView(models.Model):
    """Model pentru tracking vizualizări tururi"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='views', verbose_name='Tur')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Utilizator')
    session_id = models.CharField(max_length=100, verbose_name='ID sesiune')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Data vizualizării')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Adresă IP')
    
    class Meta:
        verbose_name = 'Vizualizare tur'
        verbose_name_plural = 'Vizualizări tururi'
        ordering = ['-viewed_at']
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonim'
        return f"{user_str} - {self.tour.name} ({self.viewed_at.strftime('%Y-%m-%d %H:%M')})"


class TourCompletion(models.Model):
    """Model pentru tracking completări tururi"""
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='completions', verbose_name='Tur')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilizator')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Data completării')
    rating_given = models.BooleanField(default=False, verbose_name='Rating dat')
    
    class Meta:
        verbose_name = 'Completare tur'
        verbose_name_plural = 'Completări tururi'
        unique_together = ['tour', 'user']
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"
