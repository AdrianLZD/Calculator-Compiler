import sys
import datetime
import parser_tests
import scope_tests
import unittest


if __name__ == '__main__':
    log_file = 'full_tests.log'
    sys.stdout = open(log_file, 'w')
    print('Last time tested:\n' + str(datetime.datetime.now()) + '\n')

    suite = unittest.TestLoader().loadTestsFromModule(parser_tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromModule(scope_tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

    sys.stdout.close()
    sys.stdout = sys.__stdout__
