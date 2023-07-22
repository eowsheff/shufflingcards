import numpy as np
from deck import Deck
from gsr import get_cut_position, create_packet, riffle_shuffle

# TODO: add doc strings
# TODO: write generic functions for each shuffle

def _copy_deck(deck) -> Deck: #TODO: move this as a method of the Deck class
    original_cards: Deck = deck.cards.copy()
    deck: Deck = Deck()
    deck.cards = original_cards
    return deck


def _put_top_card_in_random_position(deck) -> Deck:
    number_of_cards: int = len(deck)
    top_card: int = deck.pop()
    idx_to_insert_card: int = np.random.randint(0, number_of_cards+1) 
    deck.insert(idx_to_insert_card, top_card)
    
    return deck


def top_in_at_random_shuffle(deck: Deck, copy: bool = False) -> Deck:
    """
    TODO: add docstrings
    """
    if copy:
        deck: Deck = _copy_deck(deck)

    number_of_cards: int = len(deck)
    bottom_card: int = deck.popleft()

    while deck.popleft() != bottom_card:
        deck: Deck = _put_top_card_in_random_position(deck)
    
    deck: Deck = _put_top_card_in_random_position(deck) # perform one more top in at random move for the bottom card

    return deck


def overhand_shuffle(deck: Deck, p: float=0.2, copy: bool = False):
    if copy:
        deck: Deck = _copy_deck(deck)

    n_cards: int = len(deck)
    pile = Deck()
    
    while len(deck) > 0:
        clump_size: int = np.random.binomial(n=n_cards, p=p)
        clump: Deck.cards = deck[:clump_size]
        cards_still_in_deck: int = len(deck)
        
        if clump_size > cards_still_in_deck:
            clump_size = cards_still_in_deck
            
        for c in range(clump_size):
            deck.popleft()
        
        pile.cards.append(clump.cards)
        
    return pile
    

def a_shuffle(deck: Deck, a: int) -> Deck:
    number_of_cuts: int = a-1
    p: float = 1/float(a)

    list_of_packets: list = list()

    total_cards_cut = 0
    for cut in range(number_of_cuts):
        relative_cut_position: int = get_cut_position(deck, p)
        absolute_cut_position: int = total_cards_cut + relative_cut_position
        cards_from_deck: Deck = deck[total_cards_cut:absolute_cut_position]
        packet: Deck = create_packet(cards_from_deck)
        list_of_packets.append(packet)
        total_cards_cut += relative_cut_position
    
    packet: Deck = create_packet(deck[total_cards_cut:]) # add last cards in deck to piles
    list_of_packets.append(packet)

    for i, pckt in enumerate(list_of_packets):
        if i == 0:
            result: Deck = pckt
        else:
            result: Deck = riffle_shuffle(result, pckt)

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