from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from movie import views as movie_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movies/", movie_views.movies_list_view, name="movies-homepage"),
    path("", movie_views.redirect_from_homepage, name="homepage"),
]

if settings.DEBUG:
    # Enable serving static files in the Development environment over the gunicorn worker.
    urlpatterns += staticfiles_urlpatterns()  # pragma: no cover
