import random 
from funcs_data.data import EXT_UI_ELEMENTS

GLOBAL_HEALTH = 150
GLOBAL_DAMAGE = 25

costumers_info = EXT_UI_ELEMENTS["costumers"]
GLOBAL_COSTUMER = random.choice(costumers_info["paths"])

print(GLOBAL_COSTUMER)


GLOBAL_DIST_MAX = (20, 30)
GLOBAL_DISTANCE = random.randint(GLOBAL_DIST_MAX[0], GLOBAL_DIST_MAX[1])

GLOBAL_PIZZA_TIME = random.randint(30, 120)