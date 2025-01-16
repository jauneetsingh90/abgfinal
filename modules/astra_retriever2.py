import streamlit as st
import cassio
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Cassandra


# Load AstraDB Token from Streamlit Secrets
ASTRA_DB_APPLICATION_TOKEN = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]

# Enable Phoenix Tracing for LangChain


# Initialize Cassandra Connection
cassio.init(
    database_id="600e85f6-8602-41b8-81f3-dc7d61545b3e",
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace="default_keyspace",
)

def retrieve_relevant_docs(query, top_k=3):
    """Retrieves relevant text chunks from AstraDB vector store with relevance scores."""
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
    vstore = Cassandra(embedding=embeddings, table_name="pdf_text_storage")

    results = vstore.similarity_search_with_score(query, k=top_k)  # Use search with score

    retrieved_docs = []
    for doc, score in results:
        retrieved_docs.append({
            "content": doc.page_content,
            "image_location": doc.metadata.get("image_location", None),  # Extract stored image path
            "score": score  # Include relevance score
        })

    

    return retrieved_docs