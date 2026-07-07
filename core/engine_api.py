import os
from dotenv import load_dotenv
from google import genai

# Point to your local keys
load_dotenv()

# Multi-Key Session Boundaries
ingestor_client = genai.Client(api_key=os.getenv("GEMINI_KEY_RESEARCHER"))
configurator_client = genai.Client(api_key=os.getenv("GEMINI_KEY_WRITER"))
packager_client = genai.Client(api_key=os.getenv("GEMINI_KEY_EDITOR"))

# =====================================================================
# 🤖 GODOT PIPELINE SYSTEM PROMPTS (Strict Operational Bounding)
# =====================================================================

GODOT_INGESTOR_PROMPT = """
You are the Asset Ingestion & Validation Agent for a Godot 4 game engine pipeline.
Your task is to analyze the plain-text configuration files or directory structures provided.
Output a raw JSON manifest detailing available assets, file validations, and structural sanity checks.
Do not output markdown block text or introductory pleasantries.
"""

GODOT_CONFIGURATOR_PROMPT = """
You are the Godot Logic Configuration Builder.
Your task is to manipulate plain-text Godot file data structures (such as .tscn files or project.godot profiles).
You append node definitions, update script parameters, or modify game states programmatically.
Output the complete modified plain-text configuration code directly.
"""

GODOT_PACKAGER_PROMPT = """
You are the Release & Deployment Telemetry Builder.
Your job is to read build states and package up instructions for itch.io distribution via the Butler CLI.
Output a strict JSON package summarizing compilation logs, target export configurations, and butler deployment parameters.
"""
