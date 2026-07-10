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
├── 03_Addon Package MCP        # Downloads zip/git plugins (e.g. Dialogic) into res://addons/
├── 04_Project Preset MCP       # Injects global engine presets & export template profiles
├── 05_Art MCP                  # Slices sprite sheets, textures, and asset files
├── 06_Animation MCP            # Generates SpriteFrames configurations & blend trees
├── 07_Static Data MCP          # Formats immutable item tables, dictionaries, & dialog strings
├── 08_Prototype MCP            # Injects input maps, core kinematics, & player vectors
├── 09_Camera MCP               # Configures camera rigs, follow smoothing, & camera framing
├── 10_Enemy AI MCP             # Injects enemy state machines, navigation, & pathfinding
├── 11_World Building MCP       # Compiles grid layers, tilemaps, & physical terrain matrices
├── 12_Scene Composition MCP    # Populates worlds with doors, triggers, items, & enemy spawns
├── 13_VFX & Particle MCP       # Sets up hit-flashes, screen-shakes, & GPUParticles2D nodes
├── 14_UI MCP                   # Builds Control node interfaces, main menu, & HUD scenes
├── 15_Sound MCP                # Maps audio buses, environmental soundscapes, & sound triggers
├── 16_Local Save MCP           # Sets up serialization/deserialization to user:// for progress
├── 17_Polisher MCP             # Self-healing engine: reads bug reports & patches GDScript
├── 18_Playtester MCP           # Automated headless testing suite (validates node trees)
├── 19_Build & Deploy MCP       # Compiles binaries & automates deployment to Itch.io via Butler
│
├── game_manifest.json          # THE DATA CONTRACT: Single Source of Truth
├── mcp_router.py               # Central Orchestration Control Plane (DAG Coordinator)
├── .env.example                # Cloud API keys (Gemini/Groq) & local target paths
└── godot_project/              # Isolated, text-compiled Godot Engine workspace

```

---

## 🏗️ Core Engineering Guardrails

To distribute this pipeline reliably and scale it across limited hardware environments, `mcp_router.py` strictly enforces three systems programming principles:

### 1. The Single-Writer Rule (Mutual Exclusion)

To completely eliminate race conditions and file system conflicts, multiple MCP servers are never permitted to access or modify the same workspace asset concurrently.

* The orchestration layer locks execution down to a strict linear step sequence.
* For instance, `02_Godot Structure MCP` exclusively owns the filesystem initialization; once finalized, its write-lock passes cleanly down the DAG to `04_Project Preset MCP` to configure parameters.

### 2. State-Based Checkpointing & Deterministic Rollbacks

Every node, scene (`.tscn`), and script (`.gd`) in Godot is fundamentally represented as plain text. The pipeline exploits this property by treating the workspace as a database tracked via local version control.

* Upon the successful conclusion of any given DAG stage, the router automatically executes a local checkpoint:
```bash
git add . && git commit -m "Pipeline Checkpoint: Stage [X] Verified"

```


* If a critical generation error occurs down-line (e.g., `14_UI MCP` corrupts a UI layout sequence), the `18_Playtester MCP` intercepts the scene compilation breakdown, registers a failure condition, and issues a deterministic rollback command:
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
* **Headless Verification:** `18_Playtester MCP` runs automated unit testing suites utilizing Godot's native command-line parameters (`godot --headless --script test_suite.gd`). This processes node compliance and structural syntax checks entirely inside virtual memory, bypassing heavy graphic engine rendering cycles and avoiding system memory starvation.

```
