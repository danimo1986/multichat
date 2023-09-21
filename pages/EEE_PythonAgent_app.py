import os
import streamlit as st
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
        verbose=True,
    )

    # User input text box
    user_input = st.text_area("User Input:", "")

    if st.button("Submit"):
        if user_input.strip() != "":
            # Get the response from the chatbot
            response = agent_executor.run(user_input)

            # Display the chatbot's response
            st.write("Chatbot Response:")
            st.write(f"Chatbot: {response}")

            # Check if the response is a dictionary
            if isinstance(response, dict):
                # Execute and display Python code
                if response.get("action") == "Python_REPL" and response.get("action_input"):
                    st.code(response["action_input"], language="python")
                    st.write("Chatbot Observations:")
                    for observation in response.get("observations", []):
                        st.write(observation)
                    st.write("Final Answer:")
                    st.write(response.get("final_answer"))
                else:
                    st.write("Response is not Python code.")

if __name__ == "__main__":
    main()
