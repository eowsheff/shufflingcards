from collections import deque 
from copy import deepcopy
from itertools import islice
import numpy as np
import types


# from typing import Self


class Deck:
    """
    This class simulates a deck of cards.

    A Deck object holds cards. The cards can be evaluated by calling Deck.cards, or Deck[slice], e.g. Deck[1:5]
    :param cards: A deque object holding a sequence of subsequent cards. This simulates the cards in a deck.
    """
    def __init__(self, cards: deque = None) -> None:
        """
        Init the Deck object with or without cards. 
        The cards param takes a deque object, which reflects the order of cards in a deck. 
        E.g.: 
            For a deck of 4 cards, in standard order, the Deck object will be initiated with Deck(deque([1,2,3,4])).
        
        If the Deck is initiated without any cards, an empty deque object is assigned to self.cards. A new deque of 'cards' can be assigned to Deck.cards
        at any time.
        E.g.: 
            d = Deck()
            c = deque([1,2,3,4,5])
            d.cards = c

        To initiate a new deck, with a new sequence of cards in standard order; use function `init_new_deck(number_of_cards)`.
        E.g.:
            To initiate a new deck, with standard 52 cards, use:
                d = Deck().init_new_deck(52)
        
                
        :param cards: A deque object holding a sequence of subsequent cards. This simulates the cards in a deck.

        :return None
        """

        if not cards:
            # cards is a deque object, as deque allows for easy and fast item selection on either end of the sequence (with O(1) time complexity).
            self._cards: deque = deque()
        else:
            self._cards: deque = cards


    def __len__(self) -> int:
        """
        When calling len(Deck), it will return the number of cards in the self.cards object. This allows the user to easily, and in a Pythonic way, 
        access the number of cards in the Deck.

        
        :param None

        :return the length of self.cards as an integer
        """
        return len(self.cards)
    
    
    def __repr__(self) -> repr:
        """
        When the user wants to print the Deck object to the std.out, it will print the sqeuence of cards in self.cards, representing the ordering
        of the cards in the deck.

        E.g.:
            d = Deck()
            d.cards = deque([1,2,3,4])
            print(d)
            std.out: shows: deque([1,2,3,4])


        :param None

        :return repr(self.cards), to show the sequence of cards in self.cards    
        """
        
        return repr(self.cards)
    
    def __getitem__(self, index) -> deque:
        """
        Cards in Deck object can be accesses by using indexes, or slices on the Deck object itself. 
        __getitem__ will check if the user has used a slice or just one index and return the requested cards from self.cards, in a new Deck object.

        E.g.: to access the first index card:
            d = Deck().init_new_deck(52)
            first_card = d[0]
        
        E.g. to access the first 3 cards:
            d = Deck().init_new_deck(52)
            first_three_cards = d[:3]

        Note: this will return a new Deck object! 
        Note: this used Python indexing, not the numbering of the cards! 

        
        :param: index: the index, or slice which will slice the self.cards object

        :return Deck: a new deck object with the cards that are selected through the user input 
        """
        if isinstance(index, slice):
            packet: Deck = Deck()
            packet.cards = deque(islice(self.cards, index.start, index.stop))
            return packet
        else:
            return self.cards[index]
        
        
    def __getattr__(self, name):
        """
        When calling a function or attribute of an instance of Deck, this function will check of the function/attribute is part of Deck.
        If it's present in the Deck class, it will call the function or attribute on the Deck instance like it normally would.
        If it's not part of the Deck class, it will call the function or attribute on self.cards, the deque object. This allows the user to directly call
        deque functionalities on the Deck object.

        E.g.: calling a function that is part of the Deck object
            d = Deck()
            d.init_new_deck(52)     --> calls function init_new_deck() because it's part of the Deck object

        E.g.: calling a function that is NOT part of the Deck object
            d = Deck().init_new_deck(52)
            d.popleft()             --> popleft() is not part of the Deck object. It is part of the self.cards deque object. So it's called on self.cards

        :param name: of attribute or function that is called
        :return function or attribute from Deck object or collections.deque object
        """
        if name == "__setstate__":
            raise AttributeError(name)
        
        if hasattr(Deck, name):
            return super(Deck, self).__getattribute__(name)
        else:
            f = getattr(self.cards, name)
            if isinstance(getattr(self.cards, name), types.FunctionType):
                f = f()
            return f

    
    def init_new_deck(self, number_of_cards: int =52): # add type hinting
        """
        This function initiates a new sequence of cards as a deque object. It initiates a sequence of n `number_of_cards`, and puts these in standard order.
        E.g.:
            d = Deck()
            d.init_new_deck(52)
            d.cards <- now holds a deque object with a sequence of [1,2,3...,52] cards

        :param number_of_cards: the number of cards in the deck of cards. In standard order, from low to high
        :return self: this object returns itself. 
        """
        self.cards = deque(range(1, number_of_cards + 1))
        return self
    
    @property
    def cards(self):
        """
        Property which returns the attribute self._cards, which holds a sequence of numbers, representing cards in a deck
        Usage: when for an instance of a Deck `d`, d.cards is called, it calls this property and returns self._cards

        :param  None
        :return self._cards, a collections.deque object which represents the cards in a deck
        """
        return self._cards
    

    @cards.setter
    def cards(self, c):
        """
        This setter ensures that when a list is assigned to Deck.cards, it is converted to a collections.deque object.

        E.g.:
            c = [1,2,3,4]
            d = Deck()
            d.cards = c  # c is a list here. This setter ensures its converted to collections.deque before setting it to self._cards
            # such that: type(d.cards) is collections.deque

        :param  c:  a sequence of numbers representing a sequence of cards
        return  None: this setter does not return anything. It sets self.cards to c.
        """
        if isinstance(c, list):
            c = deque(c)
        
        self._cards = c

        return self._cards


    @property
    def rising_sequences(self) -> int:
        """
        This property/attribute can be called on an instance of Deck, it will return the number of rising sequences in self._cards (as an integer).
        
        :param  None
        :return number of rising sequences in self._cards, as int 
        """
        cards = np.array(self.cards)
        inv_order = np.argsort(cards)
        return sum(np.diff(inv_order) < 0) + 1
    
    
    def copy(self):
        """
        Returns a copy of the instance of a Deck. Including a copy of the self.cards deque object and all of the elements (cards) within self.cards
        
        :param  None
        :return Deck object, with a new id and memory allocation, all attributes from the original Deck also have a new id and memory allocation
        """
        return deepcopy(self)


if __name__ == "__main__":
    # Unit tests
    d = Deck()

    # Assert the correct number of rising sequences
    d.cards = deque([1, 2, 4, 3, 5])
    assert d.rising_sequences == 2

    d.cards = deque([3,4,1,5,7,6,2,3,8,9,10])
    assert d.rising_sequences == 4
    
    d.init_new_deck(52)
    assert d.rising_sequences == 1
    d.cards.reverse()
    assert d.rising_sequences == 52

    # Assert the correct len of the deck of cards AND check if __getattr__ calls the correct order of functions/attributes 
    org_len = len(d)
    d.popleft()
    assert org_len == len(d) + 1