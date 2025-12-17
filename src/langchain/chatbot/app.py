from langchain_openai import ChatOpenAI  # OpenAI chat model
from langchain_core.prompts import ChatPromptTemplate  # prompt templates
from langchain_core.output_parsers import StrOutputParser  # string output parser
import streamlit as st  # web UI
import os
from dotenv import load_dotenv  # load environment variables from .env


# Load environment variables first
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Fail fast with clear messages if keys are missing
if not OPENAI_API_KEY:
	st.error("Missing OPENAI_API_KEY in src/langchain/.env")
	raise SystemExit(1)

# Set env vars for SDKs
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
if LANGCHAIN_API_KEY:
	os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
	os.environ["LANGCHAIN_TRACING_V2"] = "true"  # optional tracing


# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
	[
		("system", "You are a helpful assistant please respond to user query."),
		("user", "Question:{question}"),
	]
)


# Streamlit UI
st.title("English to French Translator")
user_input = st.text_input("Search the topic you want")


# OpenAI LLM initialization
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if user_input:
	response = chain.invoke({"question": user_input})
	st.write(response)