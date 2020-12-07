from uuid import uuid4

from django.test import TestCase

from actor.models import Actor, Specie
from movie.apps import MovieConfig
from movie.models import Movie
from django.utils import timezone


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
        movie = Movie.objects.create(title=self.movie_name + " 2")
        self.assertEqual(movie.release_year, timezone.now().year)
        self.assertEqual(movie.rt_score, 0)
