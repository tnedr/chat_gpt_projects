import re
import os


# Function to reformat the text to one sentence per line
def reformat_text(text):
    # Replace line breaks with spaces
    text = text.replace('\n', ' ')
    # Split the text into sentences and join them back together with line breaks
    text = re.split('(?<=[.!?]) +', text)
    text = '\n'.join(text)
    return text


# Function to chunk the transcript
def chunk_transcript(text, chunk_size=50, overlap=5):
    sentences = text.split('\n')
    chunks = []

    # Check if the text length is smaller than chunk size
    if len(sentences) <= chunk_size:
        return [text]

    # Break the transcript into chunks with overlapping sentences
    for i in range(0, len(sentences), chunk_size - overlap):
        chunk = sentences[i:i + chunk_size]
        chunks.append('\n'.join(chunk))
    return chunks

filename = 'meditation_orig.txt'
input_folder = 'input/'
filepath = input_folder + filename


# Read the transcript from a file
with open(filepath, 'r') as file:
    transcript = file.read()

# Reformat the transcript
transcript = reformat_text(transcript)

base = os.path.splitext(filepath)[0]
reformat_filepath = base + '_reformat.txt'
with open(reformat_filepath, 'w') as file:
    file.write(transcript)

# Chunk the transcript
chunks = chunk_transcript(transcript)

output_folder = 'output/'

# Write the chunks to separate files in the output folder
for i, chunk in enumerate(chunks):
    chunk_filepath = output_folder + os.path.basename(base) + f"_chunk{i}.txt"
    with open(chunk_filepath, 'w') as file:
        file.write(chunk)
