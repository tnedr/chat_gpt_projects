import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Replaceable dictionary for color palettes
palettes = {
    'Extended Modern and Tech-Savvy with Life and Energy': [
        ("Dark Blue", (3, 37, 65)),
        ("Teal", (0, 128, 128)),
        ("Silver", (192, 192, 192)),
        ("Steel Blue", (70, 130, 180)),
("Forest Green", (34, 139, 34)),

        ("Charcoal", (54, 69, 79)),
        ("Slate Grey", (112, 128, 144)),
        ("Goldenrod", (218, 165, 32)),
('Maroon', (128, 0, 0)),
("Scarlet 'Orange'", (255, 36, 0)),
("Fire Engine Red", (206, 32, 41)),
        ("Coral", (255, 127, 80)),
        ("Racing Red", (211, 0, 0))]
}

palettes = {
    'third color': [
        ('Vivid Blue', (0, 123, 255)),
    ('Emerald Green', (0, 128, 0)),
    ('Crimson Red', (220, 20, 60)),
    ('Golden Yellow', (255, 215, 0)),
    ('Electric Purple', (128, 0, 128)),
    ('Deep Teal', (0, 128, 128)),
    ('Electric Blue1', (125, 249, 255)),
    ('Electric Blue2', (44, 117, 255))
     ]
}

palettes = {
    'third color': [
('Electric Blue2', (44, 117, 255)),
('Complementary Orange', (255, 155, 44)),
('Near-Complementary Coral', (255, 127, 80)),
('Split-Complementary Colors Orange-Red', (255, 69, 0)),
('Orange-Yellow', (255, 165, 0)),
('Lighter Blue Analogous Colors', (135, 206, 250)),
('Darker Blue Analogous Colors', (0, 0, 128))
]
}


# Initialize the plot
fig, ax = plt.subplots(figsize=(14, 10))

# Initialize variables for layout
row_height = 1
row_start = 0

# Loop through each palette and plot the color boxes
for palette_name, colors in palettes.items():
    col_start = 0
    for color_name, rgb in colors:
        # Create a rectangle (color box)
        rect = patches.Rectangle((col_start, row_start), 1, row_height, linewidth=1, edgecolor='none', facecolor=[x/255.0 for x in rgb])

        # Add the rectangle to the plot
        ax.add_patch(rect)

        # Annotate the color box with the color name and RGB values
        text = f"{color_name}\n{rgb}"
        plt.text(col_start + 0.5, row_start + 0.5, text, ha='center', va='center', fontsize=12)

        col_start += 1.5  # Move to the next column position

    # Annotate the row with the palette name
    plt.text(-1.5, row_start + 0.5, palette_name, ha='center', va='center', fontsize=12)

    row_start -= 2  # Move to the next row position

# Set axis properties and show the plot
ax.set_xlim(-2, len(max(palettes.values(), key=len)) * 1.5)
ax.set_ylim(-2 * len(palettes), 1)
ax.axis('off')
plt.show()
