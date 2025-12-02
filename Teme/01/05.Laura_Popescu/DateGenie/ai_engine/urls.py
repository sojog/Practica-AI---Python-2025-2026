from django.urls import path
from .views import compatibility_view
from .views import analyze_birthdate_view

urlpatterns = [

	path("analyze/<int:pk>/", analyze_birthdate_view),
	path("compatibility/", compatibility_view),
]
