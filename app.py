import streamlit as st
import os
from modules.pdf_utils import pdf_to_images
from modules.image_utils import combine_pages_side_by_side
from modules.gemini_utils import extract_text_from_images
from modules.astra_utils import store_in_astradb

# Setup Streamlit UI
st.title("📄 PDF Image Extractor & AstraDB Storage")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF Uploaded Successfully!")

    # Create output directory
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to images
    st.write("📥 Extracting images from PDF...")
    image_files = pdf_to_images(uploaded_file, output_folder)

    if len(image_files) < 2:
        st.warning("PDF has less than two pages. At least two pages are required for combined images.")
    else:
        # Combine images side by side
        st.write("🖼️ Combining images side-by-side...")
        combined_images = combine_pages_side_by_side(image_files, output_folder)

        # Display images
        st.write("### 📸 Preview of Combined Images")
        for img_path in combined_images:
            st.image(img_path, caption=os.path.basename(img_path))

        # Extract descriptions using Gemini AI
        st.write("🔍 Extracting text descriptions from images...")
        extracted_texts = extract_text_from_images(combined_images)

        # Store descriptions in AstraDB
        if extracted_texts:
            st.write("🗂️ Storing extracted text in AstraDB...")
            store_in_astradb(extracted_texts, combined_images)
            st.success("✅ Extracted text stored in AstraDB successfully!")