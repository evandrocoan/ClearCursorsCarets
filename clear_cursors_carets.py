
"""
See/read the README.MD file.
"""


import os

import sublime
import sublime_plugin


g_debug_index = 0
last_expansions = []
g_last_selection = None

def force_focus(view, region_borders):
    window = sublime.active_window()
    window.focus_view( view )
    view.show( region_borders )


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
                print('ClearCursorsCarets: Could not detect the find under expand selections.')
                view.run_command( "single_selection" )

            else:
                global g_last_selection
                g_last_selection = first
                view.run_command( "clear_cursors_carets_single_selection_blinker", { "message": "FIRST" } )

        else:
            print('ClearCursorsCarets: Could not detect the find under expand selections.')
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

        global g_last_selection
        g_last_selection = last
        view.run_command( "clear_cursors_carets_single_selection_blinker", { "message": "LAST" } )


class ClearCursorsCaretsSingleSelectionBlinkerCommand(sublime_plugin.TextCommand):

    def run(self, edit, message):
        view = self.view
        selections = view.sel()

        def run_blinking_focus():
            force_focus( view, g_last_selection )
            view.run_command( "clear_cursors_carets_single_selection_blinker_helper" )

        selections.clear()
        selections.add( g_last_selection.end() )
        sublime_plugin.sublime.status_message( 'Selection set to %s %s' % ( message, view.substr( g_last_selection )[:100] ) )

        # view.run_command( "move", {"by": "characters", "forward": False} )
        # print( "SingleSelectionLast, Selecting last:", g_last_selection )
        sublime.set_timeout( run_blinking_focus, 250 )
        force_focus( view, g_last_selection )


class ClearCursorsCaretsSingleSelectionBlinkerHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection Last Helper... ', g_last_selection )
        view = self.view
        selections = view.sel()

        selections.clear()
        selections.add( g_last_selection )


class FindUnderExpandFirstSelectionListener(sublime_plugin.EventListener):

    # def on_text_command(self, view, command_name, args):
    #     self.on_window_command( view.window(), command_name, args )

    # def on_post_text_command(self, view, command_name, args):
    #     self.on_post_window_command( view.window(), command_name, args )

    def on_window_command(self, window, command_name, args):
        """
            Here we clean the selections.
        """
        if command_name == 'find_under_expand':
            # global g_debug_index; g_debug_index += 1; print( g_debug_index, 'command_name', command_name)

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
        if command_name == 'find_under_expand':
            # global g_debug_index; g_debug_index += 1; print( g_debug_index, 'command_name', command_name)
            view       = window.active_view()
            selections = view.sel()

            # print( "find_under_expand(POST), selections_length: %14d, selections: %s%s" % ( len( selections ), " "*12, str( [ selection for selection in selections ] ) ) )
            # print( "find_under_expand(POST), last_expansions_length: %9d, last_expansions: %s%s" % ( len( last_expansions ), " "*7, str( last_expansions ) ) )

            for selection in selections:

                # print( "find_under_expand(POST), Adding selection: %15s, not in last_expansions? %s" % ( selection, str( selection not in last_expansions ) ) )
                if selection not in last_expansions:
                    last_expansions.append( selection )

