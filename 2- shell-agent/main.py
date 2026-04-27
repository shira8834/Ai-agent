import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# פונקציית עזר לקריאת הפרומפט מהקובץ
def get_prompt(level):
    file_path = f"prompts/level-{level}.md"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def translate_to_cli(user_input):
    system_instructions = get_prompt(3) 
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_input}
            ],
            temperature=0.0 
        )
        
        command = completion.choices[0].message.content
        return command.strip()
    
    except Exception as e:
        return f"שגיאה בהתחברות למודל: {str(e)}"

with gr.Blocks(title="CLI Agent v1") as demo:
    gr.Markdown("# 🤖 CLI Agent - Version 1.0")
    gr.Markdown("הקלידי הוראה בעברית או באנגלית וקבלי פקודת טרמינל (Windows)")
    
    with gr.Row():
        user_text = gr.Textbox(placeholder="לדוגמה: תראה לי את כתובת ה-IP שלי", label="הוראה חופשית")
        output_text = gr.Textbox(label="פקודת CLI")
    
    submit_btn = gr.Button("תרגם לפקודה")
    submit_btn.click(fn=translate_to_cli, inputs=user_text, outputs=output_text)

if __name__ == "__main__":
    demo.launch()