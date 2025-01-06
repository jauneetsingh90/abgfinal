import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Cassandra
import cassio

# AstraDB Configuration
ASTRA_DB_ID="600e85f6-8602-41b8-81f3-dc7d61545b3e"
ASTRA_DB_APPLICATION_TOKEN=""
OPENAI_API_KEY=""

cassio.init(
    database_id=ASTRA_DB_ID,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace="default_keyspace",
)

def retrieve_relevant_docs(query, top_k=5):
    """Retrieves relevant text chunks from AstraDB vector store."""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vstore = Cassandra(embedding=embeddings, table_name="pdf_text_storage")

    results = vstore.similarity_search(query, k=top_k)

    retrieved_docs = []
    for doc in results:
        retrieved_docs.append({
            "content": doc.page_content,
            "image_location": doc.metadata.get("image_location", "Unknown File"),
        })

    return retrieved_docs
