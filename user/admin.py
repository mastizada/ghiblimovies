from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (
            _("Account Info"),
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("username", "email"),
                    "groups",
                    "is_active",
                    ("is_staff", "is_superuser"),
                )
            },
        ),
        (_("Password"), {"fields": ("password",)}),
        (
            _("Stamps"),
            {
                "fields": (
                    ("date_joined", "updated_at"),
                    "last_login",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("pk", "username", "first_name", "last_name", "last_login")
    readonly_fields = ("updated_at", "date_joined", "last_login")
    search_fields = ("user__username", "user__email", "user__last_name")
