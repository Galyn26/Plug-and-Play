import os
import json
from engine_api import ingestor_client, GODOT_INGESTOR_PROMPT, genai

def verify_pipeline():
    print("==================================================")
    print("🚦 RUNNING PRODUCTION CORE INTEGRATION TEST")
    print("==================================================")
    
    # Simple check to ensure credentials exist in environment
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY not found in environment.")
        return

    print("[TEST] Sending mock Godot directory layout to Ingestor Client...")
    
    # Mock file-structure data to simulate what your future MCP server will pass
    mock_input = """
    Project Directory Layout:
    - /project.godot
    - /scenes/main.tscn
    - /assets/player_sprite.png
    """

    try:
        # Run a live test call to ensure your key and package work together
        response = ingestor_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this directory:\n{mock_input}",
            config=genai.types.GenerateContentConfig(
                system_instruction=GODOT_INGESTOR_PROMPT,
                response_mime_type="application/json"
            )
        )
        
        print("\n🟢 [SUCCESS] API Gateway Communication Stable!")
        print("==================================================")
        print("📢 INGESTOR MODEL MANIFEST RESPONSE:")
        print("==================================================")
        print(response.text)
        print("--------------------------------------------------")
        
    except Exception as e:
        print(f"\n❌ CRITICAL: Verification failed with error:\n{e}")

if __name__ == "__main__":
    verify_pipeline()
