import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import datetime
import unittest

class ScopeTests(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    log_file = 'scope_tests.log'
    sys.stdout = open(log_file, 'w')
    print('Last time tested:\n' + str(datetime.datetime.now()) + '\n')
    unittest.main()
    sys.stdout.close()
    sys.stdout = sys.__stdout__
