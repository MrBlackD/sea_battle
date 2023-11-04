import random

def random_number(low_bound, high_bound):
    return int(low_bound + random.random() * (high_bound + 1))
