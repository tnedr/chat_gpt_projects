import os
import re
import pyperclip


def write_structure_file(root_dir, output_dir):
    basename = os.path.basename(os.path.normpath(root_dir))
    structure_file_path = os.path.join(output_dir, f'{basename}_structure.txt')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(structure_file_path, 'w') as f:
        f.write(f'I have a project called {basename}\n')
        f.write(f'It is located at {os.path.abspath(root_dir)}\n')
        f.write('This is the project structure\n')
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', '.idea']]
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}{os.path.basename(root)}/\n')
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                if file.endswith('.py'):
                    f.write(f'{subindent}{file}\n')
    return structure_file_path


def create_module_file_list(root_dir, max_token_length):
    module_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                if not content.strip():
                    content = "This Python file is blank."
                if (token_count := len(content.split())) > max_token_length:
                    raise ValueError(f"Module '{path}' has too many tokens ({token_count}) to fit in one text file.")
                prefix = f"ok this is the content of {file} module located at {os.path.abspath(path)}:\n"
                content = [prefix + line if i == 0 else line for i, line in enumerate(content)]
                module_files.append((path, content))
    return module_files
def write_code_jumbo_file(module_files, output_dir):
    basename = os.path.basename(os.path.normpath(root_dir))
    jumbo_file_path = os.path.join(output_dir, f'{basename}_codes.txt')

    with open(jumbo_file_path, 'w') as f:
        for path, content in module_files:
            f.write(''.join(content))
            f.write('\n')
    return jumbo_file_path



def write_split_file(modules, output_dir, structure_file_path, file_num, is_last_file):
    basename = os.path.basename(os.path.normpath(root_dir))
    file_path = os.path.join(output_dir, f'{basename}_{file_num}.txt')

    with open(file_path, 'w') as f:
        if file_num == 1:
            with open(structure_file_path, 'r') as structure_file:
                f.write(structure_file.read())
                f.write("And in the following, I give the modules of the project:\n")

        for module in modules:
            lines = module.split('\n')
            for i, line in enumerate(lines):
                if i == 0:
                    f.write(line + '\n')
                else:
                    indent_level = len(line) - len(line.lstrip())
                    indent = ' ' * indent_level
                    if line.strip():
                        f.write(indent + line.lstrip() + '\n')
                    else:
                        f.write('\n')

        # Add the message at the end of the split file only if it's not the last file
        if not is_last_file:
            f.write("I will provide more information about the project in the next message. Do not say anything now, just OK\n")


def write_splitted_files(code_file_path, output_dir, structure_file_path, max_tokens_per_file):
    current_file_tokens = 0
    current_file_modules = []
    current_module_lines = []
    current_file_num = 1

    total_modules = 0
    with open(code_file_path, 'r') as jumbo_file:
        for line in jumbo_file:
            if line.startswith('ok this is the content of'):
                total_modules += 1

    processed_modules = 0
    with open(code_file_path, 'r') as jumbo_file:
        for line in jumbo_file:
            line_tokens = len(line.split())
            current_module_lines.append(line.rstrip('\n'))

            # Check if the current line marks the end of a module
            if line.startswith('ok this is the content of') and current_module_lines[:-1]:
                module_tokens = sum(len(line.split()) for line in current_module_lines[:-1])
                processed_modules += 1
                is_last_module = processed_modules == total_modules

                # Check if adding the current module to the file would exceed max_tokens_per_file
                if current_file_tokens + module_tokens > max_tokens_per_file or is_last_module:
                    is_last_file = is_last_module
                    write_split_file(current_file_modules, output_dir, structure_file_path, current_file_num, is_last_file)
                    current_file_tokens = 0
                    current_file_modules = []
                    current_file_num += 1

                current_file_tokens += module_tokens
                current_file_modules.extend(current_module_lines[:-1])
                current_module_lines = [current_module_lines[-1]]

    # Write the last file with the remaining content
    if current_file_modules:
        is_last_file = True
        write_split_file(current_file_modules, output_dir, structure_file_path, current_file_num, is_last_file)


def write_all_files(root_dir, output_dir, max_token_length, max_tokens_per_file):
    structure_file_path = write_structure_file(root_dir, output_dir)
    module_files = create_module_file_list(root_dir, max_token_length)
    jumbo_file_path = write_code_jumbo_file(module_files, output_dir)
    write_splitted_files(jumbo_file_path, output_dir, structure_file_path, max_tokens_per_file)

def iterate_over_result_file_to_the_clipboard(directory):

    # Set the directory path and suffix pattern to search for
    suffix_pattern = r"_\d+\.txt$"

    # Compile the suffix pattern into a regular expression object
    suffix_regex = re.compile(suffix_pattern)
    # Get a list of all .txt files in the directory that match the suffix pattern
    txt_files = [file for file in os.listdir(directory) if suffix_regex.search(file)]


    # Iterate over each file and copy its contents to the clipboard
    for file in txt_files:
        with open(os.path.join(directory, file), 'r') as f:
            file_contents = f.read()
            pyperclip.copy(file_contents)
        print(f"I have copied {file} into the clipboard.")
        continue_input = input("Press 'y' to continue to the next file or any other key to stop: ")
        if continue_input.lower() != 'y':
            break


if __name__ == "__main__":

    project = input("What is the project name? ")

    # project = 'anylog_solution'
    # project = 'ppt_generator'
    # project = 'youtube_translator'
    root_dir = 'C:/Users/Tamas/PycharmProjects/'
    root_dir = root_dir + project + '/'

    max_token_length = 1500
    output_dir = './output/project_to_text/' + project
    print("Generating text files...")
    write_all_files(root_dir, output_dir, max_token_length, max_token_length)
    print("Done.")
    iterate_over_result_file_to_the_clipboard(output_dir)
