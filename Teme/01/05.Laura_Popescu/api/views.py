from django.shortcuts import render

# Create your views here.

def get_birthdates_view(request):
	context = {}
	return render(request, 'None.html', context)
