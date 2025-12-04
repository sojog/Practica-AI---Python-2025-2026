from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/new/', views.event_create, name='event_create'),
    path('event/<int:event_id>/guests/', views.guest_list, name='guest_list'),
    path('event/<int:event_id>/guests/add/', views.guest_add, name='guest_add'),
    path('event/<int:event_id>/generate/', views.generate_invitation, name='generate_invitation'),
    path('event/<int:event_id>/save/', views.save_invitation, name='save_invitation'),
    path('event/<int:event_id>/generate-image/', views.generate_invitation_image, name='generate_invitation_image'),
    path('invitation-image/<int:invitation_id>/', views.invitation_image_detail, name='invitation_image_detail'),
    path('invitation/<uuid:invitation_id>/', views.render_invitation, name='render_invitation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
