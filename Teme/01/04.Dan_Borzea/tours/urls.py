from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('search/', views.search_tours, name='search'),
    path('<slug:slug>/', views.tour_detail, name='tour_detail'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('review/add/<int:tour_id>/', views.add_review, name='add_review'),
    path('favorite/toggle/<int:tour_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('comment/add/<int:tour_id>/', views.add_comment, name='add_comment'),
    path('download/<int:tour_id>/', views.download_tour, name='download_tour'),
]
