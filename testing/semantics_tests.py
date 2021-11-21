import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import datetime
import unittest
import plysemantics

class ScopeTests(unittest.TestCase):

    def test_declarations(self):
        self.assertEqual(plysemantics.test_input('int a = 0;'), 'good')


if __name__ == '__main__':
    log_file = 'semantics_tests.log'
    sys.stdout = open(log_file, 'w')
    print('Last time tested:\n' + str(datetime.datetime.now()) + '\n')
    unittest.main()
    sys.stdout.close()
    sys.stdout = sys.__stdout__
