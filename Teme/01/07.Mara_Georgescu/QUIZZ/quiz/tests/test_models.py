from django.test import TestCase
from django.contrib.auth import get_user_model
from quiz.models import Note, Quiz, Question

User = get_user_model()

class QuizModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.note = Note.objects.create(
            user=self.user,
            title='Test Note',
            extracted_text='Content'
        )

    def test_note_creation(self):
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.user, self.user)

    def test_quiz_creation(self):
        quiz = Quiz.objects.create(
            user=self.user,
            note=self.note,
            question_count=10,
            question_type='mixed',
            difficulty='medium'
        )
        self.assertEqual(quiz.question_count, 10)
        self.assertEqual(quiz.difficulty, 'medium')

    def test_question_creation(self):
        quiz = Quiz.objects.create(
            user=self.user,
            note=self.note,
            question_count=5
        )
        question = Question.objects.create(
            quiz=quiz,
            question_text='What is?',
            question_type='multiple_choice',
            correct_answer='A',
            order=1
        )
        self.assertEqual(question.question_text, 'What is?')
        self.assertEqual(question.quiz, quiz)

    def test_quiz_get_score(self):
        quiz = Quiz.objects.create(
            user=self.user,
            note=self.note,
            question_count=2
        )
        q1 = Question.objects.create(quiz=quiz, question_text='Q1', correct_answer='A', order=1)
        q2 = Question.objects.create(quiz=quiz, question_text='Q2', correct_answer='B', order=2)
        
        from quiz.models import Answer
        Answer.objects.create(user=self.user, question=q1, user_answer='A', is_correct=True)
        Answer.objects.create(user=self.user, question=q2, user_answer='C', is_correct=False)
        
        correct, total = quiz.get_score()
        self.assertEqual(correct, 1)
        self.assertEqual(total, 2)
