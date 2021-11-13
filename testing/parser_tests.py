
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import plyparser
import datetime


class TestDeclarations(unittest.TestCase):

    def test_integers_declaration(self):
        print('\n--------INTEGERS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['int a;']), 'a')
        self.assertEqual(plyparser.test_tokens(['int b = 3;']) , 3)
        self.assertEqual(plyparser.test_tokens(['int b = 3.0;']), 3.0)
        self.assertEqual(plyparser.test_tokens(['int c']) , None)
        self.assertEqual(plyparser.test_tokens(['int $$$;']), None)
        self.assertEqual(plyparser.test_tokens(['int _a;']), '_a')
        self.assertEqual(plyparser.test_tokens(['int a = 123124124']) , None)


    def test_floats_declaration(self):
        print('\n--------FLOATS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['float a;']), 'a')
        self.assertEqual(plyparser.test_tokens(['float b = 3;']), 3.0)
        self.assertEqual(plyparser.test_tokens(['float d = 0.0;']), 0.0)
        self.assertEqual(plyparser.test_tokens(['float c']), None)
        self.assertEqual(plyparser.test_tokens(['float $$$;']), None)
        self.assertEqual(plyparser.test_tokens(['float _a;']), '_a')
        self.assertEqual(plyparser.test_tokens(['float a = 123124124']), None)


    def test_strings_declaration(self):
        print('\n--------STRINGS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['string a;']), 'a')
        self.assertEqual(plyparser.test_tokens(['string b = 3;']), None)
        self.assertEqual(plyparser.test_tokens(['string d = 0.0;']), None)
        self.assertEqual(plyparser.test_tokens(['string c']), None)
        self.assertEqual(plyparser.test_tokens(['string $$$;']), None)
        self.assertEqual(plyparser.test_tokens(['string _a;']), '_a')
        self.assertEqual(plyparser.test_tokens(['string a = "123124124";']), '123124124')
        self.assertEqual(plyparser.test_tokens(['string a = "hola";']), 'hola')
        self.assertEqual(plyparser.test_tokens(['string a = "not"']), None)
        self.assertEqual(plyparser.test_tokens(['string a = "if else while for + - ";']), 'if else while for + - ')
        self.assertEqual(plyparser.test_tokens(['string a = "";']), '')
        self.assertEqual(plyparser.test_tokens(['string a = "  ";']), '  ')
        self.assertEqual(plyparser.test_tokens(['string a = "|?¡!#$&/(==?";']), '|?¡!#$&/(==?')
        self.assertEqual(plyparser.test_tokens(['string a = "=+-*/^><(){};";']), '=+-*/^><(){};')
        self.assertEqual(plyparser.test_tokens(['string a = "\\\'";']), "'")
        self.assertEqual(plyparser.test_tokens(['string a = "\\\"";']), '"')
        self.assertEqual(plyparser.test_tokens(['string a = \'|?¡!#$&/(==?\';']), '|?¡!#$&/(==?')
        self.assertEqual(plyparser.test_tokens(['string a = \'=+-*/^><(){};\';']), '=+-*/^><(){};')
        self.assertEqual(plyparser.test_tokens(['string a = \'\\\'\';']), "'")
        self.assertEqual(plyparser.test_tokens(['string a = \'\\\"\';']), '"')
        
    
    def test_strings_concatenation(self):
        print('\n--------STRINGS CONCATENATION--------')
        self.assertEqual(plyparser.test_tokens(['string a = \'\\\"\' + \'\\\"\';']), '""')
        self.assertEqual(plyparser.test_tokens(['string a = \'\\\'\' + \'\\\"\';']), "'\"")


    def test_booleans_declaration(self):
        print('\n--------BOOLEANS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['boolean a;']), 'a')
        self.assertEqual(plyparser.test_tokens(['boolean b = 3;']), None)
        self.assertEqual(plyparser.test_tokens(['boolean d = 0.0;']), None)
        self.assertEqual(plyparser.test_tokens(['boolean c']), None)
        self.assertEqual(plyparser.test_tokens(['boolean $$$;']), None)
        self.assertEqual(plyparser.test_tokens(['boolean _a;']), '_a')
        self.assertEqual(plyparser.test_tokens(['boolean a = "123124124";']), None)
        self.assertEqual(plyparser.test_tokens(['boolean c = 0;']), None)
        self.assertEqual(plyparser.test_tokens(['boolean oas = true;']), True)
        self.assertEqual(plyparser.test_tokens(['boolean oas = false;']), False)
        self.assertEqual(plyparser.test_tokens(['boolean oas = true']), None)
        self.assertEqual(plyparser.test_tokens(['boolean oas = false']), None)

    def test_comparisons_number_as_declaration(self):
        print('\n--------COMPARISONS OF NUMBER DECLARATION--------')
        # Integers
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 == 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 != 1);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 > 123);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean b = (1 < 123);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 >= 2);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean b = (1 <= 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 >= 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 == true);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (0 == false);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (2 == true);']), False)
        # Floating and Integers
        self.assertEqual(plyparser.test_tokens(['boolean a = (1.0 == 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 != 1.0);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1.0 > 123.0);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean b = (1.0 < 123.0);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 >= 2.0);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean b = (1 <= 1.0);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1.0 >= 1);']), True)

    def test_comparisons_string_as_declaration(self):
        print('\n--------COMPARISONS OF STRING DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['boolean a = ("1" == "1");']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("1 " == "1");']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("1 " != "1");']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("hola" == "hola");']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("12" > "1");']), None)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("1" < "12");']), None)
        self.assertEqual(plyparser.test_tokens(['boolean b = ("1" <= "2");']), None)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("1" >= "0");']), None)
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == "1");']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("trues" == true);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("true" == true);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("" == true);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = ("true" == 123);']), None)
        self.assertEqual(plyparser.test_tokens(['boolean a = (123 == "123");']), None)

    def test_comparisons_boolean_as_declaration(self):
        print('\n--------COMPARISONS OF BOOLEAN DECLARATION--------')
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (false == 123123);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = (false == 0);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == true);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (false != true);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (false != false);']), False)
        

    def test_comparisons_nested(self):
        print('\n--------COMPARISONS NESTED--------')
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == (1 == 1));']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ((1 == 1) == true);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ((1 != 1) == true);']), False)
        self.assertEqual(plyparser.test_tokens(['boolean a = (1 == (1 == 1));']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = ((false) == true);']), False)

    def test_number_block_operations(self):
        print('\n--------PARENTHESIS OPERATIONS--------')
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == (12 / 12));']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == (4 / 2) - 1);']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == ((4 / 2) - (12 / 12)));']), True)
        self.assertEqual(plyparser.test_tokens(['boolean a = (true == ((2 / 2) - (12 / 12)));']), False)
        self.assertEqual(plyparser.test_tokens(['int a = ((40 / 2) - (12 / 12));']), 19.0)
        self.assertEqual(plyparser.test_tokens(['int a = (32 -(44 - 10 * (2*2)) / 4);']), 31)


if __name__ == '__main__':
    log_file = 'parser_tests.log'
    sys.stdout = open(log_file, 'a')
    print('Last time tested:\n' + str(datetime.datetime.now()) + '\n')
    unittest.main()
    sys.stdout.close()
    sys.stdout = sys.__stdout__
       
