class Case:
    def __init__(self, position: tuple[int, int]):
        self.pos = position
        self.__case_side = None     # either a 0 or 1, to indicate 
                                    # the player it bellongs to, if no color is set,this value is set to None
        self.__protection_turn = -1 
        self.__pin = None
        

    def __repr__(self):
        return f"Case(case_id={self.pos}, side={self.case_side}, empty={self.is_empty()})"
    
    @property 
    def case_side(self):
        return self.__case_side
    
    @case_side.setter
    def case_side(self, side: int):
        if side not in (0, 1) and side is not None:
            raise ValueError("Invalid side. Choose from 0 or 1 or None.")
        self.__case_side = side

    def protected(self, turn: int) -> bool:
        if turn - self.__protection_turn <= 2:
            return True
        return False
     
    def is_empty(self) -> bool:
        return self.__pin is None
    
    def eliminate(self):
        self.__pin = None
    
    def set_pin(self, pin):
        if self.__pin is not None:
            raise ValueError("Pin already set. Cannot modify.")
        self.__pin = pin

    
    def get_pin(self):
        return self.__pin
    

    def remove_pin(self):
        if self.__pin is None:
            raise ValueError("Pin not set. Cannot modify.")
        self.__pin = None
    

    def protect(self, turn: int):
        self.__protection_turn = turn 
   