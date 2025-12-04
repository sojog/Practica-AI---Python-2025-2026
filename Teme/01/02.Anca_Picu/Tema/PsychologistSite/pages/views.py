from django.shortcuts import render

# Create your views here.
def home_view(request):
	context = {}
	return render(request, 'pages/home.html', context)

def about_view(request):
	context = {}
	return render(request, 'about.html', context)

def contact_view(request):
	context = {}
	return render(request, 'contact.html', context)
