from django import forms
from .models import Note

class NoteUploadForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all',
            'placeholder': 'Enter a title for your note...'
        })
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all',
            'accept': '.txt,.pdf,.docx,.doc,.jpg,.jpeg,.png,.webp'
        })
    )

class NoteEditForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['extracted_text']
        widgets = {
            'extracted_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all font-mono text-sm',
                'rows': 20,
                'placeholder': 'Extracted text will appear here...'
            }),
        }

class QuizGenerationForm(forms.Form):
    MODE_CHOICES = [
        ('standard', 'Standard (10 questions, mixed type, medium difficulty)'),
        ('custom', 'Custom (choose your own settings)'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('mixed', 'Mixed'),
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('mixed', 'Mixed'),
    ]
    
    FEEDBACK_CHOICES = [
        (True, 'Instant Feedback (see correct answer after each question)'),
        (False, 'Final Feedback (see results at the end)'),
    ]
    
    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'focus:ring-primary'}),
        initial='standard'
    )
    
    # Custom options (only used if mode='custom')
    question_count = forms.IntegerField(
        min_value=5,
        max_value=50,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all'
        })
    )
    
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES,
        initial='mixed',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all'
        })
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        initial='medium',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all'
        })
    )
    
    instant_feedback = forms.ChoiceField(
        choices=FEEDBACK_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'focus:ring-primary'}),
        initial=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        
        # Set standard defaults if mode is 'standard'
        if mode == 'standard':
            cleaned_data['question_count'] = 10
            cleaned_data['question_type'] = 'mixed'
            cleaned_data['difficulty'] = 'medium'
        
        return cleaned_data
