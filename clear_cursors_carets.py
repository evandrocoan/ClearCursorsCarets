
"""
See/read the README.MD file.
"""


import os

import sublime
import sublime_plugin


def force_focus(view, region):
    window = sublime.active_window()
    window.focus_view( view )
    view.show( region )


last_expansions = []

class SingleSelectionFirstCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection First...' )
        # print( "SingleSelectionFirst, last_expansions_length: " + str( len( last_expansions ) ) )
        view       = self.view
        selections = view.sel()

        # If the selection changed as when using the arrow keys, we cannot use `first_expansion`
        if len( last_expansions ):
            first = last_expansions[0]
            # print( "SingleSelectionFirst, Selecting first: " + str( first ) )

            if first not in selections:
                view.run_command( "single_selection" )

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

        def run_blinking_focus():
            global last_selection
            last_selection = last

            force_focus( view, last )
            view.run_command( "single_selection_last_helper" )

        selections.clear()
        sublime_plugin.sublime.status_message( 'Last selection set to %s' % view.substr( last ) )

        # view.run_command( "move", {"by": "characters", "forward": False} )
        # print( "SingleSelectionLast, Selecting last: " + str( last ) )
        sublime.set_timeout_async( run_blinking_focus, 200 )
        force_focus( view, last )


class SingleSelectionLastHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection Last Helper...' )
        view       = self.view
        selections = view.sel()

        force_focus( view, last_selection )
        selections.clear()

        selections.add( last_selection )
        force_focus( view, last_selection )


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

