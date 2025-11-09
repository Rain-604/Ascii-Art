import os
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# -----------------------------
# 1. Generate character templates
# -----------------------------
def generate_character_map(width=7, height=11, font_path="consola.ttf", font_size=11):
    char_map = {}
    font = ImageFont.truetype(font_path, size=font_size)

    for i in range(32, 126):  # Printable ASCII
        image = Image.new("1", (width, height), color=0)  # 0 = white background
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), chr(i), fill=1, font=font)      # 1 = black text
        arr = np.array(image).astype(int)
        # Invert values: make 0 = white, 1 = black
        arr = 1 - arr
        char_map[chr(i)] = arr
    return char_map

# -----------------------------
# 2. Read pixel-art text file
# -----------------------------
def read_txt_as_array(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip("\n") for line in f]
    # Convert '#' to 0 (black), space to 1 (white)
    arr = np.array([[0 if ch == '#' else 1 for ch in line] for line in lines], dtype=int)
    return arr

# -----------------------------
# 3. Similarity calculation
# -----------------------------
def calculate_similarity(image_batch, template):
    """
    image1: 3D numpy array (n_chars, height, width)
    image2: 2D numpy array (height, width)
    Returns: list of similarity scores for each 2D slice in image1
        """

    similarities = []
    for idx in range(image_batch.shape[0]):  # auto-detect number of characters
        matching_pixels = np.sum(image_batch[idx] == template)
        total_pixels = template.size
        similarities.append(float(matching_pixels / total_pixels))
    return similarities


    return similarities
# -----------------------------
# 4. Decode the big image
# -----------------------------
def decode_image_fast(big_image, char_map, char_width=7, char_height=11):
    rows, cols = big_image.shape
    output_lines = []

    # Pre-stack templates for fast comparison
    template_chars = list(char_map.keys())
    template_stack = np.stack([char_map[c] for c in template_chars])

    for y in range(0, rows, char_height):
        line_chars = []
        for x in range(0, cols, char_width):
            block = big_image[y:y+char_height, x:x+char_width]
            if block.shape != (char_height, char_width):
                continue

            # Vectorized similarity
            matches = (template_stack == block).sum(axis=(1, 2))
            scores = matches / block.size
            best_idx = np.argmax(scores)
            best_char = template_chars[best_idx]

            line_chars.append(best_char)

        if line_chars:
            output_lines.append("".join(line_chars))

    return "\n".join(output_lines)

def decode_image(big_image, char_map, char_width=7, char_height=11, threshold=0.8):
    rows, cols = big_image.shape
    output_lines = []
    
    for y in range(0, rows, char_height):
        line_chars = []
        for x in range(0, cols, char_width):
            block = big_image[y:y+char_height, x:x+char_width]

            # Skip if block is smaller than expected (avoids shape mismatch)
            if block.shape != (char_height, char_width):
                continue

            best_char = "?"
            best_score = 0

            for char, template in char_map.items():
                scores = calculate_similarity(block, template)  # returns a list
                for s in scores:
                    if s > best_score:
                        best_score = s
                        best_char = char

            # Apply threshold
            line_chars.append(best_char)

        if line_chars:  # only append if we found characters in this row
            output_lines.append("".join(line_chars))

    return "\n".join(output_lines)

def enlarge_binary_image(arr, scale=3):
    h, w = arr.shape
    enlarged = np.repeat(np.repeat(arr, scale, axis=0), scale, axis=1)
    return enlarged

def enlarge_ascii_image(image_lines):
    """height = len(image_lines)
    width = len(image_lines[0])
    enlarged = []

    for row in image_lines:
        top = []
        bottom = []
        for ch in row:
            top.extend([ch, ch])
            bottom.extend([ch, ch])
        enlarged.append("".join(top))
        enlarged.append("".join(bottom))"""
    enlarged = []

    for row in image_lines:
        # Each character becomes 3 horizontally
        tripled_row = ["".join([ch * 3 for ch in row])]
        # Repeat each row 3 times vertically
        enlarged.extend(tripled_row * 3)


    return enlarged
# -----------------------------
# 5. Main
# -----------------------------
def main():
    # Generate the matching map
    char_map = generate_character_map()

    # Find all .txt files in current folder
    folder_path = os.getcwd()
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    if not txt_files:
        print("No .txt files found in the current directory.")
        return

    for txt_file in txt_files:
        print(f"Decoding {txt_file}...")
        print("step 1/3: read the image file")
        big_image = read_txt_as_array(txt_file)
        print("step 2/3: enlarge the image for better visibility")
        enlarged_image = enlarge_binary_image(big_image, scale=2)
        print("step 3/3: decode the image to text")
        decoded_text = decode_image_fast(enlarged_image, char_map)
        #enlarged_line = enlarge_ascii_image(decoded_text.splitlines())
        # Print to console
        print("\nDecoded text:\n")
        print(decoded_text)
        print("\n" + "-"*40 + "\n")

        # Save to new file
        output_filename = os.path.splitext(txt_file)[0] + "_decoded.txt"
        with open(output_filename, "w") as f:
            #f.write("\n".join(enlarged_line))
            f.write(decoded_text)
        print(f"Saved decoded output to: {output_filename}")

if __name__ == "__main__":
    main()