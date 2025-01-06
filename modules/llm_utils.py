import openai
import os
import streamlit as st

# OpenAI API Key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

def generate_response_from_openai(query, retrieved_docs):
    """Uses OpenAI's LLM to generate a response based on retrieved AstraDB content."""
    
    context = "\n\n".join([doc["content"] for doc in retrieved_docs])
    
    system_prompt = f"""
    You are an AI assistant. Answer the query based on the retrieved content below.
    Answer in a markdown fasion, answer the key summary of response, then some bullet points if they are available, and then give refernece page numbers
    If the content is insufficient, provide a helpful but generic answer.
    
    Retrieved Content:
    {context}
    
    User Query: {query}
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}],
       
    )
    
    return response.choices[0].message.content
