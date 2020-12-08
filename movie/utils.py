"""
Utils related to Movies used in Tasks.
"""
import logging
from typing import Optional

from actor.models import Actor, GenderTypes
from movie.models import Movie

logger = logging.getLogger("gtasks")


def id_from_uri(uri: str) -> str:
    """Get the item ID from URI address."""
    return uri.rstrip("/").split("/")[-1]


def import_movie_from_data(data: dict) -> Optional[Movie]:
    """Save the movie from the raw API data."""
    # check for required fields: id and title
    if not all(key in data for key in ("id", "title")):
        logger.error(f"Movie is missing required fields: {data}")
        return

    # initialize the model with the base values
    movie = Movie(id=data["id"], title=data["title"])

    # check and add additional fields
    # ignore missing and null values
    if data.get("description"):
        movie.description = data["description"]

    if data.get("director"):
        movie.director = data["director"][:200]  # limit to max allowed length in the model

    if data.get("producer"):
        movie.producer = data["producer"][:200]

    if data.get("release_date"):
        try:
            movie.release_year = int(data["release_date"])
        except (ValueError, TypeError):
            # ignore non-integer date values
            pass

    if data.get("rt_score"):
        try:
            movie.rt_score = int(data["rt_score"])
        except (ValueError, TypeError):
            # RT score has to be an integer
            pass

    # save and return
    movie.save()
    logger.info(f"Movie {movie.title} imported.")
    return movie


def import_actor_from_data(data: dict) -> Optional[Actor]:
    """Save the actor from the raw API data."""
    # check for required fields: id and title
    if not all(key in data for key in ("id", "name")):
        logger.error(f"Actor is missing required fields: {data}")
        return

    # initialize the model with the base values
    actor = Actor(id=data["id"], name=data["name"])

    # check and add additional fields
    # ignore missing and null values
    for key in ["age", "eye_color", "hair_color"]:
        if data.get(key):
            setattr(actor, key, data[key][:20])

    if data.get("gender"):
        if data["gender"] == "Male":
            actor.gender = GenderTypes.MALE
        elif data["gender"] == "Female":
            actor.gender = GenderTypes.FEMALE

    # save and return
    actor.save()
    logger.info(f"Actor {actor.name} imported.")
    return actor
