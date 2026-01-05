# ==============================
# CV Service - backend/services/cv_service.py
# ==============================

from backend.services.ai_service import generate_reply
from PyPDF2 import PdfReader
import docx

# ==============================
# Read CV file
# ==============================
async def read_cv_file(file):
    content = ""
    file_bytes = await file.read()

    if file.filename.endswith(".txt"):
        content = file_bytes.decode("utf-8")

    elif file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(file_bytes)
        reader = PdfReader("temp.pdf")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                content += page_text

    elif file.filename.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(file_bytes)
        doc = docx.Document("temp.docx")
        content = "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError("Unsupported file type")
    return content

# ==============================
# Generate CV feedback
# ==============================
def generate_cv_feedback(content: str, job_title: str, client):
    prompt = f"""
    You are a professional career coach and CV reviewer.

    Task:
    Analyze the CV content below for the role '{job_title}'.

    Instructions:
    1. Provide **concise, actionable feedback** in **6-7 lines max**, structured with bullet points.
    2. For each section (Summary, Skills, Experience/Projects, Education), give:
       - What to **highlight**
       - What to **remove or shorten**
       - What to **add or rephrase**, including **concrete example sentences or bullet points**
    3. Include **at least one new concrete suggestion** per section if something is missing.
    4. Focus **strictly on the CV content provided**; do not give general advice.
    5. **Respond in the same language as the job title**:
       - Hebrew job title → response in Hebrew
       - English job title → response in English

    CV content:
    {content}
    """

    return generate_reply(client, prompt)
