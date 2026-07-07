import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load your root environment variables
load_dotenv()

# Initialize the Manager Client specifically with its own key container
manager_client = genai.Client(api_key=os.getenv("GEMINI_KEY_MANAGER"))

MANAGER_SYSTEM_PROMPT = """
You are the Manager / Producer Agent of an autonomous game studio mesh.
Your job is to deconstruct the CEO's creative vision into structural, specialized JSON task blocks for your departments.

You must output a single, valid JSON object matching this exact schema:
{
  "task_id": "unique_string",
  "executive_summary": "High level overview of the feature",
  "allocations": {
    "technical_dept": "Explicit instructions for scene configurations and terminal execution",
    "design_dept": "Explicit instructions for game mechanics coordinates and node tracking logic",
    "asset_dept": "Explicit instructions for sprite dimensions and audio file validations"
  }
}
Do not wrap your output in markdown text blocks. Output raw JSON only.
"""

def generate_studio_tasks(ceo_prompt: str):
    print("\n[MANAGER] Ingesting CEO Executive Direction...")
    print(f"[VISION] \"{ceo_prompt}\"")
    print("[MANAGER] Dispatching orchestration pass via Gemini Pro...")

    try:
        response = manager_client.models.generate_content(
            model='gemini-2.5-flash', # High intelligence reasoning model
            contents=f"CEO Input: {ceo_prompt}",
            config=types.GenerateContentConfig(
                system_instruction=MANAGER_SYSTEM_PROMPT,
                response_mime_type="application/json"
            )
        )
        
        # Parse and save the generated task state matrix
        task_matrix = json.loads(response.text.strip())
        workspace_state_path = "core/workspace/state_matrix.json"
        
        with open(workspace_state_path, "w") as f:
            json.dump(task_matrix, f, indent=4)
            
        print("\n🟢 [SUCCESS] Manager has successfully written the state matrix!")
        print(f"[STATE] Task matrix saved to: {workspace_state_path}")
        print("==================================================")
        print(json.dumps(task_matrix, indent=2))
        print("==================================================")
        
    except Exception as e:
        print(f"\n❌ MANAGER CRITICAL ERROR: Orchestration pass failed:\n{e}")

if __name__ == "__main__":
    # Simulate a direct prompt from you, the CEO
    test_prompt = "Build a 2D top-down cyberpunk room where hitting the spacebar changes gravity."
    generate_studio_tasks(test_prompt)
