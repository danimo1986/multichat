__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import sqlite3
from PyPDF2 import PdfReader
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

def generate_response(uploaded_file, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        pdf_text = get_pdf_text(uploaded_file)
        if pdf_text:
            # Split documents into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.create_documents([pdf_text])
            # Select embeddings
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            # Create a vectorstore from documents
            db = Chroma.from_documents(texts, embeddings)
            # Create retriever interface
            retriever = db.as_retriever()
            # Create QA chain
            qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
            return qa.run(query_text)
        else:
            return "Error: PDF text extraction failed."

# Page title
st.set_page_config(page_title='🦜🔗 Ask the PDF App')
st.title('🦜🔗 Ask the PDF App')

# File upload
uploaded_file = st.file_uploader('Upload a PDF file', type=['pdf'])

def get_pdf_text(uploaded_file):
    if uploaded_file is not None:
        pdf_text = ""
        pdf_reader = PdfReader(uploaded_file)
        
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        return pdf_text
    else:
        return None

# Query text
query_text = st.text_input('Enter your question:', placeholder='Please provide a short summary.')

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type='password', key='openai_key')
    submitted = st.form_submit_button('Submit', disabled=not (uploaded_file and query_text))
    
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(result[0])
