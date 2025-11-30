from django.urls import path
from .views import get_birthdates_view

urlpatterns = [

	path("birthdates/", get_birthdates_view),
]
