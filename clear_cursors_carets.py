
"""
See/read the README.MD file.
"""


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

        # print( "SingleSelectionLast, Selecting last: " + str( last ) )
        selections.clear()
        selections.add( last )
        view.show( last )


class FindUnderExpandFirstSelectionListener(sublime_plugin.EventListener):

    def on_window_command(self, window, command_name, args):
        """
            Here we clean the selections.
        """
        if command_name == "find_under_expand":
            # print( "(PRE) Running... find_under_expand" )
            view       = window.active_view()
            selections = view.sel()

            selections_length      = len( selections )
            last_expansions_length = len( last_expansions )

            if last_expansions_length > 1 \
                    and selections_length > 0 \
                    and last_expansions_length >= selections_length:

                # print( "(PRE) Cleaning: " + str( last_expansions ) )
                for index, selection in enumerate( last_expansions ):

                    if selection not in selections:
                        del last_expansions[index]

    def on_post_window_command(self, window, command_name, args):
        """
            Here add the recent created new selections by Sublime Text.
        """
        if command_name == "find_under_expand":
            # print( "(POS) Running... find_under_expand" )
            view       = window.active_view()
            selections = view.sel()

            for selection in selections:

                if selection not in last_expansions:
                    # print( "(POS) selection: " + str( selection ) )
                    last_expansions.append( selection )

            # print( "(POS) last_expansions: " + str( last_expansions ) )


