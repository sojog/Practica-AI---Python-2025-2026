from django.urls import path
from .views import profile_dashboard_view

urlpatterns = [

	path("profile/", profile_dashboard_view),
]
