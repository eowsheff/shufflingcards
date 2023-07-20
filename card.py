class Card:

    def __init__(self, value: int) -> None:
        self.value: int = value
    
    def __repr__(self):
        return repr(self.value)
