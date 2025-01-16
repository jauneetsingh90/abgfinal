import streamlit as st
from modules.astra_retriever2 import retrieve_relevant_docs
from modules.llm_utils1 import generate_response_from_openai
from phoenix.otel import register
import phoenix as px
from modules.astra_logger import save_chat_to_astradb  

tracer_provider = register(
  project_name="default",
  endpoint="http://localhost:6006/v1/traces"
)


px.launch_app()
# Streamlit UI
st.title("💬 Conversational PDF Chatbot with AstraDB & OpenAI")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
query = st.chat_input("Ask something about your documents...")

if query:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve relevant pages
    retrieved_docs = retrieve_relevant_docs(query)

    if retrieved_docs:
        # Display Retrieved Pages with Images
        st.subheader("📄 Retrieved Pages")
        for doc in retrieved_docs:
            st.markdown(f"**📜 Page from:** `{doc['image_location']}`")
            st.markdown(f"**🔎 Relevance Score:** `{doc['score']:.4f}`")  # Print relevance score
            
            # Display Image if Available
            if doc["image_location"]:
                st.image(doc["image_location"], caption=f"Image from {doc['image_location']}", use_column_width=True)
            
            # Show Extracted Text
            st.write(doc['content'])
            st.write("---")

        # Generate response
        with st.chat_message("assistant"):
            response = generate_response_from_openai(query, retrieved_docs)
            st.markdown(response)

        # Store assistant response in chat history
        st.session_state["messages"].append({"role": "assistant", "content": response})
        # ✅ Store conversation in AstraDB
        save_chat_to_astradb(query, response)

    else:
        with st.chat_message("assistant"):
            st.markdown("❌ No relevant content found in AstraDB.")
        st.session_state["messages"].append({"role": "assistant", "content": "❌ No relevant content found in AstraDB."})