
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import plyparser


class TestDeclarations(unittest.TestCase):
    log_file = 'parser_tests.log'
    def test_integers(self):
        sys.stdout = open(self.log_file, 'w')
        print('\n####TESTING INTEGERS####')
        self.assertEqual(plyparser.test_input(['int a;']), 'a')
        self.assertEqual(plyparser.test_input(['int b = 3;']) , '3')
        self.assertEqual(plyparser.test_input(['int c']) , None)
        self.assertEqual(plyparser.test_input(['int $$$;']), None)
        self.assertEqual(plyparser.test_input(['int _a;']), '_a')
        self.assertEqual(plyparser.test_input(['int a = 123124124']) , None)
        sys.stdout.close()
        sys.stdout = sys.__stdout__


unittest.main()
