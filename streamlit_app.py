import streamlit as st


st.title("Homepage for My ChatGPT")
st.header('Hello! This page offers multiple apps that have added specific features to ChatGPT.')

st.markdown('''
Please select an app from the sidebar. 

Below are descriptions for each app.

- **AAA: ask PDF**
  You can ask questions about the content of the uploaded PDF! 
            
- **BBB: ask CSV**
  You can ask questions about the data from the uploaded CSV file!

- **CCC: Similarity Calculator**
  From the uploaded CSV file dataset, it will extract and display the top 5 items most relevant to the input text!

- **DDD: Web Search**
  When you ask a question, it will provide answers using information from the web!
            
- **EEE: Python Agent**
  It will respond to your questions using Python!
''')



# *** sidebar
#st.sidebar.title('Homepage sidebar')