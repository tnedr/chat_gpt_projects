import os
import pytesseract
from PIL import Image
from datetime import datetime

# Set the input and output directories
input_dir = 'input/code_photos'
output_dir = 'output'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the list to hold the extracted text from each image
texts = []

# Loop through all image files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image
    if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.PNG'):
        # Load the image
        image_path = os.path.join(input_dir, filename)
        img = Image.open(image_path)

        # Apply thresholding to the image
        threshold = 100
        img = img.point(lambda p: p > threshold and 255)

        # Loop through four rotations of the image
        for i in [0]: #range(4):
            # Rotate the image
            rotated_img = img.rotate(i * 90)

            # Convert the rotated image to grayscale
            rotated_img = rotated_img.convert('L')

            # Perform OCR on the rotated image
            text = pytesseract.image_to_string(rotated_img)

            # Append the extracted text to the list
            texts.append(text)

            # Generate the filename for the output file
            now = datetime.now()
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            output_filename = f'{os.path.splitext(filename)[0]}_{i*90}_{timestamp}.txt'
            output_path = os.path.join(output_dir, output_filename)

            # Save the extracted text to the output file
            with open(output_path, 'w') as f:
                f.write(text)

            # Print a message to confirm that the text was saved
            print(f'Text extracted from {filename} (rotation={i*90}) and saved to {output_path}.')

# Concatenate the extracted text from all images
all_text = '\n'.join(texts)

# Generate the filename for the concatenated output file
now = datetime.now()
timestamp = now.strftime('%Y%m%d_%H%M%S')
output_filename = f'concatenated_{timestamp}.txt'
output_path = os.path.join(output_dir, output_filename)

# Save the concatenated text to the output file
with open(output_path, 'w') as f:
    f.write(all_text)

# Print a message to confirm that the concatenated text was saved
print(f'Text extracted from {len(texts)} images and concatenated to {output_path}.')
