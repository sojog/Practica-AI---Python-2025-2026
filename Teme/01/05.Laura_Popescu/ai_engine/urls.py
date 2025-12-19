from django.urls import path
from .views import analyze_birthdate_view, compatibility_dashboard_view, compatibility_result_view, get_compatibility_api_v2, get_gift_suggestions, ai_dashboard_view, gift_suggestions_page_view, smart_gifting_view, social_aura_dashboard_view, social_aura_view, get_social_aura

urlpatterns = [
    path("dashboard/", ai_dashboard_view, name="ai_dashboard"),
    path('analyze/', analyze_birthdate_view, name='analyze_birthdate'),
    path('compatibility/', compatibility_dashboard_view, name='compatibility_dashboard'),
    path('compatibility/result/', compatibility_result_view, name='compatibility_result'),
    path('compatibility/api/', get_compatibility_api_v2, name='get_compatibility_api'),
    path('suggestions/<int:pk>/', get_gift_suggestions, name='get_gift_suggestions'),
    path('gift-ideas/<int:pk>/', gift_suggestions_page_view, name='gift_suggestions_page'),
    path('smart-gifting/', smart_gifting_view, name='smart_gifting'),
    path('social-aura/', social_aura_dashboard_view, name='social_aura_dashboard'),
    path('social-aura/view/<int:pk>/', social_aura_view, name='social_aura_view'),
    path('social-aura/api/<int:pk>/', get_social_aura, name='get_social_aura'),
]
