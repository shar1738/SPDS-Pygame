class GameState:
    def __init__(self):

        self.ex_health = 150
        self.ex_health_index = -1
        self.ex_health_frame = None

        self.ex_remaining_time = None
        self.ex_time_frame = None

    
        self.holes = []

        self.current_level = {"Exterior", "Interior", "MiniGame"}
        self.has_interior_ran = False