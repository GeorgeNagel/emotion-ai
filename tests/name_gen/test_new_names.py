from unittest import TestCase

from ai.name_gen.new_names import generate_names


class TestGenerateNames(TestCase):
    def test_generate_names(self):
        """Test that the generate_names() interface behaves as expected."""
        male_name = generate_names("male", 1)
        self.assertEqual(len(male_name), 1)
        self.assertIsInstance(male_name[0], basestring)

        male_names = generate_names("male", 20)
        self.assertEqual(len(male_names), 20)

        male_name = generate_names("female", 1)
        self.assertEqual(len(male_name), 1)
        self.assertIsInstance(male_name[0], basestring)

        male_names = generate_names("female", 20)
        self.assertEqual(len(male_names), 20)
