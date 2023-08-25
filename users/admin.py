from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users import models


class CustomUserAdmin(UserAdmin):
    ordering = ("-id",)
    search_fields = ("email",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = ("id", "email", "is_active")
    list_display_links = ("id", "email")
    fieldsets = (
        ("Login Info", {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
    )


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.EmployeeInformation)
