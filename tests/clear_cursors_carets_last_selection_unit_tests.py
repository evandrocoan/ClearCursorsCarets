

import sublime
import sublime_plugin

import os
import sys
import importlib

PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) )
CURRENT_PACKAGE_NAME = os.path.basename( PACKAGE_ROOT_DIRECTORY ).rsplit('.', 1)[0]

utilities = importlib.import_module( CURRENT_PACKAGE_NAME + ".tests.utilities" )


class ClearCursorsCaretsLastSelectionUnitTests(utilities.BasicSublimeTextViewTestCase):

    def test_1_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_2_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(5, 9), region )

    def test_6_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(26, 30), region )

    def test_6_selections_plus_redundant_expand_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(26, 30), region )

    def test_2_selections_at_last_word(self):
        self.create_test_text(26)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_3_selections_at_last_word(self):
        self.create_test_text(26)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(5, 9), region )

    def test_6_selections_at_last_word(self):
        self.create_test_text(26)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(21, 25), region )

    def test_6_selections_at_last_word_plus_redundant_expansion_at_last_word(self):
        self.create_test_text(26)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(21, 25), region )

