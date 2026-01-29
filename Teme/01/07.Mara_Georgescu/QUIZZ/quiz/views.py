from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note, Quiz
from .forms import NoteUploadForm, NoteEditForm
from .services import extract_text_from_file
from django.utils.translation import gettext as _
import unicodedata
from difflib import SequenceMatcher

def normalize_answer(text):
    """
    Normalize text to remove diacritics and convert to lowercase.
    Example: 'Lăpușneanu' -> 'lapusneanu'
    """
    if not text:
        return ""
    # Normalize unicode characters to NFD (decomposed) form
    text = unicodedata.normalize('NFD', str(text))
    # Filter out non-spacing mark characters (diacritics)
    text = "".join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().strip()

def convert_text_numbers(text):
    """
    Convert text numbers to digits for Romanian.
    Example: 'trei secvente' -> '3 secvente'
    """
    if not text:
        return ""
        
    mapping = {
        'unu': '1', 'una': '1', 'un': '1',
        'doi': '2', 'doua': '2',
        'trei': '3',
        'patru': '4',
        'cinci': '5',
        'sase': '6',
        'sapte': '7',
        'opt': '8',
        'noua': '9',
        'zece': '10'
    }
    
    words = text.split()
    new_words = [mapping.get(w, w) for w in words]
    return " ".join(new_words)

@login_required
def dashboard_view(request):
    """Display user's notes and quizzes"""
    notes = Note.objects.filter(user=request.user)
    quizzes = Quiz.objects.filter(user=request.user)[:10]  # Recent 10 quizzes
    
    # Check if user has mistakes for recap
    from .models import Mistake
    has_mistakes = Mistake.objects.filter(user=request.user).exists()
    
    context = {
        'notes': notes,
        'quizzes': quizzes,
        'has_mistakes': has_mistakes,
    }
    return render(request, 'quiz/dashboard.html', context)

@login_required
def upload_note_view(request):
    """Upload and process a note file"""
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get uploaded file
            uploaded_file = request.FILES['file']
            
            # Read file content
            file_content = uploaded_file.read()
            
            # Create Note object with file in database
            note = Note.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                file_name=uploaded_file.name,
                file_content=file_content,
                file_type=uploaded_file.content_type,
                extracted_text=extract_text_from_file(uploaded_file)
            )
            
            messages.success(request, _('Note "%(title)s" uploaded successfully!') % {'title': note.title})
            return redirect('edit_note_text', note_id=note.id)
    else:
        form = NoteUploadForm()
    
    context = {'form': form}
    return render(request, 'quiz/upload_note.html', context)

@login_required
def edit_note_text_view(request, note_id):
    """Edit extracted text before generating quiz"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        form = NoteEditForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, _('Text updated successfully!'))
            return redirect('generate_quiz', note_id=note.id)
    else:
        form = NoteEditForm(instance=note)
    
    context = {
        'note': note,
        'form': form,
    }
    return render(request, 'quiz/edit_note_text.html', context)

@login_required
def generate_quiz_view(request, note_id):
    """Generate quiz with AI (mock for now)"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        from .forms import QuizGenerationForm
        from .ai_service import generate_quiz_with_ai
        
        form = QuizGenerationForm(request.POST)
        if form.is_valid():
            # Get form data
            question_count = form.cleaned_data['question_count']
            question_type = form.cleaned_data['question_type']
            difficulty = form.cleaned_data['difficulty']
            instant_feedback = form.cleaned_data['instant_feedback'] == 'True'
            
            # Create Quiz object
            quiz = Quiz.objects.create(
                note=note,
                user=request.user,
                question_count=question_count,
                question_type=question_type,
                difficulty=difficulty,
                instant_feedback=instant_feedback
            )
            
            # Get language based on mode
            mode = form.cleaned_data.get('mode')
            if mode == 'custom':
                 user_language = form.cleaned_data.get('target_language', 'ro')
            else:
                # For standard mode, keep existing behavior (use interface language)
                from django.utils import translation
                user_language = translation.get_language() or 'en'
            
            # Generate questions using AI (mock)
            questions_data = generate_quiz_with_ai(
                note.extracted_text,
                question_count,
                question_type,
                difficulty,
                user_language
            )
            
            # Create Question objects
            from .models import Question
            for q_data in questions_data:
                Question.objects.create(
                    quiz=quiz,
                    question_text=q_data['question_text'],
                    question_type=q_data['question_type'],
                    correct_answer=q_data['correct_answer'],
                    options=q_data.get('options', []),
                    explanation=q_data.get('explanation', ''),
                    order=q_data['order']
                )
            
            from django.utils.translation import gettext as _
            messages.success(request, _('Quiz generated with %(count)d questions!') % {'count': question_count})
            return redirect('take_quiz', quiz_id=quiz.id)
    else:
        from .forms import QuizGenerationForm
        form = QuizGenerationForm()
    
    context = {
        'note': note,
        'form': form,
    }
    return render(request, 'quiz/generate_quiz_options.html', context)


@login_required
def take_quiz_view(request, quiz_id):
    """Take a quiz with wizard-style interface"""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    questions = quiz.questions.all()
    
    if not questions:
        messages.error(request, _('This quiz has no questions.'))
        return redirect('dashboard')
    
    # Get or set current question index in session
    session_key = f'quiz_{quiz_id}_current'
    current_index = request.session.get(session_key, 0)
    
    # Handle quiz completion
    if current_index >= len(questions):
        # Clean up session
        if session_key in request.session:
            del request.session[session_key]
        return redirect('quiz_result', quiz_id=quiz.id)
    
    current_question = questions[current_index]
    
    # Check if already answered
    from .models import Answer
    existing_answer = Answer.objects.filter(
        question=current_question,
        user=request.user
    ).first()
    
    show_feedback = False
    is_correct = None
    
    if request.method == 'POST':
        user_answer = request.POST.get('answer', '')
        
        # Check if correct
        # Check if correct (ignoring case, whitespace, and diacritics)
        user_norm = normalize_answer(user_answer)
        correct_norm = normalize_answer(current_question.correct_answer)
        
        # 1. Exact match with simple normalization
        is_correct = user_norm == correct_norm
        
        if not is_correct:
             # 2. Normalize numbers (convert 'trei' to '3')
            user_nums = convert_text_numbers(user_norm)
            correct_nums = convert_text_numbers(correct_norm)
            
            if user_nums == correct_nums:
                is_correct = True
                
            # 3. Token containment check
            # If user answer is short (probably a number or key term) and is contained in the correct answer
            # Split into tokens/words to avoid partial matches like "3" in "123"
            if not is_correct:
                user_tokens = set(user_nums.split())
                correct_tokens = set(correct_nums.split())
                
                # If all user tokens are found in correct answer tokens
                # This covers: User="3", Correct="3 sequences"
                if user_tokens and user_tokens.issubset(correct_tokens):
                    is_correct = True
        
        # 4. Fuzzy match if not correct yet (allow 85% similarity)
        # Only apply fuzzy matching if the answer is long enough to avoid false positives on short words
        if not is_correct and len(correct_norm) > 4:
            similarity = SequenceMatcher(None, user_norm, correct_norm).ratio()
            if similarity >= 0.85:
                is_correct = True
        
        # Save answer
        Answer.objects.create(
            question=current_question,
            user=request.user,
            user_answer=user_answer,
            is_correct=is_correct
        )
        
        # Save mistake if incorrect
        if not is_correct:
            from .models import Mistake
            Mistake.objects.create(
                user=request.user,
                question=current_question,
                incorrect_answer=user_answer
            )
        
        # Show feedback if instant mode
        if quiz.instant_feedback:
            show_feedback = True
        else:
            # Move to next question immediately
            request.session[session_key] = current_index + 1
            request.session.modified = True
            return redirect('take_quiz', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'question': current_question,
        'current_index': current_index,
        'total_questions': len(questions),
        'progress_percentage': int((current_index / len(questions)) * 100),
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'existing_answer': existing_answer,
    }
    return render(request, 'quiz/take_quiz.html', context)

@login_required
def next_question_view(request, quiz_id):
    """Move to next question (used after instant feedback)"""
    session_key = f'quiz_{quiz_id}_current'
    current_index = request.session.get(session_key, 0)
    request.session[session_key] = current_index + 1
    request.session.modified = True
    return redirect('take_quiz', quiz_id=quiz_id)


@login_required
def quiz_result_view(request, quiz_id):
    """Show quiz results with detailed review"""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    questions = quiz.questions.all()
    
    # Get all answers for this quiz
    from .models import Answer
    answers = Answer.objects.filter(
        question__quiz=quiz,
        user=request.user
    ).select_related('question')
    
    # Build a dict of question_id -> answer
    answer_dict = {answer.question_id: answer for answer in answers}
    
    # Build review data
    review_data = []
    for question in questions:
        answer = answer_dict.get(question.id)
        review_data.append({
            'question': question,
            'answer': answer,
        })
    
    correct, total = quiz.get_score()
    percentage = int((correct / total * 100)) if total > 0 else 0
    
    context = {
        'quiz': quiz,
        'review_data': review_data,
        'correct': correct,
        'total': total,
        'percentage': percentage,
    }
    return render(request, 'quiz/quiz_result.html', context)


@login_required
def recap_quiz_view(request):
    """Generate recap quiz from all user's mistakes"""
    from .models import Mistake, Question
    
    # Get all unique questions from mistakes
    mistake_questions = Mistake.objects.filter(
        user=request.user
    ).values_list('question_id', flat=True).distinct()
    
    if not mistake_questions:
        messages.info(request, _('You have no mistakes to review yet. Complete some quizzes first!'))
        return redirect('dashboard')
    
    # Get the questions
    questions = Question.objects.filter(id__in=mistake_questions)
    
    if not questions.exists():
        messages.info(request, _('No questions found for recap.'))
        return redirect('dashboard')
    
    # Create a recap quiz
    # Use the first question's quiz's note as reference
    first_question = questions.first()
    note = first_question.quiz.note
    
    # Create Quiz object
    quiz = Quiz.objects.create(
        note=note,
        user=request.user,
        question_count=questions.count(),
        question_type='mixed',
        difficulty='mixed',
        instant_feedback=False,  # Default to final feedback for recap
        is_recap=True
    )
    
    # Copy questions to new quiz
    for order, original_question in enumerate(questions, start=1):
        Question.objects.create(
            quiz=quiz,
            question_text=original_question.question_text,
            question_type=original_question.question_type,
            correct_answer=original_question.correct_answer,
            options=original_question.options,
            explanation=original_question.explanation,
            order=order
        )
    
    messages.success(request, _('Recap quiz generated with %(count)d questions from your mistakes!') % {'count': questions.count()})
    return redirect('take_quiz', quiz_id=quiz.id)


@login_required
def assistant_chat_view(request):
    """Handle virtual assistant chat requests"""
    if request.method == 'POST':
        import json
        from django.http import JsonResponse
        from .ai_service import get_ai_explanation
        from .models import Question
        from django.utils import translation
        
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            user_query = data.get('query')
            
            question = get_object_or_404(Question, id=question_id)
            user_language = translation.get_language() or 'ro'
            
            explanation = get_ai_explanation(
                question.question_text,
                question.correct_answer,
                user_query,
                user_language
            )
            
            return JsonResponse({'explanation': explanation})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return redirect('dashboard')

