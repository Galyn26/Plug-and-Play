import os
import json
import subprocess
from engine_api import ingestor_client, configurator_client, GODOT_INGESTOR_PROMPT, GODOT_CONFIGURATOR_PROMPT, genai

# (Keep your working query_mcp_server function exactly the same)
def query_mcp_server(method: str, request_id: int) -> dict:
    process = subprocess.Popen(['python3', 'core/mcp_fs_server.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    payload = {"jsonrpc": "2.0", "method": method, "id": request_id}
    stdout_data, _ = process.communicate(input=json.dumps(payload) + "\n")
    try: return json.loads(stdout_data.strip()).get("result", {})
    except: return {}

def run_production_mesh():
    print("==================================================")
    print("🚀 LAUNCHING LIVE GODOT AUTOMATION ENGINE MESH")
    print("==================================================")
    
    SCENE_FILE_PATH = "core/workspace/godot_project/scenes/main.tscn"

    # Phase 1: Read the filesystem
    live_context = query_mcp_server("tools/list_files", request_id=101)
    
    # Phase 2: Call Ingestor to evaluate the files
    print("[GATEWAY] Phase 1: Analyzing directory state...")
    manifest_response = ingestor_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze this directory state:\n{json.dumps(live_context)}",
        config=genai.types.GenerateContentConfig(system_instruction=GODOT_INGESTOR_PROMPT, response_mime_type="application/json")
    )
    
    # Phase 3: Pass that analysis to the Configurator to mutate the .tscn code directly!
    print("\n[GATEWAY] Phase 2: Routing to Godot Configurator Agent...")
    
    # Read the current plain text of your main scene file
    with open(SCENE_FILE_PATH, "r") as f:
        current_scene_source = f.read()

    config_instruction = f"""
    The current scene source code is:
    {current_scene_source}

    Based on the Ingestion Manifest: {manifest_response.text}
    Modify the file to change the 'text' property of the GameStatusLabel node to read 'Engine Matrix Online - Orchestrated by Gemini'.
    Output ONLY the raw updated plain-text .tscn file source code. No explanation, no markdown ticks.
    """

    mutation_response = configurator_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=config_instruction,
        config=genai.types.GenerateContentConfig(system_instruction=GODOT_CONFIGURATOR_PROMPT)
    )

    # Safely write the updated source code straight back down to the disk block!
    with open(SCENE_FILE_PATH, "w") as f:
        f.write(mutation_response.text.strip())
        
    print("🟢 [SUCCESS] Godot plain-text scene mutated successfully!")

if __name__ == "__main__":
    run_production_mesh()
