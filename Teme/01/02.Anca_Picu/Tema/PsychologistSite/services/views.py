from django.shortcuts import render

# Create your views here.

def services_view(request):
	context = {}
	return render(request, 'services.html', context)
