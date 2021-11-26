
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import plyparser
import datetime
from ply.lex import LexError


class ParserTests(unittest.TestCase):

    def test_integers_declaration(self):
        print('\n--------INTEGERS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('int a;'), 'block|a|0|')
        self.assertEqual(plyparser.test_tokens('int b = 3;') , 'block|b|3|')
        self.assertEqual(plyparser.test_tokens('int b = ((((3))));'), 'block|b|3|')
        self.assertEqual(plyparser.test_tokens('int b = 3.0;'), 'block|b|3.0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'int c')
        self.assertRaises(LexError, plyparser.test_tokens, 'int $$$;')
        self.assertEqual(plyparser.test_tokens('int _a;'), 'block|_a|0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'int a = 123124124')
        self.assertEqual(plyparser.test_tokens('int a; int c;'), 'block|a|0|c|0|')
        self.assertEqual(plyparser.test_tokens('int a = 1; int c = 123;'), 'block|a|1|c|123|')
        self.assertEqual(plyparser.test_tokens('int a = -1;'), 'block|a|-1|')
        self.assertEqual(plyparser.test_tokens('int a = ------1;'), 'block|a|------1|')
        self.assertEqual(plyparser.test_tokens('int a = b;'), 'block|a|b|')
        

    def test_floats_declaration(self):
        print('\n--------FLOATS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('float a;'), 'block|a|0.0|')
        self.assertEqual(plyparser.test_tokens('float b = 3;'), 'block|b|3|')
        self.assertEqual(plyparser.test_tokens('float d = 0.0;'), 'block|d|0.0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'float c')
        self.assertRaises(LexError, plyparser.test_tokens, 'float $$$;')
        self.assertEqual(plyparser.test_tokens('float _a;'), 'block|_a|0.0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'float a = 123124124')
        self.assertEqual(plyparser.test_tokens('float a = c;'), 'block|a|c|')
        self.assertEqual(plyparser.test_tokens('float b = ((((3))));'), 'block|b|3|')


    def test_strings_declaration(self):
        print('\n--------STRINGS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('string a;'), 'block|a||')
        self.assertEqual(plyparser.test_tokens('string b = 3;'), 'block|b|3|')
        self.assertEqual(plyparser.test_tokens('string d = 0.0;'), 'block|d|0.0|')
        self.assertEqual(plyparser.test_tokens('string b = (3);'), 'block|b|3|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'string c')
        self.assertRaises(LexError, plyparser.test_tokens, 'string $$$;')
        self.assertRaises(LexError, plyparser.test_tokens, 'string a = "test;')
        self.assertRaises(LexError, plyparser.test_tokens, 'string b = \'test;')
        self.assertEqual(plyparser.test_tokens('string _a;'), 'block|_a||')
        self.assertEqual(plyparser.test_tokens('string a = "123124124";'), 'block|a|123124124|')
        self.assertEqual(plyparser.test_tokens('string a = "hola";'), 'block|a|hola|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'string a = "not"')
        self.assertEqual(plyparser.test_tokens('string a = "if else while for + - ";'), 'block|a|if else while for + - |')
        self.assertEqual(plyparser.test_tokens('string a = "";'), 'block|a||')
        self.assertEqual(plyparser.test_tokens('string a = "  ";'), 'block|a|  |')
        self.assertEqual(plyparser.test_tokens('string a = "|?¡!#$&/(==?";'), 'block|a||?¡!#$&/(==?|')
        self.assertEqual(plyparser.test_tokens('string a = "=+-*/^><(){};";'), 'block|a|=+-*/^><(){};|')
        self.assertEqual(plyparser.test_tokens('string a = "\\\'";'), "block|a|'|")
        self.assertEqual(plyparser.test_tokens('string a = "\\\"";'), 'block|a|"|')
        self.assertEqual(plyparser.test_tokens('string a = \'|?¡!#$&/(==?\';'), 'block|a||?¡!#$&/(==?|')
        self.assertEqual(plyparser.test_tokens('string a = \'=+-*/^><(){};\';'), 'block|a|=+-*/^><(){};|')
        self.assertEqual(plyparser.test_tokens('string a = "\\\\";'), 'block|a|\|')
        self.assertEqual(plyparser.test_tokens('string a = "\\\\\\\\";'), 'block|a|\\\\|')
        self.assertEqual(plyparser.test_tokens('string a = "\\\\\\\'";'), 'block|a|\\\'|')
        self.assertEqual(plyparser.test_tokens('string a = \'\\\'\';'), "block|a|'|")
        self.assertEqual(plyparser.test_tokens('string a = \'\\\"\';'), 'block|a|"|')
        self.assertEqual(plyparser.test_tokens('string a = c;'), 'block|a|c|')
        self.assertEqual(plyparser.test_tokens('string b = (((("3"))));'), 'block|b|3|')
        

    def test_booleans_declaration(self):
        print('\n--------BOOLEANS DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('boolean a;'), 'block|a|False|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean b = 3;')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean d = 0.0;')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean c')
        self.assertRaises(LexError, plyparser.test_tokens,'boolean $$$;')
        self.assertEqual(plyparser.test_tokens('boolean _a;'), 'block|_a|False|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = "123124124";')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean c = 0;')
        self.assertEqual(plyparser.test_tokens('boolean oas = true;'), 'block|oas|True|')
        self.assertEqual(plyparser.test_tokens('boolean oas = false;'), 'block|oas|False|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean oas = true')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean oas = false')
        self.assertEqual(plyparser.test_tokens('boolean oas = (false);'), 'block|oas|False|')
        self.assertEqual(plyparser.test_tokens('boolean oas = a;'), 'block|oas|a|')
        self.assertEqual(plyparser.test_tokens('boolean b = ((((true))));'), 'block|b|True|')


    def test_comparisons_number_as_declaration(self):
        print('\n--------COMPARISONS OF NUMBER DECLARATION--------')
        # Integers
        self.assertEqual(plyparser.test_tokens('boolean a = (1 == 12);'), 'block|a|==|1|12|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (13 != 1);'), 'block|a|!=|13|1|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = (1 > 123);'), 'block|a|>|1|123|') #False
        self.assertEqual(plyparser.test_tokens('boolean b = (1 < 123);'), 'block|b|<|1|123|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1 >= 2);'), 'block|a|>=|1|2|') #False
        self.assertEqual(plyparser.test_tokens('boolean b = (1 <= 1);'), 'block|b|<=|1|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1 >= 1);'), 'block|a|>=|1|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1.0 == true);'), 'block|a|==|1.0|True|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (0 == false);'), 'block|a|==|0|False|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (2 == true);'), 'block|a|==|2|True|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = (0 > false);'), 'block|a|>|0|False|') #True
        # Floating and Integers
        self.assertEqual(plyparser.test_tokens('boolean a = (1.0 == 1);'), 'block|a|==|1.0|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1 != 1.0);'), 'block|a|!=|1|1.0|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = (1.0 > 123.0);'), 'block|a|>|1.0|123.0|') #False
        self.assertEqual(plyparser.test_tokens('boolean b = (1.0 < 123.0);'), 'block|b|<|1.0|123.0|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1 >= 2.0);'), 'block|a|>=|1|2.0|') #False
        self.assertEqual(plyparser.test_tokens('boolean b = (1 <= 1.0);'), 'block|b|<=|1|1.0|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (1.0 >= 1);'), 'block|a|>=|1.0|1|') #True


    def test_comparisons_string_as_declaration(self):
        print('\n--------COMPARISONS OF STRING DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('boolean a = ("1" == "1");'), 'block|a|==|1|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = ("1 " == "1");'), 'block|a|==|1 |1|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("1 " != "1");'), 'block|a|!=|1 |1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = ("hola" == "hola");'), 'block|a|==|hola|hola|') #True
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("12" > "1");'), #None
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("12" => "1");'), #None
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("1" < "12");'), #None
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean b = ("1" <= "2");'), #None
        self.assertEqual(plyparser.test_tokens('boolean a = ("1" >= true);'), 'block|a|>=|1|True|') #None
        self.assertEqual(plyparser.test_tokens('boolean a = (true == "1");'), 'block|a|==|True|1|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("trues" == true);'), 'block|a|==|trues|True|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("true" == true);'), 'block|a|==|true|True|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("" == true);'), 'block|a|==||True|') #False
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("true" == 123);') 
        self.assertEqual(plyparser.test_tokens('boolean a = (123.0 != "123");'), 'block|a|!=|123.0|123|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("true" > 123);'), 'block|a|>|true|123|') #False 
        self.assertEqual(plyparser.test_tokens('boolean a = (123.0 < "123");'), 'block|a|<|123.0|123|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = ("true" >= 123);'), 'block|a|>=|true|123|') #False
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = (123.0 and "123");')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = \'(123.0 and "123")\';')


    def test_comparisons_boolean_as_declaration(self):
        print('\n--------COMPARISONS OF BOOLEAN DECLARATION--------')
        self.assertEqual(plyparser.test_tokens('boolean a = (true == 1);'), 'block|a|==|True|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (false == 123123);'), 'block|a|==|False|123123|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = (false == 0);'), 'block|a|==|False|0|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (true == true);'), 'block|a|==|True|True|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (false != true);'), 'block|a|!=|False|True|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (false != false);'), 'block|a|!=|False|False|') #False
        

    def test_comparisons_nested(self):
        print('\n--------COMPARISONS NESTED--------')
        self.assertEqual(plyparser.test_tokens('boolean a = (true == (1 == 1));'), 'block|a|==|True|==|1|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = ((1 == 1) == true);'), 'block|a|==|==|1|1|True|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = ((1 != 1) == true);'), 'block|a|==|!=|1|1|True|') #False
        self.assertEqual(plyparser.test_tokens('boolean a = (1 == (1 == 1));'), 'block|a|==|1|==|1|1|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = ((false) == true);'), 'block|a|==|False|True|') #False


    def test_basic_arithmetic(self):
        print('\n--------ARITHMETIC--------')
        self.assertEqual(plyparser.test_tokens('int a = 1 + 1;'), 'block|a|+|1|1|')
        self.assertEqual(plyparser.test_tokens('int a = 1.0 + 1.0;'), 'block|a|+|1.0|1.0|')
        self.assertEqual(plyparser.test_tokens("int a = 10 - 10 - 10 - 10 - 10;"), 'block|a|-|-|-|-|10|10|10|10|10|')
        self.assertEqual(plyparser.test_tokens("int a = 10 - -1;"), 'block|a|-|10|-1|')
        self.assertEqual(plyparser.test_tokens('int a = 1 / 2;'), 'block|a|/|1|2|')
        self.assertEqual(plyparser.test_tokens("int a = 1--1;"), 'block|a|-|1|-1|')
        self.assertEqual(plyparser.test_tokens("int a = 1-----1;"), 'block|a|-|1|----1|')
        self.assertEqual(plyparser.test_tokens("int a = 1---+-1;"), 'block|a|-|1|--+-1|')


    def test_number_block_operations(self):
        print('\n--------PARENTHESIS OPERATIONS--------')
        self.assertEqual(plyparser.test_tokens('boolean a = (true == (12 / 12));'), 'block|a|==|True|/|12|12|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (true == (4 / 2) - 1);'), 'block|a|==|True|-|/|4|2|1|') #True 
        self.assertEqual(plyparser.test_tokens('boolean a = (true == ((4 / 2) - (12 / 12)));'), 'block|a|==|True|-|/|4|2|/|12|12|') #True
        self.assertEqual(plyparser.test_tokens('boolean a = (true == ((2 / 2) - (12 / 12)));'), 'block|a|==|True|-|/|2|2|/|12|12|') #True
        self.assertEqual(plyparser.test_tokens('int a = ((40 / 2) - (12 / 12));'), 'block|a|-|/|40|2|/|12|12|') #19.0
        self.assertEqual(plyparser.test_tokens('int a = (32 -(- 1 - 44 - -2 -10 * (2*2)) / 4);'), 'block|a|-|32|/|-|-|-1|44|-|-2|*|10|*|2|2|4|')


    def test_string_concatenation(self):
        print('\n--------STRINGS CONCATENATION--------')
        self.assertEqual(plyparser.test_tokens('string a = "a" + "b";'), 'block|a|+|a|b|')
        self.assertEqual(plyparser.test_tokens('a = (a) + "b";'), 'block|a|+|a|b|')
        self.assertEqual(plyparser.test_tokens("string a = 'a' + 'b';"), 'block|a|+|a|b|')
        self.assertEqual(plyparser.test_tokens("string asd = 'a' + 'b' +'c' + 'd';"), 'block|asd|+|+|+|a|b|c|d|')
        self.assertEqual(plyparser.test_tokens('string a = "" + "";'), 'block|a|+|||')
        self.assertEqual(plyparser.test_tokens("string a = '' + '';"), 'block|a|+|||')
        self.assertEqual(plyparser.test_tokens('string a = "asd" + "1";'), 'block|a|+|asd|1|')
        self.assertEqual(plyparser.test_tokens("string a = 'asd' + (1);"), 'block|a|+|asd|1|')
        self.assertEqual(plyparser.test_tokens("string a = 'asd' + 1;"), 'block|a|+|asd|1|')
        self.assertEqual(plyparser.test_tokens('string a = "" + (1);'), 'block|a|+||1|')
        self.assertEqual(plyparser.test_tokens('string a = ""+(1);'), 'block|a|+||1|')
        self.assertEqual(plyparser.test_tokens('string a = ""+(1+2);'), 'block|a|+||+|1|2|')
        self.assertEqual(plyparser.test_tokens('string a = ""+ (1) +"asd";'), 'block|a|+|+||1|asd|')
        self.assertEqual(plyparser.test_tokens('string a = ""+ (2+4) +"asd";'), 'block|a|+|+||+|2|4|asd|')
        self.assertEqual(plyparser.test_tokens('string a = (1) + "test";'), 'block|a|+|1|test|')
        self.assertEqual(plyparser.test_tokens('string a = \'\\\"\' + \'\\\"\';'), 'block|a|+|"|"|')
        self.assertEqual(plyparser.test_tokens('string a = \'\\\'\' + \'\\\"\';'), "block|a|+|'|\"|")


    def test_andor_expressions(self):
        print('\n--------AND/OR EXPRESSIONS--------')
        self.assertEqual(plyparser.test_tokens('boolean a = true and false;'), 'block|a|and|True|False|')
        self.assertEqual(plyparser.test_tokens("boolean a = true or false;"), 'block|a|or|True|False|')
        self.assertEqual(plyparser.test_tokens('boolean a = (true and false) or (true or true);'), 'block|a|or|and|True|False|or|True|True|')
        self.assertEqual(plyparser.test_tokens('boolean a = (true and false) or (1);'), 'block|a|or|and|True|False|1|')
        self.assertEqual(plyparser.test_tokens('boolean a = 0 or 1.0;'), 'block|a|or|0|1.0|')
        self.assertEqual(plyparser.test_tokens('boolean a = (((0))) or (1);'), 'block|a|or|0|1|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = "as" or (1);')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("as") or "asd";')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = 1.0 or "asd";')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = ("as") or (1);')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'boolean a = (1) or (1)')
        self.assertEqual(plyparser.test_tokens('boolean a = 0.0 or true or false and 1;'), 'block|a|or|0.0|or|True|and|False|1|')


    def test_newlines(self):
        print('\n--------NEW LINES--------')
        self.assertEqual(plyparser.test_tokens('''
        int a = 0;
        '''), 'block|a|0|')
        self.assertEqual(plyparser.test_tokens('''


        int a = 0;

        int b = 0;


        '''), 'block|a|0|b|0|')
    

    def test_if_blocks(self):
        print('\n--------IF BLOCKS--------')
        self.assertEqual(plyparser.test_tokens('if (true) { int a;}'), 'block|if|cond|True|block|a|0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'if true { int a;}')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'if (true) }')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'if (true) { int a;')
        self.assertEqual(plyparser.test_tokens('if (true) { }'), 'block|if|cond|True|empty|')
        self.assertEqual(plyparser.test_tokens('if (true or false ) { int a;}'), 'block|if|cond|or|True|False|block|a|0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'if () { int a;}')
        self.assertEqual(plyparser.test_tokens('if (1) { int a;}'), 'block|if|cond|1|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if (1 + 2) { int a;}'), 'block|if|cond|+|1|2|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if (1 > 2) { int a;}'), 'block|if|cond|>|1|2|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if ("test") { int a;}'), 'block|if|cond|test|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if (((1))) { int a;}'), 'block|if|cond|1|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if (true or false ) { int a;}'), 'block|if|cond|or|True|False|block|a|0|')
        self.assertEqual(plyparser.test_tokens('if (((1)) or false) { int a;}'), 'block|if|cond|or|1|False|block|a|0|')


    def test_if_nestedblocks(self):
        print('\n--------NESTED IF BLOCKS--------')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { if (true) { int a;}}'),
            'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_if|P5_cond|P6_True|P6_block|P7_a|P8_0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 
            'if true { if true { int a;}}')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { if (true) {}}'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_if|P5_cond|P6_True|P6_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { if (true) { int a;} int b = 0;}'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_if|P5_cond|P6_True|P6_block|P7_a|P8_0|P4_b|P5_0|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { if (true) { int a;} } int b = 0;'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_if|P5_cond|P6_True|P6_block|P7_a|P8_0|P1_b|P2_0|')


    def test_if_else_blocks(self):
        print('\n--------IF ELSE BLOCKS--------')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { } else { }'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P2_else|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if (true) { int b; } else { int a; }'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_b|P5_0|P2_else|P3_block|P4_a|P5_0|')
        self.assertEqual(plyparser.test_tokens_parents('''
                                                        if (true) {
                                                            int a = 1;
                                                        } else { 
                                                            if (1){
                                                                int b = 2;
                                                            }else{
                                                                int c = 3;
                                                            }
                                                        }
                                                        int d = 4;
                                                       '''),
           'P0_block|P1_if|P2_cond|P3_True|P3_block|P4_a|P5_1|P2_else|P3_block|P4_if|P5_cond|P6_1|P6_block|P7_b|P8_2|P5_else|P6_block|P7_c|P8_3|P1_d|P2_4|')
        

    def test_if_elif_blocks(self):
        print('\n--------IF ELIF BLOCKS--------')
        self.assertEqual(plyparser.test_tokens_parents(
            'if(true){ }elif(true){ }'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P2_cond|P3_True|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if(true){ }elif(true){ }else{ }'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P2_cond|P3_True|P3_empty|P2_else|P3_empty|')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 
            'if(true){ }else{ }elif(true){ }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents,
            'if(true){ }elif{ }elif(true){ }')
        self.assertEqual(plyparser.test_tokens_parents(
            'if(true){ }elif(true){ }elif(true){ }'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P2_cond|P3_True|P3_empty|P2_cond|P3_True|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if(true){ }if(true){ }elif(true){}'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P1_if|P2_cond|P3_True|P3_empty|P2_cond|P3_True|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'if(true){ }elif(1 > 2){}'), 
            'P0_block|P1_if|P2_cond|P3_True|P3_empty|P2_cond|P3_>|P4_1|P4_2|P3_empty|')


    def test_while_blocks(self):
        print('\n--------WHILE BLOCKS--------')
        self.assertEqual(plyparser.test_tokens_parents('while(true){ int a = 0; }'), 'P0_block|P1_while|P2_cond|P3_True|P3_block|P4_a|P5_0|')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'while(){ int a = 0; }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'while(true)')
        self.assertEqual(plyparser.test_tokens_parents(
            'while(1 > 20){  }'), 
            'P0_block|P1_while|P2_cond|P3_>|P4_1|P4_20|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'while((1 + 20) > 2){  }'), 
            'P0_block|P1_while|P2_cond|P3_>|P4_+|P5_1|P5_20|P4_2|P3_empty|')
        self.assertEqual(plyparser.test_tokens_parents(
            'while(true){ }while(true){ }'), 
            'P0_block|P1_while|P2_cond|P3_True|P3_empty|P1_while|P2_cond|P3_True|P3_empty|')


    def test_for_blocks(self):
        print('\n--------FOR BLOCKS--------')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(int i = 0; i < 2; i++) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_i|P4_2|P2_empty|P2_+|P3_i|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(int i = 0; a < 2; i++) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_a|P4_2|P2_empty|P2_+|P3_i|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(int i = 0; a < 2; a++) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_a|P4_2|P2_empty|P2_+|P3_a|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(int i; a < 2; a++) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_a|P4_2|P2_empty|P2_+|P3_a|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(int i = 0; a < 2; a--) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_a|P4_2|P2_empty|P2_-|P3_a|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(float i = 0; a < 2; a--) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_a|P4_2|P2_empty|P2_-|P3_a|P3_1|')
        self.assertEqual(plyparser.test_tokens_parents(
            'for(i = 0; i<2 ;i++) { }'), 'P0_block|P1_for|P2_i|P3_0|P2_cond|P3_<|P4_i|P4_2|P2_empty|P2_+|P3_i|P3_1|')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for() { }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for(int i = 0;) { }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for(int i = 0; i< 2) { }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for(int i = 0; i++) { }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for(int i = 0; ;i++) { }')
        self.assertRaises(SyntaxError, plyparser.test_tokens_parents, 'for(float i = 0; i<2 ;i) { }')
        


    def test_print(self):
        print('\n--------PRINT STATEMENTS--------')
        self.assertEqual(plyparser.test_tokens('print(1);'), 'block|print|1|')
        self.assertEqual(plyparser.test_tokens('print(a);'), 'block|print|a|')
        self.assertEqual(plyparser.test_tokens('print("hola");'), 'block|print|hola|')
        self.assertEqual(plyparser.test_tokens('print(1.0);'), 'block|print|1.0|')
        self.assertEqual(plyparser.test_tokens('print(true);'), 'block|print|True|')
        self.assertEqual(plyparser.test_tokens('print(1 + 2);'), 'block|print|+|1|2|')
        self.assertEqual(plyparser.test_tokens('print((1) + "asd");'), 'block|print|+|1|asd|')
        self.assertEqual(plyparser.test_tokens('print("1" + "asd");'), 'block|print|+|1|asd|')
        self.assertEqual(plyparser.test_tokens('print((((1))) + "asd");'), 'block|print|+|1|asd|')
        self.assertEqual(plyparser.test_tokens('print("asd" + (2));'), 'block|print|+|asd|2|')
        self.assertEqual(plyparser.test_tokens('print(1 < 2);'), 'block|print|<|1|2|')
        self.assertEqual(plyparser.test_tokens('print(1 == 2);'), 'block|print|==|1|2|')
        self.assertRaises(SyntaxError, plyparser.test_tokens, 'print(1 = 2);')
        

    def test_id_assign(self):
        print('\n--------ID ASSIGNMENT--------')
        self.assertEqual(plyparser.test_tokens('a = 2;'), 'block|a|2|')
        self.assertEqual(plyparser.test_tokens('_a = 2;'), 'block|_a|2|')
        self.assertRaises(LexError, plyparser.test_tokens, '$$$ = 0;')
        self.assertEqual(plyparser.test_tokens('a = ((((2))));'), 'block|a|2|')
        self.assertEqual(plyparser.test_tokens('a = (2 + 2 * (3 * 4));'), 'block|a|+|2|*|2|*|3|4|')
        self.assertEqual(plyparser.test_tokens('a = true;'), 'block|a|True|')
        self.assertEqual(plyparser.test_tokens('a = true and false;'), 'block|a|and|True|False|')
        self.assertEqual(plyparser.test_tokens('a = (1 > 2);'), 'block|a|>|1|2|')
        self.assertEqual(plyparser.test_tokens('a = "true";'), 'block|a|true|')
        self.assertEqual(plyparser.test_tokens('a = "true" + "false";'), 'block|a|+|true|false|')
        self.assertEqual(plyparser.test_tokens('a = (1) + "asd";'), 'block|a|+|1|asd|')


if __name__ == '__main__':
    log_file = 'parser_tests.log'
    sys.stdout = open(log_file, 'w')
    print('Last time tested:\n' + str(datetime.datetime.now()) + '\n')
    unittest.main()
    sys.stdout.close()
    sys.stdout = sys.__stdout__
       
