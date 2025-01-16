import streamlit as st
import cassio

# Load AstraDB credentials
ASTRA_DB_APPLICATION_TOKEN = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_COLLECTION_NAME = "chat_history1"  # Change this if needed

# Initialize AstraDB Connection
cassio.init(
    database_id="600e85f6-8602-41b8-81f3-dc7d61545b3e",
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace="default_keyspace",
)

def save_chat_to_astradb(user_query, assistant_response):
    """Stores a conversation turn in AstraDB."""
    from langchain_community.vectorstores import Cassandra
    from langchain.embeddings import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
    vstore = Cassandra(embedding=embeddings, table_name=ASTRA_DB_COLLECTION_NAME)

    # Metadata to store chat context
    metadata = {
        "user_query": user_query,
        "assistant_response": assistant_response
    }

    # Store conversation in AstraDB
    vstore.add_texts(
        texts=[f"User: {user_query}\nAssistant: {assistant_response}"],
        metadatas=[metadata]
    )