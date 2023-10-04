import os

def concatenate_notes(vault_folder_path, starts_with, target_note):
    # Initialize an empty string to hold the concatenated content
    aggregated_content = ""

    # iterating over md files in valult path
    for root, dirs, files in os.walk(vault_folder_path):
        # select only those md files which names has starting with starts_with
        for file in files:
            if file.endswith(".md") and file.startswith(starts_with):
                print(os.path.join(root, file))
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    aggregated_content += f"\n\n---\n\n{content}"

    # Write the aggregated content to the target note
    target_note_path = os.path.join(vault_folder_path, target_note)
    with open(target_note_path, 'w', encoding='utf-8') as f:
        f.write(aggregated_content)

    print(f"Aggregated content has been written to {target_note}")

if __name__ == "__main__":
    # Replace these variables with your specific paths and note names
    vault_folder_path = "G:/My Drive/00_obsidian/SB/30_Website"
    starts_with = '2'  # Add your note names here
    target_note = "31_website_concatenated.md"  # The note where all content will be aggregated

    # Execute the function to concatenate notes
    concatenate_notes(vault_folder_path, starts_with, target_note)
