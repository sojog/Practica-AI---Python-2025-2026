from django.db import models
from birthdata.models import Birthdate

class GiftSuggestion(models.Model):
    """
    Stores AI-generated gift suggestions for caching purposes.
    Allows instant retrieval without repeated API calls.
    """
    birthdate = models.ForeignKey(Birthdate, on_delete=models.CASCADE, related_name='gift_suggestions')
    item = models.CharField(max_length=255)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.item} for {self.birthdate.full_name}"

class SocialAura(models.Model):
    """
    Stores AI-generated social aura descriptions and keywords.
    """
    birthdate = models.ForeignKey(Birthdate, on_delete=models.CASCADE, related_name='social_aura')
    description = models.TextField()
    keywords = models.CharField(max_length=255) # Comma-separated
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Aura for {self.birthdate.full_name}"

class Compatibility(models.Model):
    """
    Stores compatibility analysis between two contacts.
    """
    person_a = models.ForeignKey(Birthdate, related_name='compatibility_a', on_delete=models.CASCADE)
    person_b = models.ForeignKey(Birthdate, related_name='compatibility_b', on_delete=models.CASCADE)
    compatibility_score = models.IntegerField() # 0-100
    analysis = models.TextField()
    short_verdict = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure we don't have duplicate A-B and B-A records (enforced by logic, storage is one way)
        unique_together = ('person_a', 'person_b')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.person_a} & {self.person_b}"
