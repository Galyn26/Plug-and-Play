import sys
import os
import json

PROJECT_ROOT = "/Users/galyn/Plug-and-Play/core/workspace/godot_project"

def log_debug(message):
    # Since stdout is reserved for the MCP data stream, we log errors/debug info to stderr
    sys.stderr.write(f"[MCP LOG] {message}\n")
    sys.stderr.flush()

def list_godot_dir():
    try:
        files_list = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), PROJECT_ROOT)
                files_list.append({
                    "name": file,
                    "path": rel_path,
                    "size_bytes": os.path.getsize(os.path.join(root, file))
                })
        return {"status": "success", "files": files_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def serve():
    log_debug("Godot Filesystem MCP Server Started over stdio...")
    
    while True:
        try:
            # Read line from standard input
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            log_debug(f"Received request: {request.get('method')}")
            
            # Simple route handling for our tool
            if request.get("method") == "tools/list_files":
                response_data = list_godot_dir()
            else:
                response_data = {"status": "error", "message": "Method not found"}
            
            # Formulate standard MCP JSON-RPC response envelope
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id", 0),
                "result": response_data
            }
            
            # Stream the response directly back to the caller
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            log_debug("Received invalid JSON payload.")
        except Exception as e:
            log_debug(f"Runtime error: {str(e)}")

if __name__ == "__main__":
    serve()

