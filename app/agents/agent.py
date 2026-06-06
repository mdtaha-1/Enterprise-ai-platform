from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from app.rag.pipeline import query_documents
import os
from dotenv import load_dotenv

load_dotenv()

# Define tools the agent can use
@tool
def search_documents(query: str) -> str:
    """Search through uploaded documents to answer questions about their content."""
    return query_documents(query)

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Input should be a valid Python math expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def summarize_topic(topic: str) -> str:
    """Get a detailed explanation or summary of any topic using AI knowledge."""
    from app.core.llm import chat
    return chat(topic, system_prompt="You are an expert assistant. Give a clear, concise summary.")

# Build the agent
def get_agent():
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )

    tools = [search_documents, calculate, summarize_topic]

    agent = create_react_agent(llm, tools)
    return agent

def run_agent(user_input: str) -> str:
    agent = get_agent()
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    return result["messages"][-1].content