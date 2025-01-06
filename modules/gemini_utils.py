import base64
import google.generativeai as genai

# Gemini AI API Key
GEMINI_API_KEY=""
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Prompt for text extraction
PROMPT = """
Analyze the provided image content and describe it thoroughly in markdown format.
Focus on accurately capturing details including text, tables, graphs, charts, and any other visual elements.

# Page Title or Main Heading

## Section 1: Overview of the Image
Describe the main content, purpose, and layout.

## Section 2: Text Content
### Key Headings or Labels
- List any prominent headings or labels.

### Body Text
- Describe any detailed text content, including sentences, paragraphs, or numerical data.

## Section 3: Table Description
### Table 1: [Title]
- Describe the structure, headers, and data points.

## Section 4: Graph/Chart Description
### Graph/Chart 1: [Title]
- Explain type, labels, and key trends.

## Section 5: Additional Elements
- Describe any additional visuals, logos, or icons.

## Section 6: Observations and Insights
- Summarize important takeaways.
"""

def extract_text_from_images(image_files):
    """Extracts text descriptions from images using Gemini AI."""
    extracted_texts = []

    for img_path in image_files:
        with open(img_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode("utf-8")

        try:
            response = model.generate_content([
                {'mime_type': 'image/png', 'data': b64_data},
                PROMPT
            ])
            extracted_texts.append(response.text.strip())

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    return extracted_texts
