from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Room, Topic, Message
from django.utils.html import format_html

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'is_staff', 'is_superuser', 'avatar_preview')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'avatar', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" style="border-radius:50%;" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = 'Avatar'

# Register models
admin.site.register(User, CustomUserAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
admin.site.register(Room, RoomAdmin)
admin.site.register(Topic)
admin.site.register(Message)
