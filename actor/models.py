from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _


class GenderTypes(models.TextChoices):
    """Gender used for actors."""

    UNKNOWN = "unknown", _("Unknown")
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class Specie(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, db_index=True, default=uuid4)
    name = models.CharField(_("Name"), max_length=50)
    classification = models.CharField(_("Classification"), max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Specie")
        verbose_name_plural = _("Species")
        ordering = ("name",)


class Actor(models.Model):
    """Movie stars/actors."""

    id = models.UUIDField(_("ID"), primary_key=True, db_index=True, default=uuid4)
    name = models.CharField(_("Fullname"), max_length=200)
    gender = models.CharField(_("Gender"), max_length=7, choices=GenderTypes.choices, default=GenderTypes.UNKNOWN)
    age = models.CharField(_("Age"), max_length=20, default="Unspecified")
    eye_color = models.CharField(_("Eye color"), max_length=20, default="Unspecified")
    hair_color = models.CharField(_("Hair color"), max_length=20, default="Unspecified")
    specie = models.ForeignKey(Specie, verbose_name=_("Specie"), on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")
        ordering = ("name",)
