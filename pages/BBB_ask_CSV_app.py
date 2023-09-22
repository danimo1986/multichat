import streamlit as st
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import os
import random
from dotenv import load_dotenv

load_dotenv()  # 環境変数

# List of response templates
response_templates = [
    "Thank you for your question. ",
    #"Based on the data, I believe ",
    #"It seems likely that "
]

# Page title
#st.set_page_config(page_title='🦜🔗 Ask the CSV App')
st.title('🦜🔗 Ask the CSV App')
st.markdown('''
You can ask questions about the data from the uploaded CSV file! This allows you to retrieve specific data points from the CSV dataset or ask about patterns in the data.
''')

# Input API KEY
user_api_key = st.sidebar.text_input(
    label="OpenAI API key",
    placeholder="Paste your openAI API key here",
    type="password")
os.environ['OPENAI_API_KEY'] = user_api_key


# Global variable to store conversation history
conversation_history = ""

def chat_with_csv(df):
    st.write(df)
    user_question = st.text_input("Enter your question about the CSV data:")
    
    if user_question:
        global conversation_history
        conversation_history += f"\nUser: {user_question}"
        response_text = generate_gpt_response(user_question)
        st.write(random.choice(response_templates) + response_text)

def generate_gpt_response(prompt):
    global conversation_history
    conversation_history += f"\nAI: {prompt}"
    # CSVデータをファイルとして一時的に保存
    csv_path = "temp_csv_file.csv"
    df.to_csv(csv_path, index=False)
    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        csv_path,  # 一時的なCSVファイルのパスを渡す
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    response = agent.run(prompt)
    os.remove(csv_path)  # 一時ファイルを削除

    # レスポンス内容を確認
    st.write("Response:", response)

    if 'message' in response and 'content' in response['message']:
        return response['message']['content']
    else:
        return "No further response received"

# データの読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    chat_with_csv(df)
