import streamlit as st
import fitz  # PyMuPDF
import io
import os
from PIL import Image
from utils.ChatGPT_pages_search import ChatGPT_pages_search

pdf_file = os.path.join(os.getcwd(), 'static', 'pdfs', 'example.pdf')
logo_file = os.path.join(os.getcwd(), 'static', 'img', 'BTlogo.jpg')

# Custom function to get information about the selected page
def query_ChatGPT(search_engine, query):
    answer, page_numbers, response, context = search_engine.query_gpt(query)
    if page_numbers:
        page_numbers = [int(page_number) for page_number in page_numbers]
    else:
        page_numbers = 'Page cannot be specified.'
    return answer, page_numbers

def main():
    st.title("PDF search powered by ChatGPT")

    # Image above query input
    image = Image.open(logo_file)  # Replace "path/to/your/image.jpg" with the actual path to your image
    st.image(image, use_column_width=True)

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Load the PDF using PyMuPDF (fitz)
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Show an input field for the user to enter their query
        query = st.sidebar.text_input("Enter your query here:", "Please ask your question", key="input_query")
        query = query + " on what page it was found?"

        # Create a submit button
        if st.sidebar.button("Submit"):
            search_engine = ChatGPT_pages_search(pdf_file)
            # Get information about the selected page using the custom function
            answer, page_numbers = query_ChatGPT(search_engine, query)

            # Show the GPT answer in the sidebar
            st.sidebar.markdown("## GPT Answer")
            st.sidebar.text_area("Answer:", answer, height=500, max_chars=5000)
            
            if page_numbers!= 'Page cannot be specified.':
                for page_number in page_numbers:
                    st.sidebar.write(f"Page: {page_number}")

                    # Render the selected page using PyMuPDF (fitz)
                    page = pdf_document[page_number - 1]
                    image_bytes = page.get_pixmap().tobytes()  # Convert Pixmap to bytes
                    st.image(image_bytes, use_column_width=True, caption=f"Page {page_number}")
            else:
                st.write(page_numbers)
if __name__ == "__main__":
    main()