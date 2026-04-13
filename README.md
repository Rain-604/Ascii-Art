# ASCII Art Decoder

## Project Description

This project is an **ASCII art decoding system** that converts ASCII art (text-based images made with `#` and space characters) back into readable text. It uses character template matching to intelligently recognize and decode ASCII art representations of text.

## How It Works

The project employs a pattern-matching approach with the following workflow:

### 1. **Character Template Generation**
- Creates binary templates for all printable ASCII characters (ASCII 32-126)
- Uses a TrueType font (Consolas) to render each character
- Stores character patterns as numpy arrays for fast comparison

### 2. **ASCII Art Input**
- Reads text files containing ASCII art where:
  - `#` represents black pixels
  - Space represents white pixels
- Converts the visual representation into a numerical array for processing

### 3. **Pattern Matching & Decoding**
- Divides the ASCII art into fixed-size blocks (7x11 pixels by default)
- Compares each block against all character templates
- Calculates similarity scores using pixel-by-pixel matching
- Selects the character with the highest similarity match
- Reconstructs the original text from matched characters

### 4. **Optimization**
- Uses vectorized NumPy operations for fast batch similarity calculations
- Pre-stacks all character templates for efficient comparison
- Processes multiple blocks in parallel when possible

## Project Structure

```
Ascii-Art/
├── main.py                          # Main decoder implementation
├── DSC05557_decoded.txt            # ASCII art version (encoded)
├── DSC05557_decoded_decoded.txt    # Decoded text version (result)
├── DSC08918_decoded.txt            # ASCII art version (encoded)
├── DSC08918_decoded_decoded.txt    # Decoded text version (result)
└── README.md                        # This file
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `generate_character_map()` | Creates binary templates for ASCII characters |
| `read_txt_as_array()` | Converts ASCII art text files to numerical arrays |
| `calculate_similarity()` | Computes matching scores between image blocks and templates |
| `decode_image()` | Main decoding function with threshold checking |
| `decode_image_fast()` | Optimized version using vectorized operations |

## Technical Details

- **Language**: Python 3
- **Dependencies**: 
  - NumPy (numerical operations)
  - PIL/Pillow (image processing)
- **Character Block Size**: 7x11 pixels (default)
- **Printable ASCII Range**: 32-126 (94 characters)
- **Font**: Consolas (standard monospace font)

## Usage

```python
from main import generate_character_map, read_txt_as_array, decode_image_fast

# Generate character templates
char_map = generate_character_map()

# Read ASCII art file
ascii_art = read_txt_as_array("DSC05557_decoded.txt")

# Decode the ASCII art back to text
decoded_text = decode_image_fast(ascii_art, char_map)

# Print or save the result
print(decoded_text)
```

## Example

**Input (ASCII Art):**
```
################################################
## ## # ## # #    #########
## # # # # # # # #
# # # #  #  #  # # # # #
```

**Output (Decoded Text):**
```
Hello World!
```

## Performance Features

- **Vectorized Comparison**: Uses NumPy's broadcasting for fast similarity calculations
- **Template Stacking**: Pre-computes all templates in one array for batch processing
- **Threshold Matching**: Optional threshold parameter to filter low-confidence matches
- **Memory Efficient**: Processes large ASCII art files incrementally by rows

## Future Enhancements

- Support for different font styles and sizes
- Configurable character block dimensions
- Enhanced similarity metrics (e.g., weighted matching)
- Batch processing for multiple files
- GUI interface for interactive decoding
