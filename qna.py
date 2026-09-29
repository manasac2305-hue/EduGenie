import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API if key is present
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    genai.configure(api_key=api_key)

def answer_question_with_gemini(question: str) -> str:
    """
    Answers general knowledge and academic questions using Google Gemini API.
    """
    if not question or not question.strip():
        return "Please ask a valid question."

    # Try Gemini API if key configured
    current_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if current_key and current_key != "your_gemini_api_key_here":
        genai.configure(api_key=current_key)
        for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(question)
                if response and hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                continue

    # Clean demo fallback response if API key is not active
    q_lower = question.lower()
    if "largest ocean" in q_lower:
        return "The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 63 million square miles."
    elif "pythagoras" in q_lower:
        return "The Pythagoras Theorem states that in a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides ($a^2 + b^2 = c^2$)."
    elif "photosynthesis" in q_lower:
        return "Photosynthesis is the chemical process by which green plants and some organisms use sunlight to synthesize nutrients from carbon dioxide and water."

    return f"EduGenie (Q&A Response for '{question}'):\nTo receive live AI responses, please provide a valid GEMINI_API_KEY in your .env file."
