# apps/relationships/admin.py
from django.contrib import admin
from .models import User, UserRelationship

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender',  'is_verified', 'is_adult', 'created_at')
    search_fields = ('name', 'user_id')
    list_filter = ('gender', 'is_verified', 'is_adult')
    readonly_fields = ('user_id', 'created_at', 'updated_at')

@admin.register(UserRelationship)
class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_name', 'relationship_type', 'personality_type', 'is_active')
    list_filter = ('relationship_type', 'is_active')
    search_fields = ('user__name', 'ai_name', 'custom_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'ai_name', 'relationship_type', 'personality_type')
        }),
        ('Additional Details', {
            'fields': ('custom_name', 'bio', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )