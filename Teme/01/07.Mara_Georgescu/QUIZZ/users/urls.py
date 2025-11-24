from django.urls import path
from .views import logout_view
from .views import login_view
from .views import register_view

urlpatterns = [

	path("register/", register_view, name="register"),
	path("login/", login_view, name="login"),
	path("logout/", logout_view, name="logout"),
]
