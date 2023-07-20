from deck import Deck
import gsr
import shuffles
import randomness_test

import numpy as np


def riffle_shuffle_simulation(n_experiments: int, n_cards_in_deck: int, max_n_riffle_shuffle:int, random_seed: np.random.seed=None) -> list:
    deck: Deck = Deck().init_new_deck(n_cards_in_deck)
    result: list = []

    for i_experiment in range(n_experiments):
        experiment_result: list = []
        for i_shuffle in range(max_n_riffle_shuffle):
            # print(shuffle)
            if i_shuffle == 0:
                experiment_result.append(deck)
            cut_position: int = gsr.get_cut_position(deck)
            left_packet: Deck = deck[:cut_position]
            right_packet: Deck = deck[cut_position:]
            riffle_shuffled_pile: Deck = gsr.riffle_shuffle(left_packet, right_packet)
            
            experiment_result.append(riffle_shuffled_pile)
        result.append(experiment_result)
    return result

def a_shuffle_simulation(n_experiments:int, n_cards_in_deck: int, a: int, max_n_shuffle: int, random_seed: np.random.seed=None) -> list:
    deck: Deck = Deck().init_new_deck(n_cards_in_deck)
    results: list = []

    for i_experiment in range(n_experiments):
        experiment_results: list = []
