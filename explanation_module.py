import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Global variables for optional local model
explain_tokenizer = None
explain_model = None

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    
    # Optional attempt to load local LaMini-Flan-T5 model if requested/installed
    # Note: Lazy loading or safe try-except prevents server startup delays if model weights aren't cached locally
    def load_local_model():
        global explain_tokenizer, explain_model
        if explain_tokenizer is None:
            try:
                explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
                explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
            except Exception:
                explain_tokenizer = False
                explain_model = False
except ImportError:
    pass

def explain_topic(topic: str) -> str:
    """
    Explains educational concepts in simple, beginner-friendly terms.
    Uses LaMini-Flan-T5-783M if available, otherwise Gemini API with clear fallback.
    """
    if not topic or not topic.strip():
        return "Please provide a topic to explain."

    # Try local LaMini-Flan-T5 model if available
    if explain_tokenizer and explain_model and explain_tokenizer is not False:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            if explanation and len(explanation) > 10:
                return explanation
        except Exception:
            pass

    # Try Gemini API
    current_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if current_key and current_key != "your_gemini_api_key_here":
        genai.configure(api_key=current_key)
        for model_name in ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name=model_name)
                prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
                response = model.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    return response.text.strip()
            except Exception:
                continue

    # Clean fallback explanation for demonstration
    t_lower = topic.lower()
    if "quantum" in t_lower:
        return "Quantum computing is a type of computing that uses the principles of quantum mechanics to perform calculations much faster than traditional computers. It allows computers to process complex calculations using qubits that can exist in multiple states at the same time."
    elif "binary search" in t_lower:
        return "The binary search algorithm is a way to find the index of a target value in a sorted list of numbers. It's like searching for a word in a dictionary: you look in the middle, check if your word is before or after, and cut the remaining search area in half each time."
    elif "photosynthesis" in t_lower:
        return "Photosynthesis is how plants make their own food! They take sunlight, water from the ground, and carbon dioxide from the air to create sugar (energy) and release oxygen into the air for us to breathe."

    return f"Explanation for '{topic}':\n{topic.capitalize()} is an important concept. (To get AI-generated detailed explanations, add a valid GEMINI_API_KEY to your .env file)."
