from uuid import uuid4

from django.test import TestCase

from actor.apps import ActorConfig
from actor.models import Actor, GenderTypes, Specie


class ActorTestCase(TestCase):
    actor_name = "Keir Dullea"

    def setUp(self):
        super().setUp()
        self.human_specie = Specie.objects.create(name="Human", classification="Mammal")
        self.dog_specie = Specie.objects.create(name="Dog", classification="Mammal")

    def test_apps(self):
        self.assertEqual(ActorConfig.name, "actor")

    def test_actor_model(self):
        actor_id = uuid4()
        Actor.objects.create(id=actor_id, name=self.actor_name, specie=self.human_specie)
        actor = Actor.objects.get(id=actor_id)
        self.assertEqual(actor.gender, GenderTypes.UNKNOWN)
        for field in ["age", "eye_color", "hair_color"]:
            self.assertEqual(getattr(actor, field), "Unspecified")
        self.assertEqual(actor.specie.id, self.human_specie.id)
        self.assertEqual(str(actor), self.actor_name)

    def test_specie_model(self):
        self.assertEqual(str(self.dog_specie), self.dog_specie.name)
