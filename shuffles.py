import numpy as np
from deck import Deck
from gsr import get_cut_position, create_packet, riffle_shuffle

# TODO: add doc strings
# TODO: write generic functions for each shuffle

def copy_deck(deck) -> Deck: #TODO: move this as a method of the Deck class
    original_cards: Deck = deck.cards.copy()
    deck: Deck = Deck()
    deck.cards = original_cards
    return deck


def do_top_in_at_random(deck: Deck, copy: bool = False) -> Deck:
    """
    TODO: add docstrings
    """
    if copy:
        deck = copy_deck(deck)

    number_of_cards: int = len(deck)
    bottom_card: Card = deck[-1]

    def put_top_card_in_random_position(deck) -> Deck:
        top_card: Card = deck.popleft()
        idx_to_insert_card: int = np.random.randint(0, number_of_cards+1) 
        deck.insert(idx_to_insert_card, top_card)

    while deck[0] != bottom_card:
        put_top_card_in_random_position(deck)
    
    put_top_card_in_random_position(deck) # perform one more top in at random move for bottom card

    return deck


def do_one_overhand_shuffle(deck: Deck, copy: bool = False):
    if copy:
        deck: Deck = copy_deck(deck)

    number_of_cards: int = len(deck)
    clump_size: int = np.random.randint(1, int(number_of_cards / 2))


def do_a_shuffle(deck: Deck, a: int) -> Deck:
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
    shuffled_first_deck = do_top_in_at_random(first_deck)
    assert first_deck is shuffled_first_deck

    second_deck = Deck().init_new_deck(52)
    new_shuffled_deck = do_top_in_at_random(second_deck, copy=True)
    assert new_shuffled_deck is not second_deck
    assert sum(o == s for o,s in zip(new_shuffled_deck.cards, second_deck.cards)) != number_of_cards_in_deck

    a_shuffled_pile = do_a_shuffle(second_deck, a=10)
    assert len(a_shuffled_pile) == number_of_cards_in_deck
    assert sum(o == s for o,s in zip(second_deck, a_shuffled_pile)) != number_of_cards_in_deck

    # cut off for clumps according to binomial distribution
    # print(np.random.binomial(int(52/2), scale=1, size=1)[0])
    
    cards = np.array([3,4,1,5,7,6,2,3,8,9,10])
    sorted = np.sort(cards)
    print(sorted)

    