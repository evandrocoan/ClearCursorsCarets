

import sys

import sublime
import sublime_plugin

import textwrap
import unittest


def wrap_text(text):
    return textwrap.dedent( text ).strip( " " ).strip( "\n" )


class ClearCursorsCaretsUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None

        # Create a new Sublime Text view to perform the Unit Tests
        self.view = sublime.active_window().new_file()
        self.view.set_syntax_file( "Packages/Text/Plain text.tmLanguage" )

        # make sure we have a window to work with
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("close_windows_when_empty", False)

    # def tearDown(self):
    #     if self.view:
    #         self.view.set_scratch(True)
    #         self.view.window().focus_view(self.view)
    #         self.view.window().run_command("close_file")

    def setText(self, string, start_point=0):
        self.view.run_command("append", {"characters": wrap_text( string ) })

        selections = self.view.sel()
        selections.clear()
        selections.add( sublime.Region( start_point, start_point ) )

    def create_test_text(self):
        self.setText( """\
                word
                word
                word

                word
                word
                word""" )

    def test_triple_quotes_comment(self):
        self.create_test_text()

        # self.assertEqual( sublime.Region(0, 58), region )


