from unittest import TestCase

from ai.name_gen.new_names import generate_name


class TestGenerateNames(TestCase):
    def test_generate_names(self):
        """Test that the generate_names() interface behaves as expected."""
        male_name = generate_name("male")
        self.assertIsInstance(male_name, basestring)

        female_name = generate_name("female")
        self.assertIsInstance(female_name, basestring)

    def test_arthurian_names(self):
        male_name = generate_name("male", origin="arthurian")
        self.assertIsInstance(male_name, basestring)

        female_name = generate_name("female", origin="arthurian")
        self.assertIsInstance(female_name, basestring)

    def test_welsh_names(self):
        male_name = generate_name("male", origin="welsh")
        self.assertIsInstance(male_name, basestring)

        female_name = generate_name("female", origin="welsh")
        self.assertIsInstance(female_name, basestring)
