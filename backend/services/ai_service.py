import re

def normalize_reply(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)   # bold -> text
    text = re.sub(r"\*(.*?)\*", r"\1", text)       # italic -> text
    text = re.sub(r"`(.*?)`", r"\1", text)         # code -> text

    text = re.sub(r"\n\s*[-•*]\s*", ". ", text)
    text = re.sub(r"\n\s*\d+\.\s*", ". ", text)

    text = re.sub(r"\n+", " ", text)

    text = re.sub(r"\s{2,}", " ", text)

    sentences = re.split(r'(?<=[.!?])\s', text)
    return " ".join(sentences)




def chat_generate_reply(client ,message:str) -> str:
    try:
        system_prompt = (
            "אתה עוזר חכם שמגיב תמיד למשתמש. "
            "ענה תמיד בקצרה ולעניין. "
            "בלי רשימות, בלי כותרות, בלי Markdown. "
            "מקסימום 2–3 משפטים קצרים. "
            "תשובה רציפה בפסקה אחת. "
            "השפה של התשובה חייבת להיות באותה שפה שבה המשתמש כתב את ההודעה. "
            "עכשיו קרא את ההודעה של המשתמש וענה עליה ישירות."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                system_prompt,
                f"User: {message}\nAI:"
            ]
        )
        return normalize_reply(response.text)

    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        return f"[MOCK RESPONSE] Echo: {message}"




def cv_generate_reply(client, prompt: str) -> str:
    """
    Call the AI client with the given prompt and return the response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )
        return normalize_reply(response.text)

    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        return "[MOCK RESPONSE] Error generating CV feedback"










