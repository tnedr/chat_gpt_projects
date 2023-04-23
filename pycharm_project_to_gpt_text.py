import os

def write_structure_file(root_dir, output_dir):
    basename = os.path.basename(os.path.normpath(root_dir))
    structure_file_path = os.path.join(output_dir, f'{basename}_structure.txt')

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


def write_splitted_files(code_file_path, output_dir, structure_file_path, max_tokens_per_file):
    current_file_tokens = 0
    current_file_modules = []
    current_file_num = 1

    with open(code_file_path, 'r') as jumbo_file:
        for line in jumbo_file:
            line_tokens = len(line.split())
            if current_file_tokens + line_tokens <= max_tokens_per_file:
                print(f"Splitting modules into files. Current file size: {current_file_tokens + line_tokens} tokens.")
                current_file_tokens += line_tokens
                current_file_modules.append(line.rstrip('\n'))
            else:
                write_split_file(current_file_modules, output_dir, structure_file_path, current_file_num)
                current_file_tokens = line_tokens
                current_file_modules = [line.rstrip('\n')]
                current_file_num += 1

        write_split_file(current_file_modules, output_dir, structure_file_path, current_file_num)

def write_split_file(modules, output_dir, structure_file_path, file_num):
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
def write_all_files(root_dir, output_dir, max_token_length, max_tokens_per_file):
    structure_file_path = write_structure_file(root_dir, output_dir)
    module_files = create_module_file_list(root_dir, max_token_length)
    jumbo_file_path = write_code_jumbo_file(module_files, output_dir)
    write_splitted_files(jumbo_file_path, output_dir, structure_file_path, max_tokens_per_file)


root_dir = 'C:/Users/Tamas/PycharmProjects/anylog_solution/'
max_token_length = 4096
output_dir = './output/project_to_text'
print("Generating text files...")
write_all_files(root_dir, output_dir, max_token_length, max_token_length)
# structure_file_path = write_structure_file(root_dir, output_dir)
# module_files = create_module_file_list(root_dir, max_token_length)
# jumbo_file_path = write_code_jumbo_file(module_files, output_dir)
# write_splitted_files(jumbo_file_path, output_dir, structure_file_path, max_token_length)

print("Done.")
