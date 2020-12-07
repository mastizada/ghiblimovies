from django.contrib import admin

from movie.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rt_score", "total_actors", "created_at")
    list_filter = ("created_at",)
    autocomplete_fields = ("actors",)
    search_fields = ("title",)
