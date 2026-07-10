# MCP-Multi-Godot Pipeline 🎮🤖

An automated, self-healing game generation engine structured as an explicit Directed Acyclic Graph (DAG) of Model Context Protocol (MCP) servers. Designed to transform raw game concepts into fully realized, text-compiled 2D pixel games inside the Godot 4 Engine.

---

## 🛠️ System Architecture

The pipeline decouples the LLM "brain" from local file execution, allowing highly complex orchestration to run seamlessly on restricted development hardware. By utilizing a **Single-Writer Rule** and **Git-backed automated checkpoints**, the framework ensures deterministic state evolution without file contention or compilation decay.

### The Pipeline Blueprint (DAG Layout)

```plaintext
MCP-Multi-Godot/
├── 01_Pre-Production MCP       # GDD generation & compiles master 'game_manifest.json'
├── 02_Godot Structure MCP      # Initializes file tree & creates baseline project.godot
├── 03_Addon Package MCP        # Downloads zip/git plugins strictly into res://addons/
├── 04_Project Preset MCP       # Configures engine settings & activates plugins in project.godot
├── 05_Static Data MCP          # Formats immutable item tables, dictionaries, & dialog strings
├── 06_Art MCP                  # Slices sprite sheets, textures, and asset files
├── 07_Animation MCP            # Generates SpriteFrames configurations & blend trees
├── 08_Prototype MCP            # Injects input maps, core kinematics, & player vectors
├── 09_Camera MCP               # Configures camera rigs & smoothing (Clamping deferred to Stage 12)
├── 10_World Building MCP       # Compiles grid layers, tilemaps, & bakes NavigationRegion2D
├── 11_Enemy AI MCP             # Injects enemy FSMs & binds to computed World NavMesh geometry
├── 12_Scene Composition MCP    # Instances entities, applies camera clamps, & places items/spawns
├── 13_VFX & Particle MCP       # Sets up hit-flashes, screen-shakes, & GPUParticles2D nodes
├── 14_UI MCP                   # Builds Control node layout & HUD scene tree (bindings deferred to Stage 16)
├── 15_Sound MCP                # Maps audio buses, environmental soundscapes, & sound triggers
├── 16_Progression MCP          # Injects runtime state models & wires signals into existing UI nodes
├── 17_Local Save MCP           # Sets up serialization/deserialization to user:// for persistence
├── 18_Polisher MCP             # Self-healing engine: reads bug reports & patches GDScript
├── 19_Playtester MCP           # Automated headless testing suite (validates node trees)
├── 20_Build & Deploy MCP       # Compiles binaries & automates deployment to Itch.io via Butler
│
├── game_manifest.json          # THE DATA CONTRACT: Single Source of Truth
├── mcp_router.py               # Central Orchestration Control Plane (DAG Coordinator)
├── .env.example                # Cloud API keys (Gemini/Groq) & local target paths
└── godot_project/              # Isolated, text-compiled Godot Engine workspace
```

> **Note on I/O Contracts:** Each subdirectory contains its own standalone `README.md` defining the exact subset of keys it consumes from `game_manifest.json` and the explicit file targets it has permission to write.

> **Note on Deferred Bindings:** `09_Camera MCP` and `14_UI MCP` intentionally build structure only (rig behavior and node layout, respectively) rather than binding to data that doesn't exist yet at their point in the DAG. Camera boundary clamps are applied once level geometry exists (`12_Scene Composition MCP`), and UI data bindings are wired once runtime state exists (`16_Progression MCP`). This keeps each server's write scope narrow without forcing an earlier, less natural position in the sequence.

---

## 🏗️ Core Engineering Guardrails

To distribute this pipeline reliably and scale it across limited hardware environments, `mcp_router.py` strictly enforces three systems programming principles:

### 1. The Single-Writer Rule (Mutual Exclusion)

To completely eliminate race conditions and file system conflicts, multiple MCP servers are never permitted to access or modify the same workspace asset concurrently.

* The orchestration layer locks execution down to a strict linear sequence.
* **Explicit Resource Handoff:** `03_Addon Package MCP` exclusively handles fetching and unpacking plugin assets into the `res://addons/` directory. It is explicitly banned from touching `project.godot`. Once completed, write permission is handed off to `04_Project Preset MCP`, which holds the exclusive lock required to modify the `[editor_plugins]` enablement block inside `project.godot`.

### 2. State-Based Checkpointing & Deterministic Rollbacks

Every node, scene (`.tscn`), and script (`.gd`) in Godot is fundamentally represented as plain text. The pipeline exploits this property by treating the workspace as a database tracked via local version control.

* Upon the successful conclusion of any given DAG stage, the router automatically executes a local checkpoint:
```bash
git add . && git commit -m "Pipeline Checkpoint: Stage [X] Verified"
```

* If a critical generation error occurs down-line (e.g., `14_UI MCP` corrupts a UI layout sequence), the `19_Playtester MCP` intercepts the scene compilation breakdown, registers a failure condition, and issues a deterministic rollback command:
```bash
git reset --hard HEAD
```

The pipeline safely drops back to the last known-good state before retrying or reporting.

### 3. The `game_manifest.json` Contract

All downstream generative execution acts as a pure, deterministic function of a single, immutable JSON contract: the `game_manifest.json`.

* Compiled dynamically in Stage 1, this file outlines arrays for entity types, static data tables, tile mapping constraints, and state transitions.
* Downstream servers cannot hallucinate structural variations; they parse explicit keys from the manifest (e.g., `manifest["enemy_types"]`) to construct state machines and variables.

---

## ⚡ Hardware & Environment Optimizations

The pipeline is intentionally architected to navigate tight local hardware boundaries (e.g., Dual-Core CPUs / 8GB RAM environments) with hyper-efficient resource management:

* **Decoupled Heavy Compute:** Local scripts execute text-parsing, asset orchestration, and directory management at near-zero CPU footprint. Heavy generative processing is offloaded over highly responsive, cloud-hosted API tiers (Gemini Flash / Groq) via integrated streaming context wrappers.
* **Sequential Integrity over Parallelism:** While stages like `13_VFX` and `15_Sound` modify separate files, execution is kept strictly sequential in this version to guarantee zero overhead, trivial debugging, and minimum memory footprint on resource-constrained host machines.
* **Headless Verification:** `19_Playtester MCP` runs automated unit testing suites utilizing Godot's native command-line parameters (`godot --headless --script test_suite.gd`). This processes node compliance and structural syntax checks entirely inside virtual memory, bypassing heavy graphic engine rendering cycles and avoiding system memory starvation.

---

## 🚀 Getting Started

### Prerequisites

* **Godot Engine 4.x** (Ensure the `godot` binary is added to your system `PATH`)
* **Python 3.10+**
* **Git**

### Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/Galyn26/Plug-and-Play.git
cd Plug-and-Play
```

2. **Configure Environment Variables:**
Copy the example environment file and add your cloud API credentials:
```bash
cp .env.example .env
```

Open `.env` and configure your keys:
```env
GEMINI_API_KEY=your_api_key_here
GODOT_BINARY_PATH=/Applications/Godot.app/Contents/MacOS/Godot
```

3. **Initialize the Control Plane:**
Run the router script to execute a baseline validation of the pipeline directories:
```bash
python3 mcp_router.py --validate
```

---

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
