"""
Run this script if you want your IA to automatically play against Random
without having to change game settings.
"""

import othello_gui
game = othello_gui.OthelloGUI('Random', 'Buehler_Dekhli')
game.run_auto()