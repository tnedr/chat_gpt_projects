import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import logging

np.random.seed(42)
logging.basicConfig(level=logging.INFO)
MAX_VAL = 10000

width, height = 50, 100
width, height = 100, 20

erosion_map = np.zeros((height, width))

def add_drop(x, y):
    erosion_map[y, x] += 1

def move_drop(x, y, erosion_factor):
    logging.debug(f"Current position: ({x}, {y})")

    # Calculate neighboring values
    down_left2 = erosion_map[y + 1, x - 2] if x > 1 else MAX_VAL
    down_left = erosion_map[y + 1, x - 1] if x > 0 else MAX_VAL
    down = erosion_map[y + 1, x]
    down_right = erosion_map[y + 1, x + 1] if x < width - 1 else MAX_VAL
    down_right2 = erosion_map[y + 1, x + 2] if x < width - 2 else MAX_VAL

    directions = [down_left2, down_left, down, down_right, down_right2]
    max_val = max(directions)

    # Calculate probabilities based on Gaussian distribution and erosion factor
    probabilities = np.array([norm.pdf(x, max_val, erosion_factor) for x in directions])
    probabilities = probabilities / np.sum(probabilities)

    # Normalize probabilities with a small epsilon value
    epsilon = 1e-8
    if not np.isclose(np.sum(probabilities), 1.0, atol=epsilon):
        probabilities /= np.sum(probabilities)

    logging.debug(f"Probabilities: {probabilities}")
    new_x = np.random.choice([x - 2, x - 1, x, x + 1, x + 2], p=probabilities)
    new_y = y + 1

    return new_x, new_y

num_drops = 10000
start_x = width // 2

erosion_factor = 20  # Adjust this value to control the erosion effect

for i in range(num_drops):
    logging.info(f"Drop: {i}")
    x, y = start_x, 0
    while y < height - 1:
        add_drop(x, y)
        x, y = move_drop(x, y, erosion_factor)

plt.imshow(erosion_map, cmap='viridis', origin='lower')
plt.colorbar()
plt.show()
