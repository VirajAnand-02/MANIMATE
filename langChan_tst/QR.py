import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools

# This table is necessary to know where to draw the smaller alignment patterns.
# It's a standard part of the QR code specification.
ALIGNMENT_PATTERN_COORDS = [
    [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], 
    [6, 24, 42], [6, 26, 46], [6, 28, 50], [6, 30, 54], [6, 32, 58], 
    [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], 
    [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], 
    [6, 28, 50, 72, 94], [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], 
    [6, 28, 54, 80, 106], [6, 32, 58, 84, 110], [6, 30, 58, 86, 114], 
    [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126], 
    [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134], [6, 34, 60, 86, 112, 138], 
    [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146], [6, 30, 54, 78, 102, 126, 150], 
    [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158], 
    [6, 32, 58, 84, 110, 136, 162], [6, 26, 54, 82, 110, 138, 166], 
    [6, 30, 58, 86, 114, 142, 170]
]

def create_qr_template(version):
    """Generates an idealized QR code template with functional patterns in place."""
    grid_size = 4 * version + 17
    # Initialize with 128 (gray) to signify data areas
    template = np.full((grid_size, grid_size), 128, dtype=np.uint8)

    # 1. Draw Finder Patterns (7x7) and Separators (8x8 box)
    for pos_y, pos_x in [(0, 0), (0, grid_size - 7), (grid_size - 7, 0)]:
        template[pos_y:pos_y+7, pos_x:pos_x+7] = 0 # Black box
        template[pos_y+1:pos_y+6, pos_x+1:pos_x+6] = 255 # White box
        template[pos_y+2:pos_y+5, pos_x+2:pos_x+5] = 0 # Inner black box
    # Separators (set to white)
    for pos_y, pos_x in [(0, 0), (0, grid_size - 8), (grid_size - 8, 0)]:
        template[pos_y:pos_y+8, pos_x:pos_x+8][template[pos_y:pos_y+8, pos_x:pos_x+8] == 128] = 255

    # 2. Draw Timing Patterns
    for i in range(8, grid_size - 8):
        template[6, i] = 0 if i % 2 == 0 else 255
        template[i, 6] = 0 if i % 2 == 0 else 255
        
    # 3. Draw Alignment Patterns (if needed)
    if version >= 2:
        coords = ALIGNMENT_PATTERN_COORDS[version - 1]
        for y in coords:
            for x in coords:
                # Avoid placing on top of finder patterns
                if template[y, x] != 128: continue
                # Draw 5x5 pattern
                template[y-2:y+3, x-2:x+3] = 0
                template[y-1:y+2, x-1:x+2] = 255
                template[y, x] = 0

    # 4. Draw Dark Module
    template[4 * version + 9, 8] = 0

    return template

def generate_raw_text(grid_image):
    """Converts a grid image to a raw text block of characters."""
    # Downscale for manageable output
    height, width = grid_image.shape
    if height > 50:
        grid_image = cv2.resize(grid_image, (50, 50), interpolation=cv2.INTER_NEAREST)
    
    raw_text = ""
    for row in grid_image:
        for pixel in row:
            raw_text += '█' if pixel == 0 else ' '
        raw_text += '\n'
    return raw_text

def regenerate_and_decode_all_versions(image_path, kernel_size=2, iterations=1):
    """
    Regenerates the format for all QR versions and attempts to decode.
    """
    # --- 1. Load and Dilate Image ---
    try:
        original_image = cv2.imread(image_path)
        if original_image is None: raise FileNotFoundError
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return

    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    inverted_binary = cv2.bitwise_not(cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)[1])
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_image = cv2.bitwise_not(cv2.dilate(inverted_binary, kernel, iterations=iterations))

    # --- 2. Get Source Image for Sampling ---
    qr_decoder = cv2.QRCodeDetector()
    _, _, straight_qr = qr_decoder.detectAndDecode(dilated_image)
    
    source_grid = cv2.convertScaleAbs(straight_qr) if straight_qr is not None and straight_qr.size > 0 else dilated_image
    print("Using " + ("straightened grid" if straight_qr is not None else "full dilated image") + " as data source.")

    # --- 3. Main Loop: Regenerate, Decode, and Show for All Versions ---
    source_h, source_w = source_grid.shape[:2]

    for version in range(1, 41):
        grid_size = 4 * version + 17
        template = create_qr_template(version)
        reconstructed_grid = template.copy()

        # Fill in the data areas of the template
        for r in range(grid_size):
            for c in range(grid_size):
                if template[r, c] == 128: # Is it a data module?
                    # Find corresponding point in source grid
                    src_y = int((r / grid_size) * source_h)
                    src_x = int((c / grid_size) * source_w)
                    pixel_value = source_grid[src_y, src_x]
                    reconstructed_grid[r, c] = 0 if pixel_value < 128 else 255
        
        # Scale up for viewing and decoding
        final_image = cv2.resize(reconstructed_grid, (grid_size * 10, grid_size * 10), interpolation=cv2.INTER_NEAREST)

        # Decode and prepare output
        decoded_data, _, _ = qr_decoder.detectAndDecode(final_image)
        
        print(f"\n--- Version {version} ({grid_size}x{grid_size}) ---")
        
        result_title = ""
        if decoded_data:
            result_title = "SUCCESS!"
            print(f"✅ DECODED: {decoded_data}")
        else:
            result_title = "DECODING FAILED"
            print("❌ Decoding Failed. Displaying raw text representation:")
            print(generate_raw_text(final_image))

        # Show the regenerated image
        plt.figure(figsize=(8, 8))
        plt.imshow(final_image, cmap='gray', interpolation='nearest')
        plt.title(f"Regenerated QR Code: Version {version} ({grid_size}x{grid_size})\nResult: {result_title}", fontsize=14)
        plt.axis('off')
        plt.show()

# --- HOW TO USE ---
if __name__ == '__main__':
    DILATION_KERNEL_SIZE = 5
    DILATION_ITERATIONS = 1
    
    path_to_qr_image = r'C:\\Users\\isanham\\Downloads\\qrs.png' 
    regenerate_and_decode_all_versions(
        path_to_qr_image, 
        kernel_size=DILATION_KERNEL_SIZE, 
        iterations=DILATION_ITERATIONS
    )