import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain.vectorstores import AstraDB
from cassandra.cluster import Cluster
from langchain_community.vectorstores import Cassandra
import cassio

import cassio

# AstraDB Configuration
ASTRA_DB_ID="600e85f6-8602-41b8-81f3-dc7d61545b3e"
ASTRA_DB_APPLICATION_TOKEN=""
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

cassio.init(
    database_id=ASTRA_DB_ID,
    token=ASTRA_DB_APPLICATION_TOKEN,
    keyspace="default_keyspace",
)

def store_in_astradb(texts, image_files):
    """Stores extracted text descriptions in AstraDB."""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vstore = Cassandra(embedding=embeddings, table_name="pdf_text_storage")

    metadata_list = []
    for idx, text in enumerate(texts):
        metadata_list.append({"image_location": image_files[idx], "chunk_number": idx + 1})

    vstore.add_texts(texts, metadata_list)
