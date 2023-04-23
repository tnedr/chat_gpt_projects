import os

def generate_project_structure(root_dir, max_token_length, output_dir, max_tokens_per_file=10**6):
    module_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    prefix = "ok this is the content of {} module:\n".format(file)
                    module_files.append((path, prefix + content))

    # Generate a text file containing the directory structure
    structure_file_path = os.path.join(output_dir, 'project_structure.txt')
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

    # Generate separate text files for each module
    for path, content in module_files:
        module_name = os.path.basename(path)[:-3]  # remove the '.py' extension
        module_file_path = os.path.join(output_dir, module_name + '.txt')
        if len(content.split()) <= max_tokens_per_file:
            with open(module_file_path, 'w') as f:
                f.write(content)
        else:
            for i in range(0, len(content), max_tokens_per_file):
                module_content = content[i:i+max_tokens_per_file]
                if len(module_content.split()) > max_tokens_per_file:
                    raise ValueError("Module '{}' has too many tokens ({}) to fit in one text file.".format(path, len(module_content.split())))
                with open(module_file_path, 'w') as f:
                    f.write(module_content)

    return module_files


root_dir = 'C:/Users/Tamas/PycharmProjects/anylog_solution/'
max_token_length = 4096
output_dir = './output/project_to_text'
print("Generating text files...")
generate_project_structure(root_dir, max_token_length, output_dir)
print("Done.")
