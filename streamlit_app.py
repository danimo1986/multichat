import streamlit as st


st.title("Homepage for My ChatGPT")
st.header('Hello! This page offers multiple apps that have added specific features to ChatGPT.')

st.markdown('''
Please select an app from the slidebar. 

Below are descriptions for each app.
#ask CSV
    - You can ask questions about the data from the uploaded CSV file!
#ask PDF 
    - You can ask questions about the content of the uploaded PDF! 
#SimilarityCalculator
    - From the uploaded CSV file dataset, it will extracted and display the top 5 items most relevant to the input text!
#WebSearch
    - When you ask a question, it will provide answers using information from the web!
''')


# *** sidebar
#st.sidebar.title('Homepage sidebar')