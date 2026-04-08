import random

seed_str = input("Enter a seed: ")
try:
    seed = int(seed_str)
    random.seed(seed)
    rand_num = random.random()
    print(f"Random number: {rand_num}")
except ValueError:
    print("Invalid seed, must be an integer")