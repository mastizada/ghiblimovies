from django.shortcuts import redirect, render

from movie.models import Movie


def redirect_from_homepage(request):
    return redirect("movies-homepage")


def movies_list_view(request):
    movies = Movie.objects.filter().order_by("-created_at").prefetch_related("actors")
    return render(request, "movies.html", context={"movies": movies})
