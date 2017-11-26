
"""
See/read the README.MD file.
"""


import sublime
import sublime_plugin


last_expansions = []
first_expansion = None

class SingleSelectionFirstCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # print( 'Calling Selection First...' )
        view       = self.view
        selections = view.sel()

        global first_expansion

        # If the selection changed as when using the arrow keys, we cannot use `first_expansion`
        if first_expansion \
                and first_expansion in selections:

            first = first_expansion
            # print( "Selecting first: " + str( first ) )

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
            # print( "Selecting last: " + str( last ) )

            # If the selection changed as when using the arrow keys, we cannot use `last_expansions`
            if last not in selections:
                last = selections[-1]

        else:
            # Currently there is no Sublime Text support command to run and get the last selections
            last = selections[-1]

        selections.clear()
        selections.add( last )
        view.show( last )


class FindUnderExpandFirstSelectionListener(sublime_plugin.EventListener):

    def on_window_command(self, window, command_name, args):
        """
            Here we clean the selections and also keep re-selected the first selection on
            `first_expansion`.
        """
        if command_name == "find_under_expand":
            # print( "(PRE) Running... find_under_expand" )
            global first_expansion

            view       = window.active_view()
            selections = view.sel()

            selections_length      = len( selections )
            last_expansions_length = len( last_expansions )

            if last_expansions_length > 1 \
                    and selections_length > 0 \
                    and last_expansions_length > selections_length:

                # print( "Cleaning: " + str( last_expansions ) )
                del last_expansions[:]
                first_expansion = selections[0]

    def on_post_window_command(self, window, command_name, args):
        """
            Here add the recent created new selections by Sublime Text and first select the
            `first_expansion` when there is not previous selection.
        """
        if command_name == "find_under_expand":
            # print( "(POS) Running... find_under_expand" )
            global first_expansion

            view       = window.active_view()
            selections = view.sel()

            if not first_expansion:
                first_expansion = selections[0]

            for selection in selections:

                if selection not in last_expansions:
                    # print( "selection: " + str( selection ) )
                    last_expansions.append( selection )

            # print( "last_expansions: " + str( last_expansions ) )


