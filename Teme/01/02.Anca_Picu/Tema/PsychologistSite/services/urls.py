from django.urls import path
from .views import services_view

urlpatterns = [

	path("servicii", services_view),
]
