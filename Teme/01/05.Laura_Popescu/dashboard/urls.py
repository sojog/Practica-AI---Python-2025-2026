from django.urls import path
from .views import profile_dashboard_view, home_view

urlpatterns = [
    path("", home_view, name="home_view"),
	path("profile/", profile_dashboard_view, name="profile_dashboard"),
]
