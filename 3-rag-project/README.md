<img width="1358" height="986" alt="image" src="https://github.com/user-attachments/assets/da6bbee3-1c48-4c25-b8b6-12b0ad4f86da" />
<img width="1293" height="970" alt="image" src="https://github.com/user-attachments/assets/90c341a4-0dce-4ff4-bf2d-31790736d0c9" />

# 🎨 פרויקט: Multi-Lingual Color Expert RAG

## 📌 סקירה כללית
פרויקט זה מיישם מערכת **RAG (Retrieval-Augmented Generation)** חכמה המתמחה בעולם הצבעים ושילוביהם. המערכת סורקת מאגר ידע מובנה (`JSON`) המכיל הנחיות, חוקי ערבוב ותיאוריות צבע. המערכת מאפשרת למשתמש לתחקר את המידע בצורה טבעית ולקבל תשובות מדויקות המבוססות אך ורק על המידע הקיים במאגר.

## 🎯 מטרות הפרויקט
* **מניעת "הזיות" (Hallucinations):** הגבלת התשובות להקשר (Context) של עולם הצבעים בלבד למניעת תשובות לא רלוונטיות.
* **תמיכה רב-לשונית:** שימוש במודל Embeddings מתקדם התומך בשאילתות בעברית ובאנגלית בצורה חלקה.
* **דיוק וקטורי:** שימוש בחיפוש סמנטי כדי למצוא תשובות גם כשהניסוח של המשתמש אינו זהה לכתוב במאגר.

## 🛠️ טכנולוגיות בשימוש
* **Framework:** [LangChain](https://python.langchain.com/) (ניהול ה-Chains וה-Retriever)
* **LLM & Embeddings:** [Cohere](https://cohere.com/) (Command-R, Multilingual-v3)
* **Vector DB:** [ChromaDB](https://www.trychroma.com/) (אחסון וחיפוש וקטורי מקומי)
* **UI:** [Streamlit](https://streamlit.io/)

## 🧩 מבנה המערכת (Workflow)
1. **Data Loading:** טעינת קובץ `colors_data.json` המכיל שאילתות ותשובות.
2. **Embedding & Indexing:** המרת המידע לוקטורים ואחסונם ב-ChromaDB.
3. **Retrieval:** שליפת המידע הרלוונטי ביותר בהתבסס על שאלת המשתמש.
4. **Augmented Generation:** שליחת המידע ל-LLM יחד עם הוראה (Prompt) לענות רק על סמך המידע שסופק.

## 🚀 הוראות הרצה
1. התקנת ספריות: 
   ```bash
   pip install langchain-cohere langchain-chroma streamlit python-dotenv
עדכון מפתח API בקובץ .env:
COHERE_API_KEY=your_key_here

הרצת האפליקציה:

Bash

streamlit run app.py
💡 דוגמאות לשימוש
"איזה צבע מתקבל מערבוב של כחול וצהוב?"

"מהו הצבע המשלים של סגול?"

"איך יוצרים צבע פסטל?" 
(המערכת תענה רק אם המידע קיים במאגר).

מגישה: שירה שניידמן

קורס: AI Agents - פרויקט 3 (RAG)
