from deck import Deck
import gsr
import shuffles
import numpy as np

#TODO: fix setting a random seed per simulation


def riffle_shuffle_simulation(n_experiments: int, n_cards_in_deck: int, max_n_riffle_shuffle:int, random_seed: int = None) -> list:
    # for testing and reproduction purposes, set the random seed in the scope of this simulation.
    np.random.seed(random_seed)
    
    # the `results` is a list of lists. For each experiment we run, we append the results of that experiment to the `results` list. 
    result: list = []

    # Execute n_experiments
    for i_experiment in range(n_experiments):
        # For each experiment create a new deck of cards
        deck: Deck = Deck().init_new_deck(n_cards_in_deck)

        # The experiment_results holds all the different shuffled Decks of cards. 
        # The first deck in the experiment_results is the initial deck, in new standard order.
        experiment_result: list = []
        experiment_result.append(deck)
        
        # Shuffle the deck n number of times, by cutting the deck into two packets and then riffle shuffling the 
        # two packets together, using the gsr.riffle_shuffle function.
        for i_shuffle in range(max_n_riffle_shuffle):
            cut_position: int = gsr.get_cut_position(deck)
            left_packet: Deck = deck[:cut_position]
            right_packet: Deck = deck[cut_position:]
            deck: Deck = gsr.riffle_shuffle(left_packet, right_packet)
            experiment_result.append(deck)
            
        result.append(experiment_result)
    
    return result


def a_shuffle_simulation(n_experiments:int, a: int, n_cards_in_deck: int, max_n_shuffle: int, random_seed: int = None) -> list:
    # for testing and reproduction purposes, set the random seed in the scope of this simulation.
    np.random.seed(random_seed)
    
    result: list = []
    
    for i_experiment in range(n_experiments):
        deck: Deck = Deck().init_new_deck(n_cards_in_deck)
        
        experiment_result: list = []
        experiment_result.append(deck)
        
        for i_shuffle in range(max_n_shuffle):
            deck: Deck = shuffles.a_shuffle(deck, a)
            experiment_result.append(deck)
        
        result.append(experiment_result)
    
    return result


def top_in_at_random_shuffle_simulation(n_experiments: int, n_cards_in_deck: int, random_seed: int = None) -> list:
    # for testing and reproduction purposes, set the random seed in the scope of this simulation.
    np.random.seed(random_seed)
    
    result: list = []
    
    for i_experiment in range(n_experiments):
        deck: Deck = Deck().init_new_deck(n_cards_in_deck)
        bottom_card: int = deck[0]
        
        experiment_result: list = []
        experiment_result.append(deck)
        
        while deck[-1] != bottom_card:
            deck = shuffles.top_in_at_random_shuffle(deck)
            experiment_result.append(deck)
        
        # perform one more top in at random move for the bottom card 
        deck = shuffles.top_in_at_random_shuffle(deck)
        experiment_result.append(deck)
        
        result.append(experiment_result)
        
    return result
        

def overhand_shuffle_simulation(n_experiments: int, n_cards_in_deck: int, max_n_shuffle: int, p: float = 0.2, random_seed: int = None) -> list:
    # for testing and reproduction purposes, set the random seed in the scope of this simulation.
    np.random.seed(random_seed)
        
    result: list = []
    
    for i_experiment in range(n_experiments):
        init_deck: Deck = Deck().init_new_deck(n_cards_in_deck)

        experiment_result: list = []
        experiment_result.append(init_deck)
        
        for i_shuffle in range(max_n_shuffle):
            shuffled_deck: Deck = shuffles.overhand_shuffle(init_deck, p=p)
            experiment_result.append(shuffled_deck)
            new_deck: Deck = Deck()
            new_deck.cards = shuffled_deck.cards
            init_deck = new_deck
        
        result.append(experiment_result)

    return result
        

if __name__ == "__main__":
    N_EXPERIMENTS = 5
    N_CARDS = 52
    MAX_RIFFLE_SHUFFLES = 20
    RANDOM_SEED = 2023
    # When setting the random seeds for a-shuffled and riffle shuffled to the same number, running the same number of experiments should yield the same result
    r = riffle_shuffle_simulation(n_experiments=N_EXPERIMENTS, n_cards_in_deck=N_CARDS, max_n_riffle_shuffle=MAX_RIFFLE_SHUFFLES, random_seed=RANDOM_SEED)
    a_r = a_shuffle_simulation(n_experiments=N_EXPERIMENTS, a=2, n_cards_in_deck=N_CARDS, max_n_shuffle=MAX_RIFFLE_SHUFFLES, random_seed=RANDOM_SEED)
    
    riffle_rising_sequences = {}
    a_rising_sequences = {}
    
    for i, exps in enumerate(zip(r, a_r)):
        riffle_exp, a_exp = exps
        riffle_rising_sequences[i] = []
        a_rising_sequences[i] = []
        
        for riffle_deck, a_deck in zip(riffle_exp, a_exp):
            riffle_rising_sequences[i].append(riffle_deck.rising_sequences)
            a_rising_sequences[i].append(a_deck.rising_sequences)
    
    assert len(r) == N_EXPERIMENTS
    assert len(a_r) == N_EXPERIMENTS
    assert riffle_rising_sequences == a_rising_sequences
    
    
    # number of moves to get the bottom card to the top, should be equal or greater than the number of cards in the deck
    t_r = top_in_at_random_shuffle_simulation(n_experiments=N_EXPERIMENTS, n_cards_in_deck=N_CARDS, random_seed=RANDOM_SEED)
    number_of_top_in_at_raondom_moves = []
    for exp in t_r:
        number_of_top_in_at_raondom_moves.append(len(exp))
    
    assert len(r) == N_EXPERIMENTS
    assert any([i >= N_CARDS for i in number_of_top_in_at_raondom_moves])
    
    
    MAX_OVERHAND_SHUFFLES = 10000
    o_r = overhand_shuffle_simulation(n_experiments=N_EXPERIMENTS, n_cards_in_deck=N_CARDS, max_n_shuffle=MAX_OVERHAND_SHUFFLES, p=0.2, random_seed=RANDOM_SEED)
    # write unit tests