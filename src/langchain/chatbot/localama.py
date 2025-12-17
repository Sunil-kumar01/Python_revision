from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
import json
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
	os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
	os.environ["LANGCHAIN_TRACING_V2"] = "true"

prompt = ChatPromptTemplate.from_messages([
	("system", "You are a helpful assistant please respond to user query."),
	("user", "Question:{question}"),
])

st.title("this ChatBot helps in answering created by Sunil Kumar")
user_input = st.text_input("Search the topic you want")

MODEL_NAME = "gemma3:1b"
BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
llm = Ollama(model=MODEL_NAME, temperature=0.7, base_url=BASE_URL)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

st.caption(f"Using model: {MODEL_NAME} | base_url: {BASE_URL}")

try:
	with urlopen(f"{BASE_URL}/api/tags", timeout=2) as resp:
		data = json.load(resp)
		models = [m.get("name") for m in data.get("models", [])]
		st.caption("Ollama models: " + ", ".join(models) if models else "(none)")
except Exception as e:
	st.caption(f"Ollama models fetch error: {e}")

if user_input:
	try:
		response = chain.invoke({"question": user_input})
		st.write(response)
	except Exception as e:
		st.error(f"Model call failed: {e}")
