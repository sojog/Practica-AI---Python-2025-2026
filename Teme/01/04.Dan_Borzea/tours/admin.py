from django.contrib import admin
from .models import Tour, Location, LocationImage, Review, Favorite, Comment, OfflineContent


class LocationInline(admin.TabularInline):
    """Inline pentru locații în admin-ul tururilor"""
    model = Location
    extra = 1
    fields = ['name', 'latitude', 'longitude', 'order', 'duration_minutes']


class LocationImageInline(admin.TabularInline):
    """Inline pentru imagini în admin-ul locațiilor"""
    model = LocationImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    """Admin pentru tururi"""
    
    list_display = ['name', 'category', 'is_premium', 'price', 'difficulty', 'is_active', 'created_by', 'created_at']
    list_filter = ['category', 'is_premium', 'difficulty', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LocationInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informații de bază', {
            'fields': ('name', 'slug', 'description', 'cover_image')
        }),
        ('Detalii tur', {
            'fields': ('category', 'difficulty', 'duration')
        }),
        ('Premium', {
            'fields': ('is_premium', 'price')
        }),
        ('Meta', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin pentru locații"""
    
    list_display = ['name', 'tour', 'order', 'latitude', 'longitude', 'duration_minutes']
    list_filter = ['tour']
    search_fields = ['name', 'description']
    inlines = [LocationImageInline]


@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    """Admin pentru imagini locații"""
    
    list_display = ['location', 'caption', 'order']
    list_filter = ['location__tour']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin pentru review-uri"""
    
    list_display = ['user', 'tour', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'tour__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin pentru favorite"""
    
    list_display = ['user', 'tour', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'tour__name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin pentru comentarii"""
    
    list_display = ['user', 'tour', 'parent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'tour__name', 'content']


@admin.register(OfflineContent)
class OfflineContentAdmin(admin.ModelAdmin):
    """Admin pentru conținut offline"""
    
    list_display = ['user', 'tour', 'downloaded_at', 'expiry_date']
    list_filter = ['downloaded_at', 'expiry_date']
    search_fields = ['user__username', 'tour__name']
