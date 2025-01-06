import os
import io
import base64
from PIL import Image, ImageDraw

def combine_pages_side_by_side(image_files, output_folder):
    """Combine pages side-by-side and return a list of image paths."""
    combined_images = []
    
    for i in range(len(image_files) - 1):
        img1 = Image.open(image_files[i])
        img2 = Image.open(image_files[i + 1])

        w1, h1 = img1.size
        w2, h2 = img2.size
        combined_width = w1 + w2
        combined_height = max(h1, h2)

        new_img = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (w1, 0))

        draw = ImageDraw.Draw(new_img)
        draw.line((w1, 0, w1, combined_height), fill=(0, 0, 0), width=3)

        image_filename = os.path.join(output_folder, f"combined_page_{i+1}_and_{i+2}.png")
        new_img.save(image_filename)

        combined_images.append(image_filename)

    return combined_images
