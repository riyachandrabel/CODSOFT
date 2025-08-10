# CHATBOT WITH RULE-BASED RESPONSES


#!/usr/bin/env python3
"""
chatbot.py – a minimal rule-based chatbot for learning purposes.
Run:
    python chatbot.py
Then type messages like:
    Hello
    What is your name?
    Weather in Paris
    bye
"""

import re
import sys

# ------------------------------------------------------------------
# 1.  Knowledge base / canned responses
# ------------------------------------------------------------------
RESPONSES = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there 👋",
        "Greetings, human!"
    ],
    "name": [
        "I'm RuleBot, your friendly rule-based assistant.",
        "People call me RuleBot."
    ],
    "how_are_you": [
        "I'm just code, but thanks for asking!",
        "Doing great—no bugs today!"
    ],
    "help": [
        "You can ask me about:\n"
        "• The weather in a city (e.g. \"weather in London\")\n"
        "• My name, age, or purpose\n"
        "• Simple math (e.g. \"calculate 3 + 5\")\n"
        "Or just say hi!"
    ],
    "thanks": [
        "You're welcome!",
        "Anytime 😊"
    ],
    "bye": [
        "Goodbye! Have a great day.",
        "See you later!"
    ],
    "unknown": [
        "Sorry, I didn't understand that. Type 'help' for things I can do.",
        "Hmm… could you rephrase?"
    ]
}

# ------------------------------------------------------------------
# 2.  Intent matching functions
# ------------------------------------------------------------------
def match_greeting(text: str) -> bool:
    return re.search(r"\b(hi|hello|hey|greetings?)\b", text, re.I) is not None

def match_name(text: str) -> bool:
    return re.search(r"\b(name|who are you)\b", text, re.I) is not None

def match_how_are_you(text: str) -> bool:
    return re.search(r"\b(how are you|how do you do)\b", text, re.I) is not None

def match_help(text: str) -> bool:
    return re.search(r"\bhelp\b", text, re.I) is not None

def match_thanks(text: str) -> bool:
    return re.search(r"\b(thank|thanks)\b", text, re.I) is not None

def match_bye(text: str) -> bool:
    return re.search(r"\b(bye|goodbye|quit|exit)\b", text, re.I) is not None

# ------------------------------------------------------------------
# 3.  Simple domain-specific handlers
# ------------------------------------------------------------------
def handle_weather(text: str) -> str | None:
    """
    Recognizes patterns like:
        weather in <city>
        what's the weather like in <city>
    Returns a canned response if matched, else None.
    """
    m = re.search(r"\bweather\b.*?\b(?:in|at|for)\s+([a-zA-Z\s]+)", text, re.I)
    if m:
        city = m.group(1).strip()
        return f"Right now in {city.title()} it's sunny with a gentle breeze ☀️ (simulated)."
    return None

def handle_math(text: str) -> str | None:
    """
    Very small math evaluator: 3+5, 10 - 2, etc.
    Uses eval() for brevity; in production you'd use a safe parser.
    """
    math_expr = re.search(r"\b(?:calculate|math|compute)\s*([0-9+\-*/\s().]+)", text, re.I)
    if not math_expr:
        # Also try simple standalone expressions like "3+5"
        math_expr = re.search(r"^([\d+\-*/().\s]+)$", text.strip())

    if math_expr:
        expr = math_expr.group(1).strip()
        try:
            result = eval(expr)
            return f"{expr} = {result}"
        except Exception:
            return "I couldn't compute that expression."
    return None

# ------------------------------------------------------------------
# 4.  Main chat loop
# ------------------------------------------------------------------
def get_response(user_input: str) -> str:
    """Returns a single string response given user input."""
    user_input = user_input.strip()
    if not user_input:
        return "Say something!"

    # 1.  Check domain-specific handlers first
    weather = handle_weather(user_input)
    if weather:
        return weather

    math_res = handle_math(user_input)
    if math_res:
        return math_res

    # 2.  Check generic intents
    if match_greeting(user_input):
        return RESPONSES["greeting"][0]
    if match_name(user_input):
        return RESPONSES["name"][0]
    if match_how_are_you(user_input):
        return RESPONSES["how_are_you"][0]
    if match_help(user_input):
        return RESPONSES["help"][0]
    if match_thanks(user_input):
        return RESPONSES["thanks"][0]
    if match_bye(user_input):
        return RESPONSES["bye"][0]

    # 3.  Fallback
    return RESPONSES["unknown"][0]

def main():
    print("RuleBot: Hello! Type 'bye' to exit.")
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nRuleBot: Interrupted. Bye!")
            break

        reply = get_response(user)
        print("RuleBot:", reply)

        if match_bye(user):
            break

if __name__ == "__main__":
    main()