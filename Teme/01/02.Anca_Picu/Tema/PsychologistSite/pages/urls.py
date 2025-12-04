from django.urls import path
from .views import contact_view
from .views import about_view

urlpatterns = [

	path("despre", about_view),
	path("contact", contact_view),
]
