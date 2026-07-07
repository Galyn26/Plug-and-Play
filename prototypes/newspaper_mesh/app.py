import os
import json

# Define our mock workspace directory
WORKSPACE_DIR = "./workspace"

# =====================================================================
# 🛠️ MOCK MCP SERVER TOOLS (The Core Infrastructure)
# =====================================================================
def mcp_tool_fetch_research(topic: str) -> str:
    """Simulates a Search/Fetch MCP server returning raw brief text."""
    print(f"[MCP TOOL] Fetching web data for: '{topic}'...")
    # Triple quotes allow the string to safely break across multiple lines
    mock_brief = f"""RAW DATA BRIEF ON {topic.upper()}:
- Fact 1: Major breakthrough announced this week.
- Fact 2: Industry open-source adoption is up 40%.
- Fact 3: Deployment velocity has doubled due to automated pipelines."""
    return mock_brief

def mcp_tool_write_file(filename: str, content: str):
    """Simulates a Filesystem MCP server writing an artifact state."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"[MCP TOOL] State modification written to: {filepath}")

def mcp_tool_read_file(filename: str) -> str:
    """Simulates a Filesystem MCP server reading an artifact state."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r") as f:
        return f.read()

# =====================================================================
# 🤖 THE AGENT DEPARMENTS (Hyper-Focused Constraints)
# =====================================================================
def run_research_agent(prompt: str) -> str:
    """BOXED ROLE: Ingests a prompt, extracts facts via Fetch MCP tool."""
    print("\n[AGENT] Running Research Agent (Claude/Gemini Persona)...")
    raw_brief = mcp_tool_fetch_research(prompt)
    
    # Save the output artifact state to the mesh workspace
    mcp_tool_write_file("research_brief.txt", raw_brief)
    return "research_brief.txt"

def run_writer_agent(brief_file: str) -> str:
    """BOXED ROLE: Reads the research brief, outputs structured copy."""
    print("\n[AGENT] Running Journalist Writer Agent (GPT-4o Persona)...")
    raw_data = mcp_tool_read_file(brief_file)
    
    # Process the text (simulating LLM writing logic)
    article_draft = f"# BREAKING NEWS STORY\n\n{raw_data}\n\n*Draft written in AP style by Automated Journalist Agent.*"
    
    # Save draft artifact
    mcp_tool_write_file("article_draft.md", article_draft)
    return "article_draft.md"

def run_copy_editor_agent(draft_file: str) -> str:
    """BOXED ROLE: Formats and adds regulatory metadata boundaries."""
    print("\n[AGENT] Running Copy Editor Agent (Claude Persona)...")
    draft_content = mcp_tool_read_file(draft_file)
    
    # Wrap content inside finalized validation template
    finalized_package = {
        "status": "PENDING_PUBLISHER_APPROVAL",
        "headline": "The Automated Automation Dawn",
        "body": draft_content,
        "formatting_verified": True
    }
    
    mcp_tool_write_file("final_package.json", json.dumps(finalized_package, indent=4))
    return "final_package.json"

# =====================================================================
# 🎛️ THE MANAGER / ORCHESTRATOR LOOP (The Producer)
# =====================================================================
def start_newspaper_pipeline(vision: str):
    print(f"=== INITIALIZING NEWSPAPER ORCHESTRATION MESH ===")
    print(f"CEO Order: '{vision}'")
    
    # Phase 1: Research
    brief_artifact = run_research_agent(vision)
    
    # Phase 2: Write
    draft_artifact = run_writer_agent(brief_artifact)
    
    # Phase 3: Format & Edit
    final_json_artifact = run_copy_editor_agent(draft_artifact)
    
    # Phase 4: Human-in-the-Loop Convergence Gate
    print("\n==================================================")
    print("📢 MANAGER REPORT: PIPELINE READY FOR REVIEW")
    print("==================================================")
    
    package_data = json.loads(mcp_tool_read_file(final_json_artifact))
    print(f"Proposed Headline: {package_data['headline']}")
    print(f"Status: {package_data['status']}")
    print(f"Content Preview:\n{package_data['body']}")
    print("--------------------------------------------------")
    
    # Interactive CLI verification command
    approval = input("CEO/Publisher Approval - Route to Production? (Y/N): ")
    if approval.strip().lower() == 'y':
        print("\n🚀 [SUCCESS] Article Published Live to Production Infrastructure!")
    else:
        print("\n❌ [REJECTED] Rolling back changes. Sending notes back to Manager Agent.")

if __name__ == "__main__":
    # Create workspace if it doesn't exist
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
        
    user_input = "Write a front-page story on the rise of local infrastructure automation tools"
    start_newspaper_pipeline(user_input)
