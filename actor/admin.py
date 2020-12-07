from django.contrib import admin

from actor.models import Actor, Specie


@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = ("name", "classification")
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "specie")
    list_filter = ("specie",)
    search_fields = ("name", "id")
    autocomplete_fields = ("specie",)
