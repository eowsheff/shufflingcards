import numpy as np
from deck import Deck

def top_in_at_random(deck: Deck, copy: bool = False) -> Deck:
    """
    This function blabla
    """
    if copy:
        original_cards = deck.cards.copy()
        deck = Deck()
        deck.cards = original_cards

    number_of_cards = len(deck)

    for i in range(number_of_cards):
        top_card = deck.cards.pop()
        idx_to_insert_card = np.random.randint(0, 52)
        deck.cards.insert(idx_to_insert_card, top_card)
    
    return deck



if __name__ == "__main__":
    cards_in_deck = 52

    first_deck = Deck().init_new_deck(cards_in_deck)
    shuffled_first_deck = top_in_at_random(first_deck)
    assert first_deck is shuffled_first_deck

    second_deck = Deck().init_new_deck(52)
    new_shuffled_deck = top_in_at_random(second_deck, copy=True)
    assert new_shuffled_deck is not second_deck
    assert sum(o == s for o,s in zip(new_shuffled_deck.cards, second_deck.cards)) != cards_in_deck