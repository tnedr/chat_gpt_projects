import os
import re
import pyperclip

def write_split_file(lines, basename, output_dir, file_num, is_last_file):
    file_path = os.path.join(output_dir, f'{basename}_{file_num}.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

        # Add the message at the end of the split file only if it's not the last file
        if not is_last_file:
            f.write("I will provide more information about the thesis in the next message. Please wait.\n")

def write_splitted_files(thesis_path, output_dir, max_tokens_per_file):
    current_file_tokens = 0
    current_file_lines = []
    current_file_num = 1

    base_name = os.path.basename(thesis_path)  # Get the filename with extension
    basename = os.path.splitext(base_name)[0]

    with open(thesis_path, 'r', encoding='utf-8') as thesis_file:

        for line in thesis_file:
            line_tokens = len(line.split())
            current_file_lines.append(line.rstrip('\n'))

            # Check if adding the current line to the file would exceed max_tokens_per_file
            if current_file_tokens + line_tokens > max_tokens_per_file:
                is_last_file = False
                write_split_file(current_file_lines, basename, output_dir, current_file_num, is_last_file)
                current_file_tokens = 0
                current_file_lines = []
                current_file_num += 1
            current_file_tokens += line_tokens
    # Write the last file with the remaining content
    if current_file_lines:
        is_last_file = True
        write_split_file(current_file_lines, basename, output_dir, current_file_num, is_last_file)

def iterate_over_result_file_to_the_clipboard(directory):
    # Set the directory path and suffix pattern to search for
    suffix_pattern = r"_\d+\.txt$"

    # Compile the suffix pattern into a regular expression object
    suffix_regex = re.compile(suffix_pattern)
    # Get a list of all .txt files in the directory that match the suffix pattern
    txt_files = [file for file in os.listdir(directory) if suffix_regex.search(file)]

    # Iterate over each file and copy its contents to the clipboard
    for file in txt_files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            file_contents = f.read()
            pyperclip.copy(file_contents)
        print(f"I have copied {file} into the clipboard.")
        continue_input = input("Press 'y' to continue to the next file or any other key to stop: ")
        if continue_input.lower() != 'y':
            break

if __name__ == "__main__":
    # thesis_path = input("What is the path of the thesis? ")
    thesis_path = 'C:/Users/tamas/PycharmProjects/chat_gpt_projects/input/hfs.txt'
    max_token_length = 1000
    output_dir = './output/'
    print("Generating text files...")
    write_splitted_files(thesis_path, output_dir, max_token_length)
    print("Done.")
    iterate_over_result_file_to_the_clipboard(output_dir)
