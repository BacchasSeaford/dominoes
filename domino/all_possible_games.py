import common
import copy
import domino
import itertools
import multiprocessing
import random

FIXED_MOVES = 8

def compute_all_possible_games(game):
    in_progress = [game]
    completed = []

    while in_progress:
        game = in_progress.pop()
        moves = game.valid_moves()

        for move in moves:
            new_game = copy.deepcopy(game)
            result = new_game.make_move(*move)
            if result is None:
                in_progress.append(new_game)
            else:
                completed.append(new_game)

    return completed

with common.stopwatch('Initializing random game'):
    game = domino.Game()

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

with common.stopwatch('Computation of all possible games'):
    moves = game.valid_moves()

    games = []
    for move in moves:
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)

        games.append(new_game)

    with multiprocessing.Pool(len(games)) as pool:
        completed = pool.map(compute_all_possible_games, games)

    completed = itertools.chain(*completed)

    print(len(list(completed)))