import numpy as np
from collections import deque
from deck import Deck
import gsr

def _create_packet(cards: deque) -> Deck:
    """
    A helper function used to create the left and right packets within the `riffle_shuffle` and `a_shuffles` functions. 
    The cards that are assigned to the packet are given as a sequence of Deck.cards in the parameter of this function. 

    This function returns a new instance of a Deck

    :param  cards: a sequence of Deck.cards of a collections.deque object with a sequence of integers, representing cards in a deck
    :return packet: a new instance of Deck, with the `cards` from the params assigned to the instance to Deck.cards
    """

    packet: Deck = Deck()
    packet.cards = cards
    return packet

def top_in_at_random_shuffle(deck) -> Deck:
    """
    This function simulates one move for a top in 'top in at random shuffle'. 
    That is: it takes the top card and inserts it in a random position of the same deck, but once! 
    This function should be called multiple times to shuffle a deck properly.

    Following real-life, this function performs the permutations on the cards in the deck on the deck itself. 
    Because this function performs the shuffle in the same deck it got as a parameter, it does not return a new deck. It will return 
    the reference to the original deck.

    :param      deck: instance of Deck of cards, holding cards in Deck.cards
    :return     deck: the same instance as given in param, but with one 'top in at random' permutation performed on the cards
    """
    deck = deck.copy()
    number_of_cards: int = len(deck)
    # take the top card
    top_card: int = deck.pop()
    idx_to_insert_card: int = np.random.randint(0, number_of_cards+1) 
    # insert the top card to a random position in the deck
    deck.insert(idx_to_insert_card, top_card)
    
    return deck


def overhand_shuffle(deck: Deck, p: float=0.2):
    """
    
    """

    # n_cards: int = len(deck) # TODO: check if binomial n should be the cards still in the orginal deck or n_cards
    pile = Deck() # This pile will represent the shuffled pile of cards
    
    while len(deck) > 0:
        n_cards_still_in_deck: int = len(deck)
        clump_size: int = np.random.binomial(n=n_cards_still_in_deck, p=p) 

        # TODO: include or exclude - based on using cards_still_in_deck vs n_cards
        # if clump_size > cards_still_in_deck:
        #     clump_size = cards_still_in_deck
        
        # Create a clump of cards that is added to the new pile of cards
        # Use slice with positive numbers instead of a slice with negative index for performance
        clump: Deck = deck[n_cards_still_in_deck-clump_size : n_cards_still_in_deck]

        # remove number of cards in the clump from original deck
        for c in range(clump_size):
            deck = deck.copy()
            deck.pop()
        
        # Add clump of cards to the shuffled pile of cards
        pile.cards.extend(clump.cards)
        
    return pile
    

def a_shuffle(deck: Deck, a: int) -> Deck:
    number_of_cuts: int = a-1
    p: float = 1/float(a)

    list_of_packets: list = list()

    total_cards_cut = 0
    for cut in range(number_of_cuts):
        relative_cut_position: int = gsr.get_cut_position(deck, p)
        absolute_cut_position: int = total_cards_cut + relative_cut_position
        cards_from_deck: Deck = deck[total_cards_cut:absolute_cut_position]
        packet: Deck = _create_packet(cards_from_deck)
        list_of_packets.append(packet)
        total_cards_cut += relative_cut_position
    
    packet: Deck = _create_packet(deck[total_cards_cut:]) # add last cards in deck to piles
    list_of_packets.append(packet)

    for i, pckt in enumerate(list_of_packets):
        if i == 0:
            result: Deck = pckt
        else:
            result: Deck = gsr.riffle_shuffle(result, pckt)

    return result


if __name__ == "__main__":
    number_of_cards_in_deck = 52

    first_deck = Deck().init_new_deck(number_of_cards_in_deck)
    shuffled_first_deck = top_in_at_random_shuffle(first_deck)
    assert first_deck is shuffled_first_deck

    second_deck = Deck().init_new_deck(52)
    new_shuffled_deck = top_in_at_random_shuffle(second_deck, copy=True)
    assert new_shuffled_deck is not second_deck
    assert sum(o == s for o,s in zip(new_shuffled_deck.cards, second_deck.cards)) != number_of_cards_in_deck

    a_shuffled_pile = a_shuffle(second_deck, a=10)
    assert len(a_shuffled_pile) == number_of_cards_in_deck
    assert sum(o == s for o,s in zip(second_deck, a_shuffled_pile)) != number_of_cards_in_deck

    overhand_shuffled_pile = overhand_shuffle(second_deck, p=0.2)
    assert len(overhand_shuffle) == number_of_cards_in_deck
    assert sum(o == s for o,s in zip(second_deck, overhand_shuffled_pile)) != number_of_cards_in_deck