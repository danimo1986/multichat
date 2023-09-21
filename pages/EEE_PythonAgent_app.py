import os
import streamlit as st
import sys
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

# Install required packages
# !pip install langchain==0.0.149

# Create Streamlit app
def main():
    # Page title
    st.title("🐍Python Agent App")

    # Sidebar for API key input
    user_api_key = st.sidebar.text_input(
        label="OpenAI API key",
        placeholder="Paste your OpenAI API key here",
        type="password")

    # Check if the API key is provided
    if not user_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        return

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = user_api_key

    llm = OpenAI(model_name="text-davinci-003")
    agent_executor = create_python_agent(
        llm=llm,
        tool=PythonREPLTool(),
        verbose=True,  # デバッグ情報を表示するためにverboseをTrueに設定
    )

    # User input text box
    user_input = st.text_area("User Input:", "")

    if st.button("Submit"):
        if user_input.strip() != "":
            # Capture stdout to display debug information
            sys.stdout = st

            # Get the response from the chatbot
            response = agent_executor.run(user_input)

            # Restore the original stdout
            sys.stdout = sys.__stdout__

            # Display the chatbot's response
            st.write("Chatbot Response:")
            st.markdown(f"<p style='font-size:24px; color:red;'>Chatbot: {response}</p>", unsafe_allow_html=True)
            #st.write(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
