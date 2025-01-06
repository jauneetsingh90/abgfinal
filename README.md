**This application is a chatbot app on the pdf/reports which has lot of tables/graphs**

**Secrets**
create a secret file by adding .streamlit/secrets.toml like
OPENAI_API_KEY="xyz"
Add all the secrets for gemini and AstraDB here like example below.


**Loading pdf into vector**
Run the below command
#streamlit run app.py

**Retriever Application**
#streamlit run retriever_app.py


**Notes**
Change the prompt for extracting data in gemini_utils.py file, same way for retriever you can add the prompt in astra_retriever.py which are in the modules folder.


**Reach to me @jauneet.singh@datastax.com for any queries**

