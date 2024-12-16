from unittest import TestCase
from task_1 import strict
import unittest

class TestResultFunction(TestCase):
    def setUp(self):
        # Чтобы self не мешал
        @strict
        def example_function(a: int, b: int) -> int:
            return a + b
         
        self.example_function = example_function
        

    def test_correct_arguments(self):
        result = self.example_function(5, 5)
        self.assertEqual(result, 10)

    def test_incorrect_argument_type(self):
        with self.assertRaises(TypeError) as context:
            self.example_function(10, '2')
        self.assertEqual(str(context.exception), 'b не соответствует типу!')

if __name__ == '__main__':
    unittest.main()