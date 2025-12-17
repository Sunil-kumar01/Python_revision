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

###till now streamlit was done and langchain thing was done in a chain basis for the paid keys which will be charged based on tokens and monotoring will be done in langchain cloud for cost and usage###
###Now we will do the same thing using langchain chatbot framework where we will create an agent which will use the same llm and prompt template but will have more features like memory, tool usage etc###
# Note: Make sure to run this script with `streamlit run src/langchain/chatbot/app.py`

#now let us use the ollama for the free key and which is opensource