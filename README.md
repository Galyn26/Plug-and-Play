# 🎮 Plug-and-Play (PnP)

**The AI-Driven Autonomous Game Studio Mesh**

`Plug-and-Play` is an advanced, protocol-first, multi-agent development matrix built using the **Model Context Protocol (MCP)**. Instead of trapped monolithic prompts, this system replicates a 
virtual, distributed game studio. By restricting specialized LLMs into hyper-focused "job roles" and equipping them with low-level infrastructural tools via MCP, the repository transforms a creative 
game design vision into verified, structured gameplay logic, asset pipelines, and deployment-ready software configurations.

No humans involved. You are the CEO/Publisher; they are your automated software execution mesh.

---

## 🏗️ Architectural Topology

The system operates like an event-driven task router (inspired by the Solace Agent Mesh). Agents do not engage in chaotic group chats; they publish structured state modifications (`.json` artifacts) 
to a shared workspace, passing strict boundaries and instructions down the hierarchy.

### 🧠 Cross-Model Strategic Allocation
To maximize processing performance and keep API resource credits optimal, specific models are assigned based on mathematical and technical strengths:
* **Claude 3.5 Sonnet / Opus:** Powers the **Technical Department & Infrastructure**. Handles complex state logic, terminal process execution, and system formatting.
* **GPT-4o:** Powers the **Design & Logic Department**. Handles structured coordinate layouts, node configurations, and gameplay rule graphs.
* **Gemini 1.5 Pro:** Powers the **Asset Pipeline Department**. Utilizes its massive context window to ingest entire asset manifests, frame rendering logs, and media configurations simultaneously.

---

## 🏢 Department Breakdown & Constraints

Agents perform 10x better when boxed into a role. Each sub-agent is strictly sandboxed by custom system prompts and specific MCP capability profiles.

### I. Technical Department (The Core Loop)
Responsible for executing scripts simulating the game frame loop lifecycle: Input Handling, State/Delta Time Calculations, Rendering Pipelines, and Audio Triggers.
* **Input & Window Sub-Agent:** Maps OS keystrokes and core tick rates.
* **State & Physics Sub-Agent:** Focuses strictly on coordinate vector math, delta time bounds, and boundary collision boundaries.
* *Tools via MCP:* Access to compiling runtimes, file validation, and system environment builders.

### II. Design & Logic Department (Core Mechanics)
Responsible for defining the player "verbs" and progression pathways.
* **Mechanics Sub-Agent:** Generates logic rules for entity states (e.g., jumping, health metrics, damage vectors).
* **Level & Layout Sub-Agent:** Translates structural design schemas into tight coordinate patterns.
* *Constraints:* Cannot execute host code directly; can only output raw schema contracts (e.g., JSON maps) for the Technical Dept to ingest.

### III. Asset Pipeline Department (Media & Manifests)
Responsible for structural verification of content rendering and audio bindings.
* **Visual Formatting Sub-Agent:** Validates sprite dimensions, texture maps, and formatting parameters.
* **Audio Processing Sub-Agent:** Hooks background scores and spatial event cues directly to internal triggers.

---

## 🛠️ Infrastructure Stack & MCP Layer

This repository focuses entirely on the **software orchestration and infrastructure layers** of game deployment. 

* **Orchestration:** Python-based asynchronous event routing engine (supporting LangGraph state frameworks for DAG-based execution).
* **Protocol:** Native Model Context Protocol (MCP) JSON-RPC standard.
* **Interface:** Beautiful, multi-pane terminal monitoring dashboard utilizing `Rich` / `Textual` in Python to inspect real-time agent execution streams, infrastructure load, and log generation.

---

## 🚀 The Operational Pipeline Flow

1. **The Executive Vision:** The CEO passes a prompt via the CLI dashboard: *"Build a 2D top-down cyberpunk room where hitting the spacebar changes the room's gravity."*
2. **Deconstruction:** The Head Manager breaks the vision into sub-tasks, routing data blueprints to respective Department Leads.
3. **Local Tool Execution:** Workers call local MCP servers to read template assets, manipulate configuration maps, or check build parameters.
4. **The Convergent Breakpoint:** Before anything is deployed to local infrastructure, the mesh hits an intentional execution breakpoint, presenting an approval dashboard in your terminal detailing 
system state, metrics, and generated schemas.
5. **Approve / Send Back:** You choose to approve production deployment or reject it with programmatic feedback that cascades back into the mesh.


![Agent Mesh](Images/Agent-Workflow.png)
