# This script can be used to automatically check the assignments of students
import py
import os
import sys
import argparse
verbose = True

# List of assignment names and achievable points
test_list = [("41"),
             ("42"),
             ("43"),
             ("44"),            
             ("45")
]

def run_test(name):
    test_file =  name+"_test" + ".py"
    if not os.path.isfile(test_file):
        print "Test file '{0}' does not exist.".format(test_file)
        exit(1)
    if verbose:
        return py.test.cmdline.main(["-s", test_file])
    else:
        return py.test.cmdline.main(["-q", test_file])

def run_all_tests():
    summary=''
    for test in test_list:
        exit_code = run_test(test)
        if exit_code == 0:
            print "Test {0} passed\n".format(test)
            summary += "Test {0} passed\n".format(test)
        else:
            print "Test {0} failed\n".format(test)
            summary += "Test {0} failed\n".format(test)
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tests assignemnts.')
    parser.add_argument('-s', '--silent', action='store_false',
                        help='Surpress most output')
    args = parser.parse_args()
    verbose = args.silent

    summary = run_all_tests()
    print "== Summary ==\n", summary
