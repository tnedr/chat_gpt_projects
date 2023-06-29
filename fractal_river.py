import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# initial terrain and water matrices
terrain = np.random.rand(100, 100)
water = np.zeros_like(terrain)

# parameters
rain_per_turn = 0.1
evaporation_rate = 0.99
gravity = 0.5
num_iterations = 100000

# create figure for plotting
fig, ax = plt.subplots()
im = ax.imshow(terrain, cmap='terrain')

def update(i):
    global terrain, water

    # erosion simulation
    water += rain_per_turn
    erosion = np.minimum(water, terrain) * 0.01
    terrain -= erosion
    water -= erosion
    water *= evaporation_rate
    water_diff = np.roll(water, 1, axis=0) - water
    water += gravity * water_diff

    # update image
    im.set_array(terrain)
    ax.set_title(f"Iteration: {i}")
    return [im]

# create animation
ani = FuncAnimation(fig, update, frames=num_iterations, blit=True)

plt.show()
