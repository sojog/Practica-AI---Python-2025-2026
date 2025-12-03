from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)  # Original filename
    file_content = models.BinaryField()  # Store file in database
    file_type = models.CharField(max_length=100)  # MIME type
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Quiz(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', _('Multiple Choice')),
        ('true_false', _('True/False')),
        ('fill_in_blank', _('Fill in the Blank')),
        ('short_answer', _('Short Answer')),
        ('mixed', _('Mixed')),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
        ('mixed', _('Mixed')),
    ]
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='quizzes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizzes')
    question_count = models.IntegerField(default=10)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='mixed')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    instant_feedback = models.BooleanField(default=False)
    is_recap = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Quiz {self.id} - {self.note.title}"
    
    def get_score(self):
        """Calculate the score for this quiz"""
        total = self.questions.count()
        if total == 0:
            return 0, 0
        correct = Answer.objects.filter(question__quiz=self, is_correct=True).count()
        return correct, total

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', _('Multiple Choice')),
        ('true_false', _('True/False')),
        ('fill_in_blank', _('Fill in the Blank')),
        ('short_answer', _('Short Answer')),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    correct_answer = models.TextField()
    options = models.JSONField(default=list, blank=True)  # For multiple choice options
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Q{self.question.order} - {'✓' if self.is_correct else '✗'}"

class Mistake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mistakes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mistakes')
    incorrect_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:50]}"
