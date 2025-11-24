from django.shortcuts import render

# Create your views here.

def ui_test_view(request):
	context = {}
	return render(request, 'ui_test/ui_test.html', context)
