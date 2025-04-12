class Pin: 
    def __init__(self, grid, side: int, pin_num: int, region_id: int=None):
        self.__side = side
        self.__pin_num = pin_num
        self.__alive = False
        self.__grid = grid
        
    def __repr__(self):
        return f"Pin(pin_num={self.__pin_num}, side={self.__side}, alive={self.__alive})"
    
  
    def is_alive(self) -> bool:
        return self.__alive
    
    def revive(self):
        self.__alive = True

    def kill(self):
        self.__alive = False


    @staticmethod
    def generate_pins(n: int):
        return [Pin(None, None, i) for i in range(n)]

    @staticmethod
    def set_all_pins(pins:list["Pin"], grid, side):
        for pin in pins:
            pin.set_grid(grid)
            pin.set_side(side)


    def set_grid(self, grid):
        if self.__grid is not None:
            raise ValueError("Grid already set. Cannot modify.")
        self.__grid = grid
        
    def set_side(self, side):
        if self.__side is not None:
            raise ValueError("Side already set. Cannot modify.")
        if side not in (0, 1):
            raise ValueError("Invalid side. Choose from 0 or 1.")
        self.__side = side
        
