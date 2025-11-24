from django.urls import path
from .views import recap_quiz_view
from .views import quiz_result_view
from .views import take_quiz_view
from .views import generate_quiz_view
from .views import edit_note_text_view
from .views import upload_note_view
from .views import dashboard_view

urlpatterns = [

	path("dashboard/", dashboard_view, name="dashboard"),
	path("upload/", upload_note_view, name="upload_note"),
	path("note/<int:note_id>/edit/", edit_note_text_view, name="edit_note_text"),
	path("note/<int:note_id>/generate/", generate_quiz_view, name="generate_quiz"),
	path("quiz/<int:quiz_id>/take/", take_quiz_view, name="take_quiz"),
	path("quiz/<int:quiz_id>/result/", quiz_result_view, name="quiz_result"),
	path("recap/", recap_quiz_view, name="recap_quiz"),
]
