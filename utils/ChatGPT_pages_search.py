import os
import json
import requests
import PyPDF2
import string
import openai
import re


class ChatGPT_pages_search:

    def __init__(self, pdf_file) -> None:
        self.current_directory= os.getcwd()
        # self.parent_directory= os.path.dirname(self.current_directory)
        # print(self.parent_directory)
        self.secret_file= os.path.join(self.current_directory, 'secrets.json')
        # self.pdf_path= os.path.join(self.parent_directory, 'static', 'doc', 'Test doc')
        # self.pdf_files= [os.path.join(self.pdf_path,f) for f in os.listdir(self.pdf_path) if f.endswith('.pdf')]
        # self.pdf_file= self.pdf_files[1]
        self.pdf_file=pdf_file
        self.API_KEY=self.load_secrets()
        openai.api_key = self.API_KEY

    def load_secrets(self):
        # load secret file
        with open(self.secret_file, "r") as f:
            secrets=json.load(f)
        API_KEY=secrets['api_key']
        return API_KEY
    
    def extract_text_from_pdf(self, pdf_path):
        pdf_text = {}
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                page_text = page.extract_text()
                page_text = page_text.translate(str.maketrans("", "", string.punctuation))
                pdf_text[f"Page {page_number + 1}"] = page_text
        return pdf_text
    
    
    def query_gpt(self, query):
        self.pdf_json = self.extract_text_from_pdf(self.pdf_file)
        # clean json after it was extracted(to not to loose information on each page
        self.pdf_json = {key: value.strip().strip().lower().replace("  ", "").replace("\n", "") for key, value in self.pdf_json.items()}

        context = '\n'.join([f"{page}: {text}" for page, text in self.pdf_json.items()])  # Concatenate page number and text in context
        prompt = f"Question: {query}\nContext:\n{context}\nAnswer:"

        # Call the OpenAI API to generate a completion
        response = openai.Completion.create(
            engine='text-davinci-003',
            # engine='gpt-3.5-turbo',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Retrieve the answer from the API response
        choices = response.choices[0]
        answer = choices.text.strip()

        # # Find the page number for the answer
        page_numbers = re.findall(r"(?i)page\s+(\d+)", answer)
        return answer, page_numbers, response, context