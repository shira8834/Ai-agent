import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. הגדרות וטעינה
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

st.set_page_config(page_title="צ'אט הצבעים שלי", page_icon="🎨")
st.title("🎨 מומחה הצבעים (RAG)")

# 2. פונקציית טעינת הנתונים (בדיוק כמו ב-rag_app.py)
@st.cache_resource
def get_retriever():
    with open("colors_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    documents = [
        Document(page_content=f"שאלה: {item['question']} תשובה: {item['answer']}") 
        for item in data
    ]
    
    embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=api_key)
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 2})

retriever = get_retriever()
llm = ChatCohere(model="command-r-08-2024", cohere_api_key=api_key)

# 3. התבנית ה"קשוחה" שעבדה לך
template = """את/ה עוזר/ת מומחה/ית. משימתך היא לענות על שאלת המשתמש בהתבסס אך ורק על ההקשר שסופק.

הקשר:
---
{context}
---

שאלה:
{question}

הוראות:
- ענה על שאלת המשתמש באמצעות המידע המסופק ב"הקשר" שלעיל בלבד.
- אם ה"הקשר" אינו מכיל מספיק מידע כדי לענות על השאלה, ציין בבירור: "אני מצטער, אך המסמכים שסופקו אינם מכילים מספיק מידע כדי לענות על שאלה זו."
- אל תשתמש בידע קודם כלשהו.
"""

prompt = ChatPromptTemplate.from_template(template)

# פונקציית עזר לפורמט הטקסט
def format_docs(docs):
    return "\n---\n".join(doc.page_content for doc in docs)

# 4. בניית השרשרת
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 5. ממשק הצ'אט של Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("שאל אותי על צבעים..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # הרצה של השרשרת בדיוק כמו בטרמינל
        response = rag_chain.invoke(user_input)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})