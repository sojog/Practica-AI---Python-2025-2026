from django.shortcuts import render

# Create your views here.

def dashboard_view(request):
	context = {}
	return render(request, 'dashboard.html', context)

def upload_note_view(request):
	context = {}
	return render(request, 'upload_note.html', context)

def edit_note_text_view(request):
	context = {}
	return render(request, 'edit_note_text.html', context)

def generate_quiz_view(request):
	context = {}
	return render(request, 'generate_quiz_options.html', context)

def take_quiz_view(request):
	context = {}
	return render(request, 'take_quiz.html', context)

def quiz_result_view(request):
	context = {}
	return render(request, 'quiz_result.html', context)

def recap_quiz_view(request):
	context = {}
	return render(request, 'recap_quiz.html', context)
