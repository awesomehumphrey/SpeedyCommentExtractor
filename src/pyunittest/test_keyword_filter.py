import unittest
import os
import inspect
import sys
# relative imports from parent directory ######################################
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
# relative import ends ########################################################
from keyword_filter import keyword_filter as filter
# import src.keyword_filter as filter

class test_keyword_filter(unittest.TestCase):

    def setUp(self):
        self.keyword_filter = filter("./file.csv")

    def test_open_csv_file(self):
        testcase = self.keyword_filter.get_all_lines()
        expected = [
            "test1",
            "test2",
            "test3"
        ]
        self.assertEqual(expected, testcase)

    def test_write_csv_file(self):
        self.keyword_filter.append_to_csv_file([{'line': 'poo poo', 'location': 'poo', 'language': 'poolang'}], "poo.csv")

    def test_get_synonym(self):
        testcase = self.keyword_filter.get_synonyms("choosing own goals")
        self.assertAlmostEqual(testcase, ["keep", "for how", "skip", "uncomment", "comment", "you may", "instead", "could be replaced", "avoid problems", "make sure", "run this", "see", "todo", "value", "wait until", "if so", "backup", "asap", "as soon as possible"])

def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(test_keyword_filter)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
