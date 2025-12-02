"""
URL configuration for QUIZZ project.
"""
from django.contrib import admin
from django.urls import path, include
from users.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('quiz/', include('quiz.urls')),
    path('users/', include('users.urls')),
    path('quiz/', include('quiz.urls')),
    path('ui-test/', include('ui_test.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', login_view, name='home'), # Root URL points to login
]
