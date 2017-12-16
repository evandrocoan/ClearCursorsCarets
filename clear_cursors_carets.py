
"""
See/read the README.MD file.
"""


import os

import sublime
import sublime_plugin


last_expansions = []

class SingleSelectionFirstCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection First...' )
        # print( "SingleSelectionFirst, last_expansions_length: " + str( len( last_expansions ) ) )
        view       = self.view
        selections = view.sel()

        def run_single_selection():
            view.run_command( "single_selection" )

        # If the selection changed as when using the arrow keys, we cannot use `first_expansion`
        if len( last_expansions ):
            first = last_expansions[0]
            # print( "SingleSelectionFirst, Selecting first: " + str( first ) )

            if first not in selections:
                run_single_selection()

            else:
                selections.clear()
                selections.add( first )
                view.show( first )

        else:
            view.run_command( "single_selection" )


class SingleSelectionLastCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection Last...' )
        view       = self.view
        selections = view.sel()

        if len( last_expansions ):
            last = last_expansions[-1]

            # If the selection changed as when using the arrow keys, we cannot use `last_expansions`
            if last not in selections:
                last = selections[-1]

        else:
            # Currently there is no Sublime Text support command to run and get the last selections
            last = selections[-1]

        selections.clear()
        selections.add( last )

        def delayed_run():
            # print( "SingleSelectionLast, Selecting last: " + str( last ) )

            view.show_at_center( last )
            sublime_plugin.sublime.status_message( '`%s` selected!' % view.substr( last ) )

        first = last_expansions[0]
        view.show_at_center( first )
        sublime.set_timeout_async( delayed_run, 100 )


class FindUnderExpandFirstSelectionListener(sublime_plugin.EventListener):

    def on_window_command(self, window, command_name, args):
        """
            Here we clean the selections.
        """
        if command_name == "find_under_expand":
            view       = window.active_view()
            selections = view.sel()

            selections_length      = len( selections )
            last_expansions_length = len( last_expansions )

            # print( "\nfind_under_expand(PRE),  selections_length: %14d, selections: %s%s" % ( selections_length, " "*12, str( [ selection for selection in selections ] ) ) )
            # print( "find_under_expand(PRE),  last_expansions_length: %9d, last_expansions: %s%s" % ( last_expansions_length, " "*7, str( last_expansions ) ) )

            if last_expansions_length > 1 \
                    and selections_length > 0 \
                    and last_expansions_length >= selections_length:

                last_expansions[:] = [ last_expansion for last_expansion in last_expansions if last_expansion in selections ]
                # print( "find_under_expand(PRE),  Cleaned last_expansions: %s" % ( str( last_expansions ) ) )

    def on_post_window_command(self, window, command_name, args):
        """
            Here add the recent created new selections by Sublime Text.
        """
        if command_name == "find_under_expand":
            view       = window.active_view()
            selections = view.sel()

            # print( "find_under_expand(POST), selections_length: %14d, selections: %s%s" % ( len( selections ), " "*12, str( [ selection for selection in selections ] ) ) )
            # print( "find_under_expand(POST), last_expansions_length: %9d, last_expansions: %s%s" % ( len( last_expansions ), " "*7, str( last_expansions ) ) )

            for selection in selections:

                # print( "find_under_expand(POST), Adding selection: %15s, not in last_expansions? %s" % ( selection, str( selection not in last_expansions ) ) )
                if selection not in last_expansions:
                    last_expansions.append( selection )


def run_tests():
    """
        How do I unload (reload) a Python module?
        https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-python-module
    """
    CURRENT_DIRECTORY    = os.path.dirname( os.path.realpath( __file__ ) )
    CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]

    print( "\n\n" )
    sublime_plugin.reload_plugin( CURRENT_PACKAGE_NAME + ".tests.unit_tests_runner" )
    sublime_plugin.reload_plugin( CURRENT_PACKAGE_NAME + ".tests.utilities" )
    sublime_plugin.reload_plugin( CURRENT_PACKAGE_NAME + ".tests.clear_cursors_carets_first_selection_unit_tests" )
    sublime_plugin.reload_plugin( CURRENT_PACKAGE_NAME + ".tests.clear_cursors_carets_last_selection_unit_tests" )

    from .tests import unit_tests_runner

    # Comment all the tests names on this list, to run all Unit Tests
    unit_tests_to_run = \
    [
        # "test_2_selections_at_last_word",
        # "test_3_selections_with_initial_selection",
    ]

    unit_tests_runner.run_unit_tests( unit_tests_to_run )


def plugin_loaded():
    """
        Running single test from unittest.TestCase via command line
        https://stackoverflow.com/questions/15971735/running-single-test-from-unittest-testcase-via-command-line
    """
    pass
    # run_tests()


