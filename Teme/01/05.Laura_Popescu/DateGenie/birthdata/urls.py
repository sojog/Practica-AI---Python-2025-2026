from django.urls import path
from .views import details_birthdate_view
from .views import delete_birthdate_view
from .views import edit_birthdate_view
from .views import list_birthdates_view
from .views import add_birthdate_view

urlpatterns = [

	path("add/", add_birthdate_view),
	path("list/", list_birthdates_view),
	path("edit/<int:pk>/", edit_birthdate_view),
	path("delete/<int:pk>/", delete_birthdate_view),
	path("detail/<int:pk>/", details_birthdate_view),
]
