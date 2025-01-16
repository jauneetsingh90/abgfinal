import streamlit as st
import openai
import phoenix as px
from datetime import datetime
import os
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor



tracer_provider = register(
  project_name="default",
  endpoint="http://localhost:6006/v1/traces"
)


OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
# Load Azure OpenAI credentials from Streamlit Secrets
# Log query to Phoenix Arize
   
# OpenAI API Key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Enable Phoenix Tracing for LangChain


def generate_response_from_openai(query, retrieved_docs):
    """Uses OpenAI's LLM to generate a response based on retrieved AstraDB content."""

    context = "\n\n".join([f"(Relevance: {doc['score']:.4f}) {doc['content']}" for doc in retrieved_docs])

    system_prompt = f"""
    You are an AI assistant. Answer the query based on the retrieved content below.
    If the content is insufficient, provide a helpful but generic answer.

    Retrieved Content:
    {context}

    User Query: {query}
    """
    # Log query to Phoenix Arize
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}]
    )

    return response.choices[0].message.content