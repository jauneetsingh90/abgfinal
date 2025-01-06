import streamlit as st
from modules.astra_retriever import retrieve_relevant_docs
from modules.llm_utils import generate_response_from_openai

# Streamlit UI
st.title("🔍 PDF Content Retriever with AstraDB & OpenAI")

query = st.text_input("Enter your search query:", "")

if query:
    st.write("🔎 Searching AstraDB for relevant results...")

    retrieved_docs = retrieve_relevant_docs(query)

    if retrieved_docs:
        st.write("✅ Found relevant content! Sending to OpenAI for response...")
        
        openai_response = generate_response_from_openai(query, retrieved_docs)

        st.subheader("📜 AI Generated Response:")
        st.write(openai_response)

        st.subheader("📑 Retrieved Chunks:")
        for doc in retrieved_docs:
            st.markdown(f"**{doc['image_location']}**")
            st.write(doc['content'])
            st.write("---")

    else:
        st.warning("No relevant content found in AstraDB.")