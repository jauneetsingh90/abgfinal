import os
from pdf2image import convert_from_bytes

def pdf_to_images(pdf_file, output_folder):
    """Convert PDF file to images."""
    pdf_bytes = pdf_file.read()
    pages = convert_from_bytes(pdf_bytes)
    image_files = []

    for i, page in enumerate(pages):
        image_filename = os.path.join(output_folder, f"page_{i + 1}.png")
        page.save(image_filename, "PNG")
        image_files.append(image_filename)

    return image_files
