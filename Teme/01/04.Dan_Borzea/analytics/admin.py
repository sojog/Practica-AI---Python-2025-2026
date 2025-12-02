from django.contrib import admin
from .models import TourView, TourCompletion


@admin.register(TourView)
class TourViewAdmin(admin.ModelAdmin):
    """Admin pentru vizualizări tururi"""
    
    list_display = ['tour', 'user', 'session_id', 'viewed_at', 'ip_address']
    list_filter = ['viewed_at', 'tour']
    search_fields = ['tour__name', 'user__username', 'session_id', 'ip_address']
    readonly_fields = ['viewed_at']


@admin.register(TourCompletion)
class TourCompletionAdmin(admin.ModelAdmin):
    """Admin pentru completări tururi"""
    
    list_display = ['tour', 'user', 'completed_at', 'rating_given']
    list_filter = ['completed_at', 'rating_given']
    search_fields = ['tour__name', 'user__username']
    readonly_fields = ['completed_at']
