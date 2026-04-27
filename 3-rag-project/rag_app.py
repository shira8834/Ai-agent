import os
import json
import cohere
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

# 1. טעינת מפתח ה-API מהקובץ .env
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("⚠️ לא נמצא API KEY, ודא שהגדרת אותו בקובץ .env")

# 2. הגדרת המודלים של Cohere (ענן - ללא הורדה למחשב)
embeddings = CohereEmbeddings(model="embed-multilingual-v3.0", cohere_api_key=api_key)
llm = ChatCohere(model="command-r-08-2024", cohere_api_key=api_key)

# 3. טעינת נתוני הצבעים מה-JSON
with open("colors_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [
    Document(page_content=f"שאלה: {item['question']} תשובה: {item['answer']}") 
    for item in data
]

# 4. יצירת בסיס הנתונים הווקטורי בזיכרון
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 5. הגדרת התבנית המדויקת שלך
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
- היה תמציתי ואל תחזור על ההקשר מילה במילה.
"""

prompt = ChatPromptTemplate.from_template(template)

# 6. בניית השרשרת (Chain)
def format_docs(docs):
    return "\n---\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. הרצה לבדיקה
if __name__ == "__main__":
    query = input("שאל שאלה על צבעים (למשל: מה יוצא מאדום וצהוב?): ")
    print("\nבודק במסמכים ומייצר תשובה...\n")
    response = rag_chain.invoke(query)
    print(f"תשובה: {response}")