"""
Task to sync movies and actors from the Ghibli API.

API does not support pagination or ordering by date.

Updating existing movies is out-of-scope.

The films API will be checked every minute to make sure we always have newest movies.
The people API will be checked if a new movie is added.

Data from the API is small enough for importing directly.
For larger APIs, best way would be to download results in chunks and then import them from a local json file.
"""
import logging
from uuid import UUID

import requests
from django.conf import settings

from actor.models import Actor
from ghiblimovies.celery import app
from movie.models import Movie
from movie.utils import id_from_uri, import_actor_from_data, import_movie_from_data

logger = logging.getLogger("gtasks")


@app.task(name="sync_actors")
def sync_actors():
    """Sync actors from the API."""
    logger.info("Sync for actors started...")

    response = requests.get(settings.MOVIES_API_BASE + "people")
    actors = response.json()
    logger.debug("Received {count} actors from the API".format(count=len(actors)))

    new_actors = 0

    for actor_data in actors:
        # get actor model
        try:
            actor = Actor.objects.get(id=actor_data["id"])
        except Actor.DoesNotExist:
            actor = import_actor_from_data(actor_data)
            if not actor:
                # issue is logged directly in the import function
                continue  # pragma: no cover
            new_actors += 1

        # check movies
        for movie_uri in actor_data["films"]:
            try:
                movie = Movie.objects.get(id=id_from_uri(movie_uri))
            except Movie.DoesNotExist:
                continue
            # add actor to the movie
            movie.actors.add(actor)

    logger.info(f"{new_actors} new actors were imported.")


@app.task(name="sync_movies")
def sync_movies():
    """Sync movies from the API."""
    logger.info("Sync for movies started...")

    response = requests.get(settings.MOVIES_API_BASE + "films")
    movies = response.json()
    logger.debug("Received {count} movies from the API".format(count=len(movies)))

    # get id list of existing movies from DB
    # Alternate to that will be to use `exists` call for each movie ID (or in batch) for large datasets.
    existing_movies = Movie.objects.values_list("id", flat=True)
    new_movies = 0

    for movie in movies:
        if UUID(movie["id"]) in existing_movies:
            # ignore movies that already exist
            continue
        if import_movie_from_data(movie):
            new_movies += 1

    logger.info(f"{new_movies} new movies were imported.")

    if new_movies:
        # start to sync actors if a new movie is added
        sync_actors.delay()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **__):
    """
    Setup periodic tasks when instance starts.

    It is called directly by the celery-beat worker and saved in the Periodic Tasks model.
    """
    # call sync_movies every minute
    sender.add_periodic_task(60.0, sync_movies.s(), name="sync movies every minute")  # pragma: no cover
