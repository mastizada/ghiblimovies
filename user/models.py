from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """Custom User Model."""

    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self) -> str:
        name = ("%s %s" % (self.first_name, self.last_name)).strip()
        if name:
            return name
        return self.username

    @property
    def created_at(self) -> datetime:
        return self.date_joined

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "auth_user"
        ordering = ("pk",)
        indexes = [models.Index(fields=["username"], name="user_username_idx")]
