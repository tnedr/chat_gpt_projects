import os

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

def slice_file(input_file, chunk_size):
    filepath = os.path.join(INPUT_FOLDER, input_file)
    with open(filepath, 'r') as f:
        data = f.read()

    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    for i, chunk in enumerate(chunks):
        filename = os.path.join(OUTPUT_FOLDER, input_file + f'_chunk_{i}.txt')
        with open(filename, 'w') as f:
            f.write(chunk)


filename = 'youtube_transcript_wolfram_chatgpt.txt'
slice_file(filename, 3000)
