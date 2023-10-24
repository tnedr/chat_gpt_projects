import matplotlib.pyplot as plt
import numpy as np
from noise import pnoise1

# Parameters
params = {
    'gap_location': 130,
    'gap_width': 40,
    'direction': "clockwise",
    'line_thickness_start': 20,
    'line_thickness_end': 4,
    'num_points': 500,
    'linechange': 'exponential',
    'thickness_params': {'exponential': 2, 'logarithmic': 1, 'sigmoid': 0.10}
}

# Function to calculate line thickness based on model
def calculate_thickness(t, start, end, model, params):
    if model == 'linear':
        return start + (end - start) * t
    elif model == 'exponential':
        exp = params['exponential']
        return start + (end - start) * np.power(t, exp)
    elif model == 'logarithmic':
        c = params['logarithmic']
        return start + (end - start) * np.log(c * t + 1)
    elif model == 'sigmoid':
        lam = params['sigmoid']
        return start + (end - start) / (1 + np.exp(-lam * (t - 0.5)))

# Calculate gap start and end
gap_start = params['gap_location'] - params['gap_width'] / 2
gap_end = params['gap_location'] + params['gap_width'] / 2

# Calculate starting and ending points in degrees
if params['direction'] == "clockwise":
    start1, end1 = gap_end, 360
    start2, end2 = 0, gap_start
else:
    start1, end1 = gap_start, 0
    start2, end2 = 360, gap_end

# Generate circle points
theta1 = np.linspace(start1, end1, params['num_points'] // 2)
theta2 = np.linspace(start2, end2, params['num_points'] // 2)
theta = np.concatenate([theta1, theta2])
theta = np.radians(theta)


# Introduce a function to generate noise
def generate_noise(length, amplitude):
    return (np.random.rand(length) - 0.5) * amplitude

# Introduce a function to generate Perlin noise
def perlin_noise(theta, scale=5, octaves=3, persistence=0.5, lacunarity=2.0, base=0.0):
    return np.array([pnoise1(int(t * scale), octaves=int(octaves), persistence=persistence, lacunarity=lacunarity, base=int(base)) for t in theta])

# Calculate Perlin noise values for the circle
noise_values = perlin_noise(theta)

# Modify the circle's radius based on the Perlin noise
radius = 1.0 + 0.05 * noise_values  # Adjust the 0.05 multiplier for more or less noise

# Generate coordinates with noise
x = np.sin(theta) * radius
y = np.cos(theta) * radius

# Apply noise to x and y coordinates
noise_amplitude = 0.002  # Adjust this value for more or less noise
x += generate_noise(len(x), noise_amplitude)
y += generate_noise(len(y), noise_amplitude)


# Create variable line thickness
t = np.linspace(0, 1, len(theta))
line_thickness = calculate_thickness(t, params['line_thickness_start'], params['line_thickness_end'], params['linechange'], params['thickness_params'])

# Plot
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')

for i in range(len(x) - 1):
    ax.plot([x[i], x[i+1]], [y[i], y[i+1]], linewidth=line_thickness[i], color='black')

# Remove axes
ax.axis('off')

# Save as SVG
plt.savefig("enso_logo.svg", format="svg")

# Show plot
plt.show()
