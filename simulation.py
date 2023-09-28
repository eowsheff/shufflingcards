from deck import Deck
import gsr
import shuffles
import numpy as np


def riffle_shuffle_simulation(n_trials: int, n_cards_in_deck: int, max_n_riffle_shuffle:int) -> list:
    """
    
    """
    # the `results` is a list of lists. For each trial we run, we append the results of that trial to the `results` list. 
    result: list = []

    # Execute n_trials
    for i_trial in range(n_trials):
        # For each trial create a new deck of cards
        deck: Deck = Deck().init_new_deck(n_cards_in_deck)

        # The trial_results holds all the different shuffled Decks of cards. 
        # The first deck in the trial_results is the initial deck, in new standard order.
        trial_result: list = []
        
        # Shuffle the deck n number of times, by cutting the deck into two packets and then riffle shuffling the 
        # two packets together, using the gsr.riffle_shuffle function.
        for i_shuffle in range(max_n_riffle_shuffle):
            cut_position: int = gsr.get_cut_position(deck)
            left_packet: Deck = deck[:cut_position]
            right_packet: Deck = deck[cut_position:]
            deck: Deck = gsr.riffle_shuffle(left_packet, right_packet)
            trial_result.append(deck)
            
        result.append(trial_result)
    
    return result


def a_shuffle_simulation(n_trials:int, a: int, n_cards_in_deck: int, max_n_shuffle: int) -> list:
    
    result: list = []
    
    for i_trial in range(n_trials):
        deck: Deck = Deck().init_new_deck(n_cards_in_deck)
        
        trial_result: list = []
        
        for i_shuffle in range(max_n_shuffle):
            deck: Deck = shuffles.a_shuffle(deck, a)
            trial_result.append(deck)
        
        result.append(trial_result)
    
    return result


def top_in_at_random_shuffle_simulation(n_trials: int, n_cards_in_deck: int) -> list:
    
    result: list = []

    for i_trial in range(n_trials):
        trial_result: list = []

        deck: Deck = Deck().init_new_deck(n_cards_in_deck)
        bottom_card: int = deck[-1]
        top_card: int = deck[0]
        
        while top_card != bottom_card:
            deck = deck.copy()
            deck: Deck = shuffles.top_in_at_random_shuffle(deck)
            trial_result.append(deck)
            top_card: int = deck[0]

        # perform one more top in at random move for the bottom card 
        deck = shuffles.top_in_at_random_shuffle(deck)
        trial_result.append(deck)
        
        result.append(trial_result)
        
    return result
        

def overhand_shuffle_simulation(n_trials: int, n_cards_in_deck: int, max_n_shuffle: int, p: float = 0.25) -> list:
        
    result: list = []
    
    for i_trial in range(n_trials):
        init_deck: Deck = Deck().init_new_deck(n_cards_in_deck)

        trial_result: list = []
        # trial_result.append(init_deck)
        
        for i_shuffle in range(max_n_shuffle):
            shuffled_deck: Deck = shuffles.overhand_shuffle(init_deck, p=p)
            trial_result.append(shuffled_deck)
            #TODO: Check object initiation for performance. This can also be done using copy() on `trial_result`, creating less objects. 
            new_deck: Deck = Deck()
            new_deck.cards = shuffled_deck.cards
            init_deck = new_deck
        
        result.append(trial_result)

    return result


def premo_simulation(n_trials: int, n_cards_in_deck: int, max_riffle_shuffle: int) -> list:
    result: list = []

    # For each trial, create cut and shuffled decks, between 1 shuffle and max_riffle shuffle
    # These cut and shuffled decks will be used later to pick a top card and then cut once more to complete the premo trick
    cut_and_shuffled_decks_all_trials: list = []
    for _ in range(n_trials):
        cut_and_shuffled_decks_per_trial = []
        d: Deck = Deck().init_new_deck(n_cards_in_deck)
        
        for e, _ in enumerate(range(max_riffle_shuffle)):
            d = d.copy()
            
            cut_position = np.random.randint(len(d)) # get uniform cut position
            d = d.cut_deck(cut_position)
            d = shuffles.riffle_shuffle(d)
            
            cut_and_shuffled_decks_per_trial.append(d)
        cut_and_shuffled_decks_all_trials.append(cut_and_shuffled_decks_per_trial)

    # `Cut_and_shuffled_decks` holds lists. Each list represents a trial. Each trial holds 1 to max_riffle_shuffles number of decks that
    # have been cut and riffle shuffled.
    # From these decks in each trial, we will pick the top card, place it randomly in the deck and cut once more.
    for trial_num, trial in enumerate(cut_and_shuffled_decks_all_trials, 1):
        for shuffle_num, d in enumerate(trial, 1):
            d: Deck = d.copy()
            row: dict = {}
            top_card: int = d.popleft()
            random_position_for_top_card: int = np.random.binomial(len(d), p=0.5)
            d.insert(random_position_for_top_card, top_card)

            cut_position: int = np.random.randint(len(d))
            d = d.cut_deck(cut_position)

            row['top_card'] = top_card
            row['deck'] = d
            row['trial'] = trial_num
            row['shuffle'] = shuffle_num
        
            result.append(row)

    return result
        

if __name__ == "__main__":
    N_TRIALS = 5
    N_CARDS = 52
    MAX_RIFFLE_SHUFFLES = 20
    RANDOM_SEED = 2023
    # When setting the random seeds for a-shuffled and riffle shuffled to the same number, running the same number of trials should yield the same result
    np.random.seed(RANDOM_SEED)
    r = riffle_shuffle_simulation(n_trials=N_TRIALS, n_cards_in_deck=N_CARDS, max_n_riffle_shuffle=MAX_RIFFLE_SHUFFLES)
    a_r = a_shuffle_simulation(n_trials=N_TRIALS, a=2, n_cards_in_deck=N_CARDS, max_n_shuffle=MAX_RIFFLE_SHUFFLES)
    
    riffle_rising_sequences = {}
    a_rising_sequences = {}
    
    for i, exps in enumerate(zip(r, a_r)):
        riffle_exp, a_exp = exps
        riffle_rising_sequences[i] = []
        a_rising_sequences[i] = []
        
        for riffle_deck, a_deck in zip(riffle_exp, a_exp):
            riffle_rising_sequences[i].append(riffle_deck.rising_sequences)
            a_rising_sequences[i].append(a_deck.rising_sequences)
    
    assert len(r) == N_TRIALS
    assert len(a_r) == N_TRIALS
    assert riffle_rising_sequences == a_rising_sequences
    
    
    # number of moves to get the bottom card to the top, should be equal or greater than the number of cards in the deck
    t_r = top_in_at_random_shuffle_simulation(n_trials=N_TRIALS, n_cards_in_deck=N_CARDS)
    number_of_top_in_at_raondom_moves = []
    for exp in t_r:
        number_of_top_in_at_raondom_moves.append(len(exp))
    
    assert len(r) == N_TRIALS
    assert any([i >= N_CARDS for i in number_of_top_in_at_raondom_moves])
    
    
    MAX_OVERHAND_SHUFFLES = 10000
    o_r = overhand_shuffle_simulation(n_trials=N_TRIALS, n_cards_in_deck=N_CARDS, max_n_shuffle=MAX_OVERHAND_SHUFFLES, p=0.2)