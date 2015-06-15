from unittest import TestCase

from ai.example.society import create_society


class TestSociety(TestCase):
    def test_create_society(self):
        seed_generation_size = 10
        number_of_generations = 3
        children_per_parents = range(1, 2)
        agents = create_society(
            seed_generation_size=seed_generation_size,
            number_of_generations=number_of_generations,
            children_per_parents=children_per_parents)
        self.assertIsInstance(agents, list)
