

import sys

import sublime
import sublime_plugin

import textwrap
import unittest


def wrap_text(text):
    return textwrap.dedent( text ).strip( " " ).strip( "\n" )


class ClearCursorsCaretsFirstSelectionUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None

        # Create a new Sublime Text view to perform the Unit Tests
        self.view = sublime.active_window().new_file()
        self.view.set_syntax_file( "Packages/Text/Plain text.tmLanguage" )

        # make sure we have a window to work with
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string, start_point=0):
        self.view.run_command("append", {"characters": wrap_text( string ) })

        selections = self.view.sel()
        selections.clear()
        selections.add( sublime.Region( start_point, start_point ) )

    def create_test_text(self, start_point):
        """
            1. (0, 4),
            2. (5, 9),
            3. (10, 14),
            4. (16, 20),
            5. (21, 25),
            6. (26, 30),
        """
        self.setText( """\
                word
                word
                word

                word
                word
                word""", start_point )

    def test_first_selection_with_2_selections_at_last_word(self):
        self.create_test_text(26)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(26, 30), region )

    def test_first_selection_with_3_selections_at_last_word(self):
        self.create_test_text(21)
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "find_under_expand" )
        self.view.window().run_command( "single_selection_first" )

        region = self.view.sel()[0]
        self.assertEqual( sublime.Region(21, 25), region )


