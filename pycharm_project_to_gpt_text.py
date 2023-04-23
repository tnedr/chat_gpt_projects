
import os

def generate_project_structure_and_jumbo_file(root_dir, max_token_length, output_dir, max_tokens_per_file=10**6):
    module_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    if len(content.split()) > max_token_length:
                        raise ValueError("Module '{}' has too many tokens ({}) to fit in one text file.".format(path, len(content.split())))
                    prefix = "ok this is the content of {} module located at {}:\n".format(file, os.path.abspath(path))
                    # prefix = "ok this is the content of {} module:\n".format(file)
                    with open(path, 'r') as f:
                        content = f.read()
                    content = [prefix + line if i == 0 else line for i, line in enumerate(content)]
                    module_files.append((path, content))
                    # module_files.append((path, prefix + content))

    basename = os.path.basename(os.path.normpath(root_dir))

    # Generate a text file containing the directory structure
    structure_file_path = os.path.join(output_dir, '{}_structure.txt'.format(basename))
    with open(structure_file_path, 'w') as f:
        f.write("Project structure:\n")
        for root, dirs, files in os.walk(root_dir):
            if '.git' in dirs:
                dirs.remove('.git')
            if '.idea' in dirs:
                dirs.remove('.idea')
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                if file.endswith('.py'):
                    f.write('{}{}\n'.format(subindent, file))

    # Generate a jumbo file containing all module content

    jumbo_file_path = os.path.join(output_dir, '{}_codes.txt'.format(basename))
    with open(jumbo_file_path, 'w') as f:
        for path, content in module_files:
            if sum(len(line.split()) for line in content) <= max_tokens_per_file:
            # if len(content.split()) <= max_tokens_per_file:
                f.write(''.join(content))
                # f.write(content)
                f.write('\n') # Add a newline between modules
            else:
                for i in range(0, len(content), max_tokens_per_file):
                    f.write(content[i:i+max_tokens_per_file])
                    f.write('\n')

    return jumbo_file_path


def split_jumbo_file(jumbo_file_path, basename, output_dir, max_tokens_per_file):
    current_file_tokens = 0
    current_file_modules = []
    current_file_num = 1

    with open(jumbo_file_path, 'r') as jumbo_file:
        for line in jumbo_file:
            line_tokens = len(line.split())
            if current_file_tokens + line_tokens <= max_tokens_per_file:
                print("Splitting modules into files. Current file size: {} tokens.".format(current_file_tokens + line_tokens))
                current_file_tokens += line_tokens
                current_file_modules.append(line.rstrip('\n'))

                # current_file_modules.append(line.strip())
            else:
                write_split_file(current_file_modules, basename, output_dir, current_file_num)
                current_file_tokens = line_tokens
                # current_file_modules = [line.strip()]
                current_file_modules = [line]

                current_file_num += 1

        # Write the last file
        write_split_file(current_file_modules, basename, output_dir, current_file_num)

def write_split_file(modules, basename, output_dir, file_num):
    file_path = os.path.join(output_dir, '{}_{}.txt'.format(basename, file_num))
    with open(file_path, 'w') as f:
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

root_dir = 'C:/Users/Tamas/PycharmProjects/anylog_solution/'
max_token_length = 4096
output_dir = './output/project_to_text'

print("Generating text files...")
max_tokens_per_file = 4096

# Generate jumbo file
jumbo_file_path = generate_project_structure_and_jumbo_file(root_dir, max_token_length, output_dir, max_tokens_per_file)

# Split jumbo file into smaller files
basename = os.path.basename(os.path.normpath(root_dir))
split_jumbo_file(jumbo_file_path, basename, output_dir, max_tokens_per_file)

print("Done.")
