from django.shortcuts import render

# Create your views here.

def add_birthdate_view(request):
	context = {}
	return render(request, 'add_birthdate.html.html', context)

def list_birthdates_view(request):
	context = {}
	return render(request, 'list_birthdates.html.html', context)

def edit_birthdate_view(request):
	context = {}
	return render(request, 'edit_birthdate.html.html', context)

def delete_birthdate_view(request):
	context = {}
	return render(request, 'delete_birthdate.html.html', context)

def details_birthdate_view(request):
	context = {}
	return render(request, 'detail_birthdate.html.html', context)
