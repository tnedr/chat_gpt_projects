gpt_promtp ="""
we are working on our website for anti aging supplement,
please review it from multiple perspective: validity of statements, we would like to avoid direct health claims. Structure. User friendlyness, engagement, and so on, you can come up with your own viewpoint which can help us to launc a successfull business. 
 Please be concrete like in this md file you state that "..", instead of this you should write that ".......".
  This is the webpages as md files: 
"""


import os

def write_aggregated_file(aggregated_content, vault_folder_path, target_note):
    target_note_path = os.path.join(vault_folder_path, target_note)
    # if file exists, delete it
    if os.path.exists(target_note_path):
        os.remove(target_note_path)

    with open(target_note_path, 'w', encoding='utf-8') as f:
        f.write(aggregated_content)

def concatenate_notes(vault_folder_path, starts_with, number_of_files_list, base_target_note):
    aggregated_content = ""
    index = 0
    generated_file_count = 1

    # iterating over md files in vault path
    for root, dirs, files in os.walk(vault_folder_path):
        selected_files = [f for f in files if f.endswith(".md") and f.startswith(starts_with)]
        # Sort the selected files in ascending order
        selected_files.sort()
        for file_count, file in enumerate(selected_files):
            print(os.path.join(root, file))
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                # put the given file name as a header
                content = f"# {file}\n\n{content}"
                aggregated_content += f"\n\n---\n\n{content}"

            if index < len(number_of_files_list) and file_count + 1 == sum(number_of_files_list[:index + 1]):
                target_note = vault_folder_path + '/' + f"{base_target_note}_{generated_file_count}.md"
                write_aggregated_file(aggregated_content, vault_folder_path, target_note)
                print(f"Aggregated content has been written to {target_note}")
                generated_file_count += 1
                aggregated_content = ""
                index += 1

    # Write remaining aggregated content to the last file
    if aggregated_content:
        target_note = vault_folder_path + '/' + f"{base_target_note}_{generated_file_count}.md"
        write_aggregated_file(aggregated_content, vault_folder_path, target_note)
        print(f"Aggregated content has been written to {target_note}")

if  __name__ == "__main__":
    # Replace these variables with your specific paths and note names
    vault_folder_path = "G:/My Drive/00_obsidian/SB/30_Website"
    starts_with = '2'
    number_of_files_list = []  # First file will have 3 md files, second will have 5, last will have remaining
    base_target_note = "30_webside_concatenated"

    # Execute the function to concatenate notes
    concatenate_notes(vault_folder_path, starts_with, number_of_files_list, base_target_note)
