from backend.services.ai_service import generate_reply




def generate_chat_feedback(client, message: str):
    prompt = f"""
        You are a professional AI assistant.
        Respond clearly, concisely, and directly to the user.
        Do not use lists, headings, or markdown.
        Limit the response to a maximum of 2–3 short sentences.
        Provide a single, continuous paragraph.
        The response must be in the same language as the user's message.
        Read the user's message carefully and answer it directly.
    
        User: {message}
        AI:
    """

    return generate_reply(client, prompt)
