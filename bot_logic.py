import google.generativeai as genai

SYSTEM_PROMPT = """You are WanderBot, a friendly and knowledgeable travel assistant.

Rules:
1. ONLY answer travel-related questions: destinations, itineraries, hotels, flights, visas, packing, budgets, local culture, food, transport, weather, safety tips, etc.
2. If the user greets you (hi, hello, hey, etc.), reply warmly and briefly — 1-2 sentences max.
3. Keep ALL answers short, clear, and well-structured. Use bullet points or numbered lists for itineraries and tips.
4. If asked about anything NOT travel-related (math, coding, politics, general knowledge, etc.), politely decline and redirect: "I'm a travel specialist! Ask me anything about your next trip. ✈️"
5. Be enthusiastic, warm, and helpful. Use travel emojis occasionally.
"""


def configure_gemini(api_key: str):
    """Configure the Gemini API with the provided key."""
    genai.configure(api_key="AIzaSyBre1Ghb49qRoLfQyAWw3_isWSg_x1o7V8")


def get_bot_response(api_key: str, messages: list, user_input: str) -> str:
    """
    Send user message to Gemini and return the bot's reply.

    Args:
        api_key   : Gemini API key
        messages  : List of prior messages [{"role": "user"/"assistant", "content": "..."}]
        user_input: Latest user message

    Returns:
        Bot reply string
    """
    try:
        configure_gemini(api_key)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )

        # Build Gemini-format history (exclude the latest user message)
        history = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            history.append({"role": role, "parts": [m["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(user_input.strip())
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
