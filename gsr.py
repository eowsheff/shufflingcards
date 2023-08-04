import numpy as np
from deck import Deck


def get_cut_position(deck: Deck, p: float = 0.5) -> np.ndarray:
    """
    Given an instance of Deck, this function returns a cut position, as an index (int), to use to cut the deck of cards.
    The cut position is determined according to the binomial distribution, as described in the paper, with parameter p.

    According to the paper by Diaconis, the cut position is determined with biomial parameter p=0.5.
    p=0.5, unsured the cut is made roughly around the middle of the deck.

    E.g.:  
        d = Deck.init_new_deck(52) # init new deck of cards with 52 cards
        cut_position = get_cut_position(deck) # get the index of the cut position
        # then to cut the deck:
        left_packet = d[:cut_position]
        right_packet= d[cut_position:]

    :param  deck: instance of Deck of cards, holding cards in Deck.cards
            p: binomial parameter, to determine the cut position.

    :return the index of the cut as an integer.
    """
    n: int = len(deck.cards)
    return np.random.binomial(n=n, p=p)
    

def drop_from_left_stack(n_left: int, n_right: int) -> bool:
    """
    This function takes the number of cards (as integers) in the two decks, and returns a boolean (True/False), if a card should be dropped
    from the the left deck (the number of cards passed as `n_left`). 
    n_left and n_right can be thought of as the number of cards in a left packet and right packet, after a deck has been cut.

    - The probability that a card should be dropped from the left stack is proportional to the number of cards in the left packet vs. the total number of
    cards in the left + right packet.
    - If there are no cards in the left packet, a card should always be dropped from the right packet. This function returns False (do not drop from left packet)
    - If there are no cards in the right packet, a card should always be dropped from the left packet. This function returns True (drop from left packet)

    :param  n_left: number of cards in the left packet
            n_right: number of cards in the right packet

    :return boolean indicating if a card should be dropped from the packet corresponding to n_left
    """
    if n_left > 0 and n_right > 0:
        prob_n_left: float = (n_left) / (n_left + n_right)
        uniform_random: float = np.random.random()
        return prob_n_left > uniform_random
        
    elif n_left == 0 and n_right > 0:
        return False
    
    elif n_left > 0 and n_right == 0:
        return True
    
    else:
        raise ValueError("n_left and n_right can not both be zero.")


def riffle_shuffle(left_packet: Deck, right_packet: Deck) -> Deck:
    """
    This function simulates a riffle shuffle, given a left packet (instance of Deck) and a right packet (instance of Deck). 
    It returns a new Deck object with Deck.cards shuffled according to the riffle shuffle, decsribed in the paper by Diaconis.

    This function makes a new instance of a Deck (pile), and assigns cards from the either the left_packet or right_packet to the pile.cards variable according to the function
    `drop_from_left_stack`.

    :param  left_packet: an instance of Deck, which holds the left packet of cards after a cut
            right_packet: an instance of Deck, which holds the left packet of cards after a cut

    return: pile: a new instance of Deck, which holds Deck.cards with riffle shuffled cards.
    """
    n_left: int = len(left_packet)
    n_right: int = len(right_packet)

    pile: Deck = Deck()

    while left_packet or right_packet:
        if drop_from_left_stack(n_left, n_right):
            card_to_drop: int = left_packet.cards.popleft()
            n_left -= 1
        else:
            card_to_drop: int = right_packet.cards.popleft()
            n_right -= 1        
        pile.cards.append(card_to_drop)

    return pile


if __name__ == "__main__":
    number_of_cards_in_deck: int = 52
    deck = Deck()
    deck = deck.init_new_deck(number_of_cards_in_deck)
    
    # test if cut off position is a valid number
    cut_position: int = get_cut_position(deck)
    left_packet: Deck = deck[:cut_position]
    right_packet: Deck = deck[cut_position:]
    assert cut_position > 0 and cut_position <= number_of_cards_in_deck

    # test if the shuffled pile contains the exact same number of cards as the original pilt
    # test if not all the positions of cards in the shuffled pile are in the same position as the original deck
    riffle_shuffled_pile: Deck = riffle_shuffle(left_packet, right_packet)
    assert len(riffle_shuffled_pile) == number_of_cards_in_deck
    assert sum(o == s for o,s in zip(deck, riffle_shuffled_pile)) != number_of_cards_in_deck
    
    # number of rising sequences can not be more than 2, after 1 riffle shuffle
    assert deck.rising_sequences <= 2
