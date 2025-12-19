from django.urls import path
from .views import testimonials_view

urlpatterns = [

	path("testimoniale", testimonials_view),
]
