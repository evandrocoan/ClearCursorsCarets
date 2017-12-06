

import sys

import sublime
import sublime_plugin


class ClearCursorsCaretsLastSelectionUnitTests(sys.modules["ClearCursorsCarets.tests.utilities"].BasicSublimeTextViewTestCase):

    @classmethod
    def setUp(self):
        super().setUp()
        self.view.set_syntax_file( "Packages/Text/Plain text.tmLanguage" )

    def test_first_selection_with_1_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_first_selection_with_2_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_first_selection_with_3_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_first_selection_with_5_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_first_selection_with_6_selections_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_first_selection_with_6_selections_plus_redundant_expand_at_first_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_last_selection_with_1_selections_at_last_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(0, 4), region )

    def test_last_selection_with_2_selections_at_last_word(self):
        self.create_test_text(0)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_last" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(5, 9), region )

    def test_last_selection_with_6_selections_at_last_word(self):
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

    def test_last_selection_with_6_selections_plus_redundant_expand_at_last_word(self):
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


