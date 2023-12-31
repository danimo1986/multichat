import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.tools import DuckDuckGoSearchTool

# Install required packages
# !pip install langchain==0.0.149
# !pip install openai==0.27.8
# !pip install duckduckgo-search==3.8.3

# Initialize chat history using a session_state variable
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Create Streamlit app
def main():
    # Page title
    st.title("🌍Chat on WebInfo App by duckduckgo-search")

    st.markdown('''
    When you ask a question, it will provide answers using information from the web! Think of it as having a virtual researcher that fetches information from a wide range of online resources.
    ''')

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

    # Create OpenAI model and tools
    llm = OpenAI(model_name="text-davinci-003", temperature=0.2)
    search = DuckDuckGoSearchTool()

    tools = [
        Tool(
            name="duckduckgo-search",
            func=search.run,
            description="Useful for when you need to search for the latest information on the web",
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True
    )

    # User input text box
    user_input = st.text_area("User Input:", "")

    # Chat history reset button in the sidebar
    if st.sidebar.button("Reset Chat History"):
        reset_chat_history()

    if st.button("Submit"):
        if user_input.strip() != "":
            # Get the response from the chatbot using conversational_chat function
            response = conversational_chat(agent, user_input)

            # Display the chatbot's response
            st.write("Chatbot Response:")
            st.write(f"Chatbot: {response}")

# Define conversational_chat function
def conversational_chat(agent, query):
    result = agent.run({'input': query, 'chat_history': st.session_state['history']})
    st.session_state['history'].append((query, result))
    return result

# Define chat history reset function
def reset_chat_history():
    st.session_state['history'] = []

if __name__ == "__main__":
    main()
