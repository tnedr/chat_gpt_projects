import os


# prompt = '''
# Hi ChatGPT,
# I will be providing you with Python codes in slices. Each slice will contain a part of a Python file or multiple Python files, and will be limited to a maximum size of 4000 characters.
# To help you understand the slices and the Python files, I will be using different markers. The "[START FILE]" marker will indicate the beginning of a new Python file in the slice, and the "[START SLICE]" marker will indicate the beginning of a new slice for a Python file. Similarly, the "[CONTINUE FILE]" marker and the "[CONTINUE SLICE]" marker will indicate that the slice or file continues from the previous slice.
# When you receive a slice, please acknowledge it by saying "OK". There is no need to summarize the contents of the slice.
# Note that only Python files in the directory will be sliced, and a summary of the sliced files will be provided in the beginning of the first slice. The summary will be enclosed between the "[SUMMARY]" marker and the "[END SUMMARY]" marker.
# When you receive the last slice, please say "OK, I see that the input is finished".
# Let me know if you have any questions.
# '''

prompt = '''
Hi ChatGPT,
I will be providing you with Python codes in slices. Each slice will contain a part of a Python file or multiple Python files, and will be limited to a maximum size of 4000 characters.
To help you understand the slices and the Python files, I will be using different markers. The "[START FILE]" marker will indicate the beginning of a new Python file in the slice, and the "[START SLICE]" marker will indicate the beginning of a new slice for a Python file. Similarly, the "[CONTINUE FILE]" marker and the "[CONTINUE SLICE]" marker will indicate that the slice or file continues from the previous slice.
When you receive a slice, please acknowledge it by saying "OK". There is no need to summarize the contents of the slice.
Note that only Python files in the directory will be sliced, and a summary of the sliced files will be provided in the beginning of the first slice. The summary will be enclosed between the "[SUMMARY]" marker and the "[END SUMMARY]" marker.
Please do not provide any additional information or commentary, except to say "OK" to acknowledge each slice, and "OK, I see that the input is finished" to indicate that the input is complete.
Let me know if you have any questions.
'''

# Define the directory where the Python files are located
folder_path = "C:/Users/Tamas/PycharmProjects/volatility_pumping"

# Define the name and path of the output file
output_folder = "output_folder"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_file = os.path.join(output_folder, "combined_files.txt")

# Set the maximum size of each slice
max_slice_size = 4000

# Loop through all the files in the folder and combine their contents into one file
with open(output_file, "w") as combined_file:
    next_file = None
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                # Read the contents of the file
                file_contents = file.read()
                # Add the slice markers to the contents
                if next_file is None:
                    combined_file.write(f"[START FILE] {filename}: {file_contents} [CONTINUE FILE]\n")
                else:
                    combined_file.write(f"[START SLICE] {filename}: {file_contents} [CONTINUE SLICE] [NEXT FILE: {next_file}]\n")
                # Set the next_file variable to indicate the filename of the next Python file
                next_file = filename

# Slice the combined file into smaller files
slice_number = 1
with open(output_file, "r") as combined_file:
    while True:
        # Read a chunk of the combined file
        chunk = combined_file.read(max_slice_size)
        # Break out of the loop if there is no more data
        if not chunk:
            break
        # Add the slice markers to the chunk
        if len(chunk) < max_slice_size:
            chunk += " [END SLICE]\n"
        else:
            chunk += " [CONTINUE SLICE]\n"
        # Construct a unique filename for the slice based on the original filename and slice number
        slice_filename = f"combined_files_slice{slice_number}.txt"
        # Open the slice file for writing
        slice_path = os.path.join(output_folder, slice_filename)
        with open(slice_path, "w") as slice_file:
            # Add a summary section to the beginning of the first slice
            if slice_number == 1:
                slice_file.write(f"[SUMMARY] Sliced Python files: {[f for f in os.listdir(folder_path) if f.endswith('.py')]} [END SUMMARY]\n\n")
            slice_file.write(chunk)
        # Increment the slice number
        slice_number += 1
