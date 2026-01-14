from django.urls import path
from .views import details_birthdate_view
from .views import delete_birthdate_view
from .views import edit_birthdate_view
from .views import list_birthdates_view
from .views import add_birthdate_view

from .views import contacts_view

urlpatterns = [
	path("add/", add_birthdate_view, name="add_birthdate"),
	path("list/", list_birthdates_view, name="list_birthdates"),
    path("contacts/", contacts_view, name="contacts_view"),
	path("edit/<int:pk>/", edit_birthdate_view, name="edit_birthdate"),
	path("delete/<int:pk>/", delete_birthdate_view, name="delete_birthdate"),
	path("detail/<int:pk>/", details_birthdate_view, name="detail_birthdate"),
]
