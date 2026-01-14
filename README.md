Project Title

Social-to-Lead Agentic Workflow for AutoStream

📌 Overview

This project implements a Conversational AI Agent for a fictional SaaS product AutoStream, which provides automated video editing tools for content creators.

The agent is designed to:

Understand user intent

Answer product and pricing questions using a local knowledge base (RAG)

Detect high-intent users

Capture qualified leads using a mock backend tool

The solution closely simulates a real-world social-to-lead conversion workflow, similar to how AI agents operate in platforms like WhatsApp or Instagram DMs.

🧠 Agent Capabilities
1️⃣ Intent Identification

The agent classifies user input into:

Greeting (e.g., “Hi”, “Hello”)

Pricing or product inquiry

High-intent lead (e.g., “Sign up”, “Buy”, “Try Pro plan”)

2️⃣ RAG-Powered Knowledge Retrieval

The agent answers pricing and feature-related questions using a local JSON-based knowledge source, which includes:

AutoStream pricing plans

Product features

Company policies

This ensures responses are grounded and accurate, not hallucinated.

3️⃣ Lead Capture Tool Execution

When a high-intent user is detected, the agent:

Requests name, email, and creator platform

Executes the mock_lead_capture() function only after all details are collected

Simulates backend lead submission

🏗️ Architecture Explanation (≈200 words)

This project uses LangGraph to build a stateful conversational agent, as it allows explicit control over conversation flow, memory, and tool execution.

LangGraph was chosen over a simple chain-based approach because:

It enables multi-step decision-making

State is persisted across multiple turns

Tool execution can be gated behind conditions (e.g., only after collecting all required inputs)

The agent maintains a structured state that includes:

user_input

detected intent

lead information (name, email, platform)

final agent response

Each user message flows through two main nodes:

Intent Detection Node – determines the user’s intent

Response Node – decides whether to answer using RAG, request details, or execute a tool

This architecture closely mirrors real production agent systems, where conversational logic, memory, and backend actions must be tightly controlled.

▶️ How to Run the Project Locally
cd autostream

2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the agent
python agent.py
