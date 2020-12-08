import logging
from uuid import uuid4

from django.test import TestCase

from actor.models import Actor, GenderTypes, Specie
from movie.apps import MovieConfig
from movie.models import Movie
from movie.tasks import sync_actors, sync_movies
from movie.utils import import_actor_from_data, import_movie_from_data


class ActorTestCase(TestCase):
    movie_name = "Who is Doctor?"
    director_name = "Graeme Harper"

    def setUp(self):
        super().setUp()
        human_specie = Specie.objects.create(id=uuid4(), name="Human", classification="Mammal")
        self.first_actor = Actor.objects.create(name="Matt Smith", specie=human_specie)
        self.second_actor = Actor.objects.create(name="Peter Capaldi", specie=human_specie)

    def test_apps(self):
        self.assertEqual(MovieConfig.name, "movie")

    def test_movie_model(self):
        movie_id = uuid4()
        movie = Movie.objects.create(
            id=movie_id,
            title=self.movie_name,
            release_year=2005,
            rt_score=100,
            director=self.director_name,
        )
        self.assertEqual(str(movie), self.movie_name)
        movie.actors.add(self.first_actor, self.second_actor)
        self.assertEqual(movie.total_actors, 2)
        self.assertTrue(Movie.objects.filter(id=movie_id).exists())

    def test_default_values(self):
        logging.disable(logging.CRITICAL)
        movie = Movie.objects.create(title=self.movie_name + " 2")
        self.assertEqual(movie.rt_score, 0)
        movie = import_movie_from_data({"id": uuid4(), "title": "Default 1", "rt_score": 500})
        self.assertEqual(movie.rt_score, 100)
        movie = import_movie_from_data({"id": uuid4(), "title": "Default 1", "rt_score": -10})
        self.assertEqual(movie.rt_score, 0)

    def test_sync_tasks(self):
        logging.disable(logging.CRITICAL)

        with self.settings(CELERY_TASK_ALWAYS_EAGER=True):
            sync_movies.delay()

        self.assertTrue(Movie.objects.count() > 5)
        self.assertTrue(Actor.objects.count() > 5)
        self.assertTrue(Movie.objects.filter(actors__isnull=False).distinct().count() > 5)

        # test calling twice
        total_movies = Movie.objects.count()

        with self.settings(CELERY_TASK_ALWAYS_EAGER=True):
            sync_movies.delay()

        self.assertEqual(Movie.objects.count(), total_movies)

        # test for non-existing movie
        Movie.objects.filter(actors__isnull=False).delete()
        # should continue after raising Movie.DoesNotExist error
        sync_actors.delay()

    def test_movie_import_function(self):
        logging.disable(logging.CRITICAL)
        self.assertIsNone(import_movie_from_data({"id": uuid4()}))
        self.assertIsNotNone(import_movie_from_data({"id": uuid4(), "title": "Import 1"}))
        # test incorrect release date and rt score values
        movie = import_movie_from_data(
            {"id": uuid4(), "title": "Import 2", "release_date": "not_int", "rt_score": "not_int"}
        )
        self.assertIsNone(movie.release_year)
        self.assertEqual(movie.rt_score, 0)

    def test_actor_import_function(self):
        logging.disable(logging.CRITICAL)
        self.assertIsNone(import_actor_from_data({"id": uuid4()}))
        self.assertIsNotNone(import_actor_from_data({"id": uuid4(), "name": "IActor 1"}))
        actor = import_actor_from_data({"id": uuid4(), "name": "IActor 2", "gender": "Female"})
        self.assertEqual(actor.gender, GenderTypes.FEMALE)
        actor = import_actor_from_data({"id": uuid4(), "name": "IActor 3", "gender": "Male"})
        self.assertEqual(actor.gender, GenderTypes.MALE)
