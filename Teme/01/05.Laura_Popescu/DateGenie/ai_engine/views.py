from django.shortcuts import render

# Create your views here.

def analyze_birthdate_view(request):
	context = {}
	return render(request, 'analyze_birthdate.html.html', context)

def compatibility_view(request):
	context = {}
	return render(request, 'compatibility.html.html', context)
