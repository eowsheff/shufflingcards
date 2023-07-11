from card import Card
from collections import deque 
from itertools import islice
# from typing import Self

class Deck:
    def __init__(self, cards: deque = None) -> None:
        if not cards:
            self.cards = deque()
        else:
            self.cards = cards

    def __len__(self) -> int:
        return len(self.cards)
    
    def __repr__(self) -> repr:
        return repr(self.cards)
    
    def __getitem__(self, index) -> deque:
        if isinstance(index, slice):
            return deque(islice(self.cards, index.start, index.stop))
        else:
            return self.cards[index]
    
    def init_new_deck(self, number_of_cards: int =52): # add type hinting
        for i in range(1, number_of_cards+1):
            card = Card(i)
            self.cards.append(card)
        return self
    
    @property
    def rising_sequences(self):
        ...
    
if __name__ == "__main__":
    print(Deck())