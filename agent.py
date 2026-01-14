import json
from typing import TypedDict

from langgraph.graph import StateGraph, END

with open("knowledge/autostream_knowledge.json", "r") as f:
    KNOWLEDGE = json.load(f)

def get_knowledge_context():
    return """
AutoStream Pricing & Features

Basic Plan:
- $29/month
- 10 videos/month
- 720p resolution

Pro Plan:
- $79/month
- Unlimited videos
- 4K resolution
- AI captions

Company Policies:
- No refunds after 7 days
- 24/7 support available only on Pro plan
"""
class AgentState(TypedDict):
    user_input: str
    intent: str
    name: str
    email: str
    platform: str
    response: str  


def detect_intent(state: AgentState):
    msg = state["user_input"].lower()

    if any(w in msg for w in ["hi", "hello", "hey"]):
        state["intent"] = "greeting"
    elif any(w in msg for w in ["price", "pricing", "plan", "cost"]):
        state["intent"] = "pricing"
    elif any(w in msg for w in ["buy", "try", "sign up", "pro plan"]):
        state["intent"] = "high_intent"
    else:
        state["intent"] = "unknown"

    return state
    
def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")

def respond(state: AgentState):
    intent = state["intent"]

    if intent == "greeting":
        state["response"] = "Hi! How can I help you with AutoStream today?"
        return state

    if intent == "pricing":
        state["response"] = get_knowledge_context()
        return state

    if intent == "high_intent":
        # Check if all required fields are present
        if not all([state.get("name"), state.get("email"), state.get("platform")]):
            state["response"] = "Great! To get started, please provide your name, email, and the platform you use (e.g., Name: Abc, Email: Abc@example.com, Platform: YouTube,Instagram)."
            return state
        else:
            
            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )
            state["response"] = "Lead captured successfully! Our team will contact you soon."
            return state

    state["response"] = "Can you please clarify your request?"
    return state


graph = StateGraph(AgentState)

graph.add_node("intent_detection", detect_intent)
graph.add_node("response", respond)

graph.set_entry_point("intent_detection")
graph.add_edge("intent_detection", "response")
graph.add_edge("response", END)

app = graph.compile()


if __name__ == "__main__":
    state = {
        "user_input": "",
        "intent": "",
        "name": "",
        "email": "",
        "platform": "",
        "response": ""
    }

    while True:
        user_text = input("User: ")
        state["user_input"] = user_text

        result = app.invoke(state)
        print("Agent:", result["response"])

        # If the agent asked for combined info, parse the next input
        if "provide your name, email" in result["response"].lower():
            combined_input = input("User: ")  # Get the combined response
            try:
               
                parts = [part.strip() for part in combined_input.split(',')]
                for part in parts:
                    if part.lower().startswith('name:'):
                        state["name"] = part.split(':', 1)[1].strip()
                    elif part.lower().startswith('email:'):
                        state["email"] = part.split(':', 1)[1].strip()
                    elif part.lower().startswith('platform:'):
                        state["platform"] = part.split(':', 1)[1].strip()
              
                result = app.invoke(state)
                print("Agent:", result["response"])
            except (IndexError, ValueError):
                print("Agent: Sorry, I couldn't parse that. Please try again in the format: Name: ..., Email: ..., Platform: ...")
                # Reset fields if parsing failed
                state["name"] = ""
                state["email"] = ""
                state["platform"] = ""
