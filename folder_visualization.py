import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Define the directory you want to visualize
directory = "C:/Users/Tamas/PycharmProjects"

# Define a function to check if a folder is empty
def is_empty_folder(folder_path):
    for _, dirnames, filenames in os.walk(folder_path):
        if dirnames or filenames:
            return False
    return True

# Define a function to find empty folders
def find_empty_folders(parent_folder):
    empty_folders = []
    for folder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder)
        if os.path.isdir(folder_path) and is_empty_folder(folder_path):
            empty_folders.append(folder_path)
    return empty_folders

# Get the list of empty folder paths
empty_folder_paths = find_empty_folders(directory)

# Create a DataFrame to store the empty folder paths
empty_folders_df = pd.DataFrame(empty_folder_paths, columns=['Empty Folder Path'])

# Save the DataFrame to a CSV file
empty_folders_df.to_csv('empty_folders.csv', index=False)

# Print the DataFrame
print(empty_folders_df)

# Define a function to recursively calculate the size, number of files, and number of subfolders of each folder
def get_folder_info(parent_folder):
    folder_sizes = {}
    folder_files = {}
    folder_subfolders = {}
    for folder in os.listdir(parent_folder):
        print(f"Processing folder: {folder}")
        folder_path = os.path.join(parent_folder, folder)
        if os.path.isdir(folder_path):
            size = 0
            files_count = 0
            subfolders_count = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    size += os.path.getsize(os.path.join(dirpath, filename))
                    files_count += 1
                subfolders_count += len(dirnames)
            folder_sizes[folder] = size
            folder_files[folder] = files_count
            folder_subfolders[folder] = subfolders_count
    return folder_sizes, folder_files, folder_subfolders

# Call the function to get the folder sizes, number of files, and number of subfolders
folder_sizes, folder_files, folder_subfolders = get_folder_info(directory)

# Filter out folders with a size of 0 bytes
non_empty_folders = {folder: size for folder, size in folder_sizes.items() if size > 0}

folder_sizes_filtered = {folder: non_empty_folders[folder] for folder in non_empty_folders}
folder_files_filtered = {folder: folder_files[folder] for folder in non_empty_folders}
folder_subfolders_filtered = {folder: folder_subfolders[folder] for folder in non_empty_folders}

# Normalize the number of files and subfolders to a range between 0 and 1
max_files = max(folder_files_filtered.values())
normalized_files = [files_count / max_files for files_count in folder_files_filtered.values()]

max_subfolders = max(folder_subfolders_filtered.values())
normalized_subfolders = [subfolders_count / max_subfolders for subfolders_count in folder_subfolders_filtered.values()]

# Generate colors based on the normalized number of files
colors = plt.cm.Blues(normalized_files)

# Define border widths based on the normalized number of subfolders
border_widths = [0.5 + 4 * norm_subfolders for norm_subfolders in normalized_subfolders]

# Define the data for the plot
sizes = list(folder_sizes_filtered.values())
labels = [f"{folder}\nSize: {size / (1024 * 1024):.2f} MB\nFiles: {folder_files_filtered[folder]}\nSubfolders: {folder_subfolders_filtered[folder]}" for folder, size in folder_sizes_filtered.items()]

# Create the plot and display it
fig, ax = plt.subplots()
rectangles = squarify.plot(sizes=sizes, ax=ax, color=colors, alpha=0.7, linewidth=border_widths, edgecolor='white')

# Add text labels
for r, label, size, files, subfolders in zip(rectangles.get_children(), non_empty_folders, sizes, folder_files_filtered.values(), folder_subfolders_filtered.values()):
    x, y, w, h = r.get_xy()[0], r.get_xy()[1], r.get_width(), r.get_height()
    ax.text(x + w / 2, y + h / 2 + h / 4, label, color='red', ha='center', va='center')
    ax.text(x + w / 2, y + h / 2 + h / 8, f"Size: {size / (1024 * 1024):.2f} MB", color='black', ha='center', va='center')
    ax.text(x + w / 2, y + h / 2, f"Subfolders: {subfolders}", color='black', ha='center', va='center')
    ax.text(x + w / 2, y + h / 2 - h / 8, f"Files: {files}", color='black', ha='center', va='center')

ax.set_title("Folder Structure")
ax.axis("off")
plt.show()




