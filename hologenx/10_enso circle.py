import matplotlib.pyplot as plt
import numpy as np

# Parameters
gap_location = 120  # Angle where the gap starts in degrees
gap_width = 30  # Angle width of the gap in degrees
direction = "clockwise"  # Direction can be "clockwise" or "counter-clockwise"
line_thickness_start = 20
line_thickness_end = 4
easing_exponent = 2  # Change this value to control the speed of thickness change
decay_rate = 5  # Change this value to control the speed of thickness change in the exponential model
num_points = 500

# Calculate gap start and end
gap_start = gap_location - gap_width / 2
gap_end = gap_location + gap_width / 2

# Calculate starting and ending points in degrees
if direction == "clockwise":
    start1, end1 = gap_end, 360
    start2, end2 = 0, gap_start
else:
    start1, end1 = gap_start, 0
    start2, end2 = 360, gap_end

# Generate circle points
theta1 = np.linspace(start1, end1, num_points//2)
theta2 = np.linspace(start2, end2, num_points//2)
theta = np.concatenate([theta1, theta2])
theta = np.radians(theta)

# Generate coordinates
x = np.sin(theta)
y = np.cos(theta)

# Create variable line thickness with easing
t = np.linspace(0, 1, len(theta))
line_thickness = line_thickness_start + (line_thickness_end - line_thickness_start) * np.power(t, easing_exponent)
line_thickness = line_thickness_start + (line_thickness_end - line_thickness_start) * np.exp(-decay_rate * t)

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
