"""
Run this script if you want your IA to automatically play against Random
without having to change game settings.
"""

import multiprocessing
import othello_gui

base_name = "Buehler_Dekhli"
runners = (
    (base_name + "_v1", base_name),
    (base_name + "_v6", base_name),
    (base_name + "_v5", base_name),
    ("Random", base_name)
)


def run(black, white):
    _game = othello_gui.OthelloGUI(black, white)
    _game.run_auto()


def run_tests():
    for first, second in runners:
        multiprocessing.Process(target=run, args=(first, second)).start()
        multiprocessing.Process(target=run, args=(second, first)).start()


if __name__ == "__main__":
    run_tests()
