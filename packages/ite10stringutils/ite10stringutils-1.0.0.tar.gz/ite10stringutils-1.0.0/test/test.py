# test_palindrome.py
import unittest
from src import utils
class TestExercise(unittest.TestCase):
    MESSAGE_FMT = 'Expected output is `{0}`, got `{1}`: `{2}`'
    def _test_all(self, func, cases):
        for input_, expect in cases:
            output = func(input_)
            msg = self.MESSAGE_FMT.format(expect, output, input_)
            self.assertEqual(output, expect, msg)
class TestPalindrome(TestExercise):
    def test_check_palindrome(self):
        cases = [('ana', True),
                 ('Civic', True),
                 ('Bach khoa Ha Noi', False),
                 ('', False),
                 ('P', False),
                 ('Able was I ere I saw Elba', True)]
        self._test_all(utils.check_palindrome, cases)
if __name__ == '__main__':
    unittest.main(verbosity=2)
