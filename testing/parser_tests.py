
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import plyparser
import datetime


class TestDeclarations(unittest.TestCase):
    log_file = 'parser_tests.log'
    "Cleans log file before appending testing logs"
    with open(log_file, 'w') as f:
        f.write('Last time tested:\n' + str(datetime.datetime.now()) + '\n')

    def test_integers(self):
        sys.stdout = open(self.log_file, 'a')
        print('\n--------TESTING INTEGERS--------')
        self.assertEqual(plyparser.test_input(['int a;']), 'a')
        self.assertEqual(plyparser.test_input(['int b = 3;']) , '3')
        self.assertEqual(plyparser.test_input(['int c']) , None)
        self.assertEqual(plyparser.test_input(['int $$$;']), None)
        self.assertEqual(plyparser.test_input(['int _a;']), '_a')
        self.assertEqual(plyparser.test_input(['int a = 123124124']) , None)
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    def test_floats(self):
        sys.stdout = open(self.log_file, 'a')
        print('\n--------TESTING FLOATS--------')
        self.assertEqual(plyparser.test_input(['float a;']), 'a')
        self.assertEqual(plyparser.test_input(['float b = 3;']), '3')
        self.assertEqual(plyparser.test_input(['float d = 0.0;']), '0.0')
        self.assertEqual(plyparser.test_input(['float c']), None)
        self.assertEqual(plyparser.test_input(['float $$$;']), None)
        self.assertEqual(plyparser.test_input(['float _a;']), '_a')
        self.assertEqual(plyparser.test_input(['float a = 123124124']), None)
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    def test_strings(self):
        sys.stdout = open(self.log_file, 'a')
        print('\n--------TESTING STRINGS--------')
        self.assertEqual(plyparser.test_input(['string a;']), 'a')
        self.assertEqual(plyparser.test_input(['string b = 3;']), None)
        self.assertEqual(plyparser.test_input(['string d = 0.0;']), None)
        self.assertEqual(plyparser.test_input(['string c']), None)
        self.assertEqual(plyparser.test_input(['string $$$;']), None)
        self.assertEqual(plyparser.test_input(['string _a;']), '_a')
        self.assertEqual(plyparser.test_input(['string a = "123124124";']), '123124124')
        self.assertEqual(plyparser.test_input(['string a = "hola";']), 'hola')
        self.assertEqual(plyparser.test_input(['string a = "not"']), None)
        self.assertEqual(plyparser.test_input(['string a = "if else while for + - ";']), 'if else while for + - ')
        self.assertEqual(plyparser.test_input(['string a = "";']), '')
        self.assertEqual(plyparser.test_input(['string a = "  ";']), '  ')
        self.assertEqual(plyparser.test_input(['string a = "|?¡!#$&/(==?";']), '|?¡!#$&/(==?')
        self.assertEqual(plyparser.test_input(['string a = "=+-*/^><(){};";']), '=+-*/^><(){};')
        self.assertEqual(plyparser.test_input(['string a = "\\\'";']), "'")
        self.assertEqual(plyparser.test_input(['string a = "\\\"";']), '"')
        self.assertEqual(plyparser.test_input(['string a = \'|?¡!#$&/(==?\';']), '|?¡!#$&/(==?')
        self.assertEqual(plyparser.test_input(['string a = \'=+-*/^><(){};\';']), '=+-*/^><(){};')
        self.assertEqual(plyparser.test_input(['string a = \'\\\'\';']), "'")
        self.assertEqual(plyparser.test_input(['string a = \'\\\"\';']), '"')
        '"'
        sys.stdout.close()
        sys.stdout = sys.__stdout__


unittest.main()
