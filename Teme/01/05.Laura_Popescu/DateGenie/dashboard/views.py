from django.shortcuts import render

# Create your views here.

def profile_dashboard_view(request):
	context = {}
	return render(request, 'profile.html.html', context)
