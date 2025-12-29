# backend/services/cv_service.py
from backend.services.ai_service import generate_reply
from PyPDF2 import PdfReader
import docx

async def read_cv_file(file):
    """Read uploaded CV file (txt, pdf, docx) and return text content."""

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

def generate_cv_feedback(content: str, job_title: str, client):
    """Generate concise AI feedback for CV targeting a specific job title."""
    prompt = f"""
                You are an expert career coach.
                Analyze this CV text for the role '{job_title}'.
                Give concise feedback in 6 short sentences max.
                Focus on what to highlight or improve for {job_title} roles, clarity, skills, and achievements.
                CV content:
                
                {content}
            """
    return generate_reply(client, prompt)

