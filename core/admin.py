from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, ArtImage, BlogPost


admin.site.site_header = "ArtFlght CMS"
admin.site.site_title = "ArtFlght Admin"
admin.site.index_title = "Welcome to the ArtFlght Admin Dashboard"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "username", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("bio", "avatar")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")}
        ),
    )


@admin.register(ArtImage)
class ArtImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "caption", "uploaded_at", "updated_at")
    search_fields = ("caption", "user__username")
    list_filter = ("uploaded_at",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "slug", "created_at", "updated_at")
    search_fields = ("title", "author__username", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
    list_filter = ("created_at", "updated_at")