from PIL import Image, ImageDraw
import argparse

def tile_image(image_path, tile_size, gap_size, min_black_size):
    # Open the image and convert it to grayscale
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    width, height = image.size

    # Calculate the number of rows and columns for the tiles
    cols = (width + gap_size) // (tile_size + gap_size)
    rows = (height + gap_size) // (tile_size + gap_size)

    # Create a new blank image to store the tiled result
    result_width = cols * (tile_size + gap_size) - gap_size
    result_height = rows * (tile_size + gap_size) - gap_size
    result_image = Image.new("RGB", (result_width, result_height), "white")
    draw = ImageDraw.Draw(result_image)

    # Iterate over each tile
    for y in range(rows):
        for x in range(cols):
            # Calculate the position of the current tile in the original image
            left = x * (tile_size + gap_size)
            upper = y * (tile_size + gap_size)
            right = left + tile_size
            lower = upper + tile_size

            # Get the pixel value (grayscale, 0-255) at the top-left corner of the current tile
            pixel_value = image.getpixel((left, upper))

            # Calculate the size of the black region (darker colors result in larger regions)
            # Map the grayscale value to the size of the black region (min_black_size to tile_size)
            if pixel_value == 255:
                # If the pixel is completely white, use min_black_size
                black_size = min_black_size
            else:
                # Otherwise, calculate the black region size based on the grayscale value
                black_size = int((255 - pixel_value) / 255 * (tile_size - min_black_size)) + min_black_size

            # Draw the black region
            if black_size > 0:
                draw.rectangle(
                    [left, upper, left + black_size, upper + black_size],
                    fill="black"
                )

    # Save the resulting image
    result_image.save("./tiled_image.png")


if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Figure batch processing")

    # Add command-line arguments
    parser.add_argument("-in", "--input", help="Path to the input file", type=str)
    parser.add_argument("-t", "--tile_size", help="Size of each tile", type=int, default=12)
    parser.add_argument("-g", "--gap_size", help="Size of the gap between tiles", type=int, default=4)
    parser.add_argument("-b", "--min_black_size", help="Minimum size of the black region for blank tiles", type=int, default=8)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Example call
    tile_image(args.input, tile_size=args.tile_size, gap_size=args.gap_size, min_black_size=args.min_black_size)
    print("Figure has been processed")