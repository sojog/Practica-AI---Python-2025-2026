from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from quiz.models import Note, Quiz, Question

User = get_user_model()

class QuizViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        self.note = Note.objects.create(
            user=self.user,
            title='Test Note',
            extracted_text='This is a test note content.'
        )
        
        self.quiz = Quiz.objects.create(
            user=self.user,
            note=self.note,
            question_count=5,
            question_type='multiple_choice',
            difficulty='easy'
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/dashboard.html')
        self.assertContains(response, 'Test Note')

    def test_upload_note_view_get(self):
        response = self.client.get(reverse('upload_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/upload_note.html')

    def test_take_quiz_view_no_questions(self):
        response = self.client.get(reverse('take_quiz', args=[self.quiz.id]))
        # Should redirect to dashboard because no questions
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_take_quiz_view_with_questions(self):
        Question.objects.create(
            quiz=self.quiz,
            question_text='Test Question',
            question_type='multiple_choice',
            correct_answer='A',
            options=['A', 'B', 'C', 'D'],
            order=1
        )
        Question.objects.create(
            quiz=self.quiz,
            question_text='Fill blank',
            question_type='fill_in_blank',
            correct_answer='answer',
            order=2
        )
        response = self.client.get(reverse('take_quiz', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/take_quiz.html')
        self.assertContains(response, 'Test Question')

    def test_quiz_result_view(self):
        response = self.client.get(reverse('quiz_result', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/quiz_result.html')

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))
