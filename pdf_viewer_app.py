import streamlit as st
import fitz  # PyMuPDF
import io
import os
from PIL import Image
from utils.ChatGPT_pages_search import ChatGPT_pages_search

pdf_file = os.path.join(os.getcwd(), 'static', 'pdfs', 'example.pdf')
logo_file = os.path.join(os.getcwd(), 'static', 'img', 'BTlogo.jpg')
search_engine = ChatGPT_pages_search(pdf_file)

st.markdown(
    """
    <style>
    body {
        color: black;
        background-color: white;
    }
    .pdf-viewer {
        border: 2px solid black;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Custom function to get information about the selected page
def query_ChatGPT(query):
    answer, page_numbers, response, context = search_engine.query_gpt(query)
    page_number = ''.join(page_numbers)
    page_number = int(page_number) if page_number else 1  # Set default value to 1 if page_number is empty
    return answer, page_number

def main():
    st.title("PDF search powerded by ChatGPT")

    # Initialize answer variable with an empty string
    answer = ""
    page_number = 1
    
    # Image above query input
    image = Image.open(logo_file)  # Replace "path/to/your/image.jpg" with the actual path to your image
    st.image(image, use_column_width=True)
    
    # Show an input field for the user to enter their query
    query = st.sidebar.text_input("Enter your query here:", "Please ask your question", key="input_query")
    query = query + " on what page it was found?"

    # Create a submit button
    if st.sidebar.button("Submit"):
        # Get information about the selected page using the custom function
        answer, page_number = query_ChatGPT(query)

    # Show the GPT answer in the sidebar
    st.sidebar.markdown("## GPT Answer")
    st.sidebar.write(answer)
    st.sidebar.write(f"Page: {page_number}")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Load the PDF using PyMuPDF (fitz)
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = pdf_document.page_count

        # Render the selected page using PyMuPDF (fitz)
        page = pdf_document[page_number - 1]
        image_bytes = page.get_pixmap().tobytes()  # Convert Pixmap to bytes
        st.image(image_bytes, use_column_width=True)
if __name__ == "__main__":
    main()