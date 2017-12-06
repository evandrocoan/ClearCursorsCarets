

import sys
import unittest

def run_unit_tests(unit_tests_to_run=[]):
    runner = unittest.TextTestRunner()

    classes = \
    [
        sys.modules["ClearCursorsCarets.tests.clear_cursors_carets_first_selection_unit_tests"].ClearCursorsCaretsFirstSelectionUnitTests,
        sys.modules["ClearCursorsCarets.tests.clear_cursors_carets_last_selection_unit_tests"].ClearCursorsCaretsLastSelectionUnitTests,
    ]

    if len( unit_tests_to_run ) < 1:

        # Comment all the tests names on this list, to run all Unit Tests
        unit_tests_to_run = \
        [
            # "test_semantic_line_wrap_line_starting_with_comment",
        ]

    runner.run( suite( classes, unit_tests_to_run ) )


def suite(classes, unit_tests_to_run):
    """
        Problem with sys.argv[1] when unittest module is in a script
        https://stackoverflow.com/questions/2812218/problem-with-sys-argv1-when-unittest-module-is-in-a-script

        Is there a way to loop through and execute all of the functions in a Python class?
        https://stackoverflow.com/questions/2597827/is-there-a-way-to-loop-through-and-execute-all-of-the-functions

        looping over all member variables of a class in python
        https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    """
    suite = unittest.TestSuite()
    unit_tests_to_run_count = len( unit_tests_to_run )

    for _class in classes:
        _object = _class()

        for function_name in dir( _object ):

            if function_name.lower().startswith( "test" ):

                if unit_tests_to_run_count > 0 \
                        and function_name not in unit_tests_to_run:

                    continue

                suite.addTest( _class( function_name ) )

    return suite


