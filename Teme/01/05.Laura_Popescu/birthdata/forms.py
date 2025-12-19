from django import forms
from .models import Birthdate

class BirthdateForm(forms.ModelForm):
    class Meta:
        model = Birthdate
        fields = ['first_name', 'last_name', 'birthdate', 'relation', 'notes']
