# imports
import pandas as pd
import numpy as np
import streamlit as st  # Streamlitを追加
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken
import os
import openai

# Streamlitアプリのタイトル
st.title('💕CSV File Uploader and Similarity Calculator')

# Streamlitのサイドバーを使用してAPIキーを入力させる
user_api_key = st.sidebar.text_input(
    label="OpenAI API key",
    placeholder="Paste your OpenAI API key here",
    type="password")

# OpenAI APIキーを設定
if user_api_key:
    openai.api_key = user_api_key
else:
    st.error("Please enter your OpenAI API key in the sidebar.")

# CSVファイルをアップロード
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Tiktokenのエンコーディングを取得
embedding_encoding = "cl100k_base"
encoding = tiktoken.get_encoding(embedding_encoding)

# 最大トークン数
max_tokens = 8000

# 類似度計算のトップN
top_n = 5

# データフレームを格納する変数
df = None

if uploaded_file is not None:
    # アップロードされたCSVファイルをDataFrameとして読み込む
    df = pd.read_csv(uploaded_file)

    # ユーザーのクエリ
    user_query = st.text_input("Enter a query:")

    # データフレームをStreamlitで表示
    st.subheader("Uploaded Data:")
    st.write(df)

    # 類似度の計算ボタン
    if st.button("Calculate Similarity"):
        # Tiktokenのエンコーディングを取得

        # データのトークン数を計算し、条件に合致するデータをフィルタリング
        df["n_tokens"] = df.keyword.apply(lambda x: len(encoding.encode(str(x))))
        df = df[df.n_tokens <= max_tokens]

        # データの埋め込みを計算
        df["embedding"] = df.keyword.apply(lambda x: get_embedding(str(x)))

        # ユーザークエリの埋め込みを計算
        embedding = get_embedding(
            user_query,
        )

        # データとの類似度を計算
        df["similarities"] = df.embedding.apply(lambda x: cosine_similarity(x, embedding))

        # 類似度の高いデータを取得して表示または保存
        res = (df.sort_values("similarities", ascending=False).head(top_n))
        st.subheader("Top Similar Items:")
        st.write(res)
