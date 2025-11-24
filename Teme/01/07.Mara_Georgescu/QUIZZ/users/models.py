from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Add any additional fields here if needed
    
    def __str__(self):
        return self.username
