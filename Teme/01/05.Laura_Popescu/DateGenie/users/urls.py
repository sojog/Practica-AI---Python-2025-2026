from django.urls import path
from .views import logout_view
from .views import login_view
from .views import register_view

urlpatterns = [

	path("register/", register_view),
	path("login/", login_view),
	path("logout/", logout_view),
]
