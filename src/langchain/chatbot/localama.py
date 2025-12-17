from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv


# Load environment variables first
load_dotenv()

# Optional tracing if LangChain key is set
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant please respond to user query."),
        ("user", "Question:{question}"),
    ]
)


# Streamlit UI
st.title("English to French Translator (Ollama)")
user_input = st.text_input("Search the topic you want")


# Ollama LLM initialization (requires Ollama running and model pulled, e.g., `ollama pull gemma3`)
llm = Ollama(model="gemma3")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


if user_input:
    response = chain.invoke({"question": user_input})
    st.write(response)
