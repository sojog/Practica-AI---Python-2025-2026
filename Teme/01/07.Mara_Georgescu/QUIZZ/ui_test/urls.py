from django.urls import path
from .views import ui_test_view

urlpatterns = [

	path("ui-test/", ui_test_view, name="ui_test_view"),
]
