
"""
See/read the README.MD file.
"""

import os

import sublime
import sublime_plugin

g_debug_index = 0
last_expansions = []


class Pref:
    p = 'clear_cursors_carets.'

    @classmethod
    def blink_selection_on_single_selection(cls, settings):
        return bool( settings.get( cls.p + 'blink_selection_on_single_selection', True ) )


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
                view.run_command( "clear_cursors_carets_single_selection_blinker", {
                        "message": "FIRST",
                        "region_start": first.begin(),
                        "region_end": first.end(),
                    } )

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

        view.run_command( "clear_cursors_carets_single_selection_blinker", {
                "message": "LAST",
                "region_start": last.begin(),
                "region_end": last.end(),
            } )


def fix_selection_aligment(selections, region_borders):

    if selections:
        last_selection = None

        for selection in sorted( selections, key=lambda item: item.begin() ):
            # print('selection.begin', selection.begin())

            if selection.begin() > region_borders.begin():

                if last_selection is None:
                    last_selection = selection
                break

            last_selection = selection

        return last_selection


def force_focus(view, region_borders):
    window = sublime.active_window()
    window.focus_view( view )
    view.show( region_borders )


class ClearCursorsCaretsSingleSelectionBlinkerCommand(sublime_plugin.TextCommand):

    def run(self, edit, message, region_start, region_end):
        view = self.view
        selections = view.sel()
        settings = view.settings()
        region_borders = sublime.Region( region_start, region_end )
        region_borders = fix_selection_aligment( selections, region_borders )

        def run_blinking_focus():
            if len( selections ) == 1 and selections[0].end() == region_borders.end():
                force_focus( view, region_borders )

                view.run_command( "clear_cursors_carets_single_selection_blinker_helper", {
                        "region_start": region_start,
                        "region_end": region_end,
                    } )

        selections.clear()
        sublime.status_message( "Selection set to %s %s" % ( message, view.substr( region_borders )[:100] ) )

        # view.run_command( "move", {"by": "characters", "forward": False} )
        # print( "SingleSelectionLast, Selecting last:", region_borders )
        if Pref.blink_selection_on_single_selection( settings ):
            selections.add( region_borders.end() )
            sublime.set_timeout( run_blinking_focus, 250 )
            force_focus( view, region_borders )

        else:
            selections.add( region_borders )
            force_focus( view, region_borders )


class ClearCursorsCaretsSingleSelectionBlinkerHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, region_start, region_end):
        # print( 'Calling Selection Last Helper... ', region_start, region_end )
        view = self.view
        selections = view.sel()
        region_borders = sublime.Region( region_start, region_end )

        selections.clear()
        selections.add( region_borders )


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

