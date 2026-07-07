import os
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI
from google import genai

# Normal local loading
load_dotenv()

# Initialize gateways
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =====================================================================
# 🤖 BOXED ROLE PROMPTS (Strict System Identity Enforcements)
# =====================================================================

CLAUDE_RESEARCH_PROMPT = """
You are the Investigative Reporter Agent for a technology newspaper. 
Your single job is to analyze a topic prompt and extract objective, hard facts.
Output ONLY raw factual bullet points based on your core knowledge. 
Do not write introductory prose or editorial filler.
"""

GPT_WRITER_PROMPT = """
You are the Lead Journalist Agent (GPT-4o Persona). 
You take raw factual research briefs and expand them into a compelling breaking news article.
You must strictly format your entire output using Markdown typography.
Maintain a crisp, objective, AP-style journalistic tone.
"""

GEMINI_EDITOR_PROMPT = """
You are the Lead Art Director & Formatting Agent (Gemini Persona).
Your job is to read a markdown draft and wrap it into a valid JSON response format.
The JSON payload must include exactly three keys: 
{
  "headline": "A catchy, short title",
  "body": "The full markdown body text here with newlines escaped",
  "formatting_verified": true
}
Output raw JSON only. Do not wrap it in markdown code blocks like ```json.
"""

# =====================================================================
# ⚡ THE MULTI-LLM API GATEWAYS
# =====================================================================

def call_research_agent(user_topic: str) -> str:
    print("\n[GATEWAY] Routing Phase 1 to Gemini 2.5 Flash (Research Agent)...")
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Research this topic: {user_topic}",
        config=genai.types.GenerateContentConfig(
            system_instruction=CLAUDE_RESEARCH_PROMPT
        )
    )
    return response.text

def call_writer_agent(research_brief: str) -> str:
    print("\n[GATEWAY] Routing Phase 2 to Gemini 2.5 Flash (Journalist Writer)...")
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Draft an article based on this brief:\n{research_brief}",
        config=genai.types.GenerateContentConfig(
            system_instruction=GPT_WRITER_PROMPT
        )
    )
    return response.text

def call_editor_agent(article_draft: str) -> str:
    print("\n[GATEWAY] Routing Phase 3 to Gemini 2.5 Flash (Formatting Editor)...")
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Format this draft into the specified JSON structure:\n{article_draft}",
        config=genai.types.GenerateContentConfig(
            system_instruction=GEMINI_EDITOR_PROMPT,
            response_mime_type="application/json"
        )
    )
    return response.text
