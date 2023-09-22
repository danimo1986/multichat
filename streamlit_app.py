import streamlit as st


st.title("Homepage for My ChatGPT")
st.header('Hello! This page offers multiple apps that have added specific features to ChatGPT.')

st.markdown('''
Please select an app from the sidebar. 

Below are descriptions for each app.

- **AAA: 🦜🔗ask PDF:**<br>
  You can ask questions about the content of the uploaded PDF! For example, you can inquire about specific information or details within the PDF document.

- **BBB: 🦜🔗ask CSV:**<br>
  You can ask questions about the data from the uploaded CSV file! This allows you to retrieve specific data points from the CSV dataset or ask about patterns in the data.

- **CCC: 💕Similarity Calculator:**<br>
  From the uploaded CSV file dataset, it will extract and display the top 5 items most relevant to the input text! This tool helps you find the items in the dataset that are closest to your query.

- **DDD: 🌍Web Search:**<br>
  When you ask a question, it will provide answers using information from the web! Think of it as having a virtual researcher that fetches information from a wide range of online resources.

- **EEE: 🐍Python Agent:**<br>
  It will respond to your questions using Python! For example, calculations can be performed in response to natural language questions like, "What is the fifth prime number?".
''', unsafe_allow_html=True)





# *** sidebar
#st.sidebar.title('Homepage sidebar')