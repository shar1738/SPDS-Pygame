class GameState:
    def __init__(self):
        self.player_health = 150
        self.health_index = 1
        self.remaining_time = None
        self.current_customer = None
        self.holes = []
        self.current_level = {"Exterior", "Interior", "MiniGame"}