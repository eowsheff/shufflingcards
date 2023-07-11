import numpy as np
from deck import Deck

# np.random.seed(0)

def get_cutoff_position(deck: Deck, p: float = 0.5) -> int:
    n: int = len(deck.cards)
    cut_off_position: int = np.random.binomial(n, p)

    return cut_off_position


def drop_from_left_stack(n_left: int, n_right: int) -> bool:
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


def riffle_shuffle(deck: Deck, p:float = 0.5) -> Deck:
    cutoff_position: int = get_cutoff_position(deck, p=p)
    
    left_stack: deck = deck[:cutoff_position]
    right_stack: deck = deck[cutoff_position:]

    n_left: int = len(left_stack)
    n_right: int = len(right_stack)

    pile = Deck()

    while left_stack or right_stack:
        if drop_from_left_stack(n_left, n_right):
            card_to_drop = left_stack.pop()
            pile.cards.append(card_to_drop)
            n_left -= 1
        else:
            card_to_drop = right_stack.popleft()
            pile.cards.append(card_to_drop)
            n_right -= 1

    return pile


def a_shuffle(deck: Deck, a: int) -> Deck:
    ...


if __name__ == "__main__":
    number_of_cards_in_deck = 52
    deck = Deck()
    deck = deck.init_new_deck(number_of_cards_in_deck)
    
    # test if cut off position is a valid number
    cutoff_position = get_cutoff_position(deck)
    assert cutoff_position > 0 and cutoff_position <= number_of_cards_in_deck

    
    # test if the shuffled pile contains the exact same number of cards as the original pilt
    # test if not all the positions of cards in the shuffled pile are in the same position as the original deck
    pile = riffle_shuffle(deck)
    assert len(pile) == number_of_cards_in_deck
    assert sum(o == s for o,s in zip(deck, pile)) != number_of_cards_in_deck