"""
FREE Demo Chatbot - No API Key Required!
Works without any external services - completely local
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# Simple rule-based responses - no API needed!
def get_response(question):
    """Simple chatbot logic without external APIs"""
    question = question.lower().strip()
    
    # Greetings
    if any(word in question for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm a demo chatbot. Ask me about Python, data science, or machine learning!"
    
    # Python questions
    elif 'python' in question:
        return """Python is a high-level programming language known for:
        - Easy to learn syntax
        - Large ecosystem of libraries
        - Great for data science, web development, automation
        - Used by companies like Google, Netflix, Instagram
        
        Popular Python libraries: pandas, numpy, scikit-learn, tensorflow"""
    
    # Data Science
    elif any(word in question for word in ['data science', 'data scientist', 'analytics']):
        return """Data Science involves:
        1. Data Collection & Cleaning
        2. Exploratory Data Analysis (EDA)
        3. Feature Engineering
        4. Model Building & Training
        5. Model Evaluation & Deployment
        
        Key skills: Python, SQL, Statistics, Machine Learning, Data Visualization"""
    
    # Machine Learning
    elif any(word in question for word in ['machine learning', 'ml', 'model', 'algorithm']):
        return """Common ML Algorithms:
        
        Supervised Learning:
        - Linear/Logistic Regression
        - Decision Trees, Random Forest
        - SVM, Neural Networks
        
        Unsupervised Learning:
        - K-Means Clustering
        - PCA, t-SNE
        - DBSCAN
        
        Time Series:
        - ARIMA, SARIMA
        - LSTM, Prophet"""
    
    # LangChain
    elif 'langchain' in question:
        return """LangChain is a framework for building LLM applications:
        - Chains: Sequence operations together
        - Agents: Let LLMs use tools
        - Memory: Maintain conversation context
        - Prompts: Template management
        - Output Parsers: Structure LLM outputs
        
        Great for chatbots, Q&A systems, document analysis!"""
    
    # Time Series
    elif 'time series' in question or 'forecasting' in question:
        return """Time Series Forecasting Techniques:
        
        Statistical Methods:
        - ARIMA (AutoRegressive Integrated Moving Average)
        - SARIMA (Seasonal ARIMA)
        - Exponential Smoothing
        
        Machine Learning:
        - XGBoost, Random Forest
        - LSTM (Long Short-Term Memory)
        - Prophet (Facebook)
        
        Key Concepts: Stationarity, Seasonality, Trend, ACF/PACF"""
    
    # Projects
    elif 'project' in question:
        return """Great Data Science Projects:
        1. Customer Segmentation (RFM Analysis)
        2. Time Series Forecasting
        3. Sentiment Analysis
        4. Recommendation System
        5. Image Classification
        6. Credit Risk Prediction
        
        Build these for your portfolio!"""
    
    # Interview
    elif 'interview' in question:
        return """Data Science Interview Prep:
        
        Topics to Master:
        - Statistics & Probability
        - SQL & Data Manipulation
        - Machine Learning Algorithms
        - Python (pandas, numpy, sklearn)
        - Model Evaluation Metrics
        - Business Case Studies
        
        Practice: LeetCode, HackerRank, Kaggle competitions"""
    
    # Default response
    else:
        return f"""I understand you're asking about: "{question}"
        
        I can help with:
        - Python programming
        - Data Science concepts
        - Machine Learning algorithms
        - Time Series forecasting
        - LangChain framework
        - Interview preparation
        - Project ideas
        
        Try asking: "What is Python?" or "Explain machine learning" """


# Streamlit UI
st.title("🤖 FREE Demo Chatbot (No API Key Required!)")
st.caption("Built with LangChain + Streamlit | Completely Local")

# Info box
st.info("""
💡 **This is a FREE demo version**
- No API keys needed
- Runs completely on your machine
- Simple rule-based responses
- Great for testing the UI!

For AI-powered responses, you need:
- Option 1: Install Ollama (free, local AI)
- Option 2: Use OpenAI API key (paid, best quality)
""")

# Input
user_input = st.text_input("Ask me anything about Data Science, Python, or ML:", 
                           placeholder="e.g., What is machine learning?")

# Show some example questions
with st.expander("📝 Example Questions"):
    st.write("""
    - What is Python?
    - Explain machine learning
    - What is data science?
    - Tell me about time series forecasting
    - What is LangChain?
    - How to prepare for data science interview?
    - Suggest data science projects
    """)

# Response
if user_input:
    with st.spinner("Thinking..."):
        response = get_response(user_input)
        st.success("**Response:**")
        st.write(response)
    
    # Show conversation history
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        'question': user_input,
        'answer': response
    })
    
    # Display history
    if len(st.session_state.history) > 1:
        with st.expander("💬 Conversation History"):
            for i, conv in enumerate(reversed(st.session_state.history[:-1]), 1):
                st.write(f"**Q{i}:** {conv['question']}")
                st.write(f"**A{i}:** {conv['answer'][:100]}...")
                st.divider()

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **FREE Demo Chatbot**
    
    This is a simple demo that works WITHOUT any API keys or external services.
    
    **Upgrade Options:**
    
    1. **Ollama (FREE)**
       - Install: Download from ollama.ai
       - Run: `ollama serve`
       - Pull model: `ollama pull gemma2:2b`
       - Use: `localama.py`
    
    2. **OpenAI (PAID)**
       - Get API key from platform.openai.com
       - Add to `.env` file
       - Use: `app.py`
    """)
    
    st.divider()
    
    st.header("🛠️ Tech Stack")
    st.write("""
    - **Framework:** LangChain
    - **UI:** Streamlit
    - **Language:** Python
    - **Mode:** Local/Offline
    """)
    
    st.divider()
    
    st.header("📚 Learn More")
    st.write("""
    - [LangChain Docs](https://python.langchain.com)
    - [Streamlit Docs](https://docs.streamlit.io)
    - [Ollama Setup](https://ollama.ai)
    - [OpenAI API](https://platform.openai.com)
    """)
