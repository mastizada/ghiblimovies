from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from actor.models import Actor


def current_year() -> int:
    return timezone.now().year


class Movie(models.Model):
    """Movie/Film details."""

    id = models.UUIDField(_("ID"), primary_key=True, db_index=True, default=uuid4)
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    director = models.CharField(_("Director"), max_length=200, blank=True, null=True)
    producer = models.CharField(_("Producer"), max_length=200, blank=True, null=True)
    release_year = models.IntegerField(_("Release year"), default=current_year)
    rt_score = models.PositiveIntegerField(
        _("Tomatometer score"), validators=[MinValueValidator(0), MaxValueValidator(100)], default=0
    )
    actors = models.ManyToManyField(Actor, related_name="movies")
    # timestamp
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)

    @property
    def total_actors(self) -> int:
        return self.actors.count()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        # always provide latest added item
        ordering = ("-created_at",)
