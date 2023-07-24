import streamlit as st
import fitz  # PyMuPDF
import io
import os
from utils.ChatGPT_pages_search import ChatGPT_pages_search

pdf_file = os.path.join(os.getcwd(), 'static', 'pdfs', 'example.pdf')
search_engine = ChatGPT_pages_search(pdf_file)

# Custom function to get information about the selected page
def query_ChatGPT(query):
    answer, page_numbers, response, context = search_engine.query_gpt(query)
    page_number = ''.join(page_numbers)
    page_number = int(page_number) if page_number else 1  # Set default value to 1 if page_number is empty
    return answer, page_number

def main():
    st.title("PDF Viewer with Page Selector and Query")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Load the PDF using PyMuPDF (fitz)
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = pdf_document.page_count

        # Initialize selected page using st.session_state
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = 1

        st.sidebar.title("Page Selector")
        # Use st.sidebar.slider to update the selected_page variable
        selected_page = st.sidebar.slider("Select Page", 1, total_pages, st.session_state.selected_page)

        # Show an input field for the user to enter their query
        query = st.text_input("Enter your query here:", "Please ask your question", key="input_query")
        query = query + " on what page it was found?"
        # Create a submit button
        if st.button("Submit"):
            # Get information about the selected page using the custom function
            answer, page_number = query_ChatGPT(query)

            # Update the selected_page variable in session_state
            st.session_state.selected_page = page_number

        # Render the selected page using PyMuPDF (fitz)
        page = pdf_document[st.session_state.selected_page - 1]
        image_bytes = page.get_pixmap().tobytes()  # Convert Pixmap to bytes
        st.image(image_bytes, use_column_width=True)

        # Display the PDF page number
        st.write(f"Page {selected_page} / {total_pages}")

        # Show the page information and GPT answer in the sidebar
        st.sidebar.markdown("## Page Information")
        st.sidebar.write(f"GPT answer: {answer}")
        st.sidebar.write(f"Page: {page_number}")

if __name__ == "__main__":
    main()
