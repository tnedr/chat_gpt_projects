import os

path = "/path/to/some/folder1"

# Split the path into directory and folder name
directory, folder = os.path.split(path)
print(directory)
print(folder)
# Get the parent directory by dropping the last folder
parent_directory = os.path.dirname(directory)
print(parent_directory)
# Create the new path with the parent directory
new_path = os.path.join(parent_directory, folder)
print(new_path)