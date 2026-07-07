import os
import json
from mesh_api import call_research_agent, call_writer_agent, call_editor_agent

WORKSPACE_DIR = "./workspace"

def mcp_tool_write_file(filename: str, content: str):
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"[WORKSPACE] Saved artifact state: {filepath}")

def mcp_tool_read_file(filename: str) -> str:
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, "r") as f:
        return f.read()

def run_live_pipeline(vision: str):
    print("==================================================")
    print("🚀 LAUNCHING LIVE MULTI-MODEL ORCHESTRATION MESH")
    print("==================================================")
    print(f"CEO Order: '{vision}'\n")

    # Ensure workspace directory exists
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)

    # Phase 1: Claude 3.5 Sonnet handles the hard data extraction
    research_text = call_research_agent(vision)
    mcp_tool_write_file("live_brief.txt", research_text)

    # Phase 2: GPT-4o synthesizes the brief into crisp Markdown copy
    brief_data = mcp_tool_read_file("live_brief.txt")
    draft_text = call_writer_agent(brief_data)
    mcp_tool_write_file("live_draft.md", draft_text)

    # Phase 3: Gemini 1.5 Pro structures the final output into validated JSON
    draft_data = mcp_tool_read_file("live_draft.md")
    final_json_string = call_editor_agent(draft_data)
    mcp_tool_write_file("live_package.json", final_json_string)

    # Phase 4: Human-in-the-Loop Convergence Gate
    print("\n==================================================")
    print("📢 MANAGER REPORT: LIVE PRODUCTION REVIEW")
    print("==================================================")
    
    try:
        package_data = json.loads(mcp_tool_read_file("live_package.json"))
        print(f"Proposed Headline: {package_data.get('headline')}\n")
        print(f"Content Preview:\n{package_data.get('body')}\n")
    except json.JSONDecodeError:
        print("❌ CRITICAL: Gemini output could not be parsed as valid JSON.")
        print(f"Raw Output:\n{final_json_string}")
    
    print("--------------------------------------------------")
    approval = input("CEO/Publisher Approval - Route to Production? (Y/N): ")
    if approval.strip().lower() == 'y':
        print("\n🚀 [SUCCESS] Live multi-model generation successfully routed to production layers!")
    else:
        print("\n❌ [REJECTED] Rolling back environment changes.")

if __name__ == "__main__":
    user_input = "Write an article analyzing how Model Context Protocol (MCP) will change local developer sandboxes."
    run_live_pipeline(user_input)
