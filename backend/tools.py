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
    return "".join(sentences)

