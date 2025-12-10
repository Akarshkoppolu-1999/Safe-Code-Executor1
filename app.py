import os
import subprocess
import tempfile
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
# Route for the Web UI
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
        
    if len(code) > 5000:
        return jsonify({"error": "Code exceeds 5000 character limit"}), 400
    # Create a temporary file to store the user's code
    # We use delete=False so we can mount it into Docker
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        # Prepare file paths for Docker
        # We mount the folder containing the temp file to /app in the container
        directory, filename = os.path.split(temp_path)
        
        # SECURE Docker command
        command = [
            "docker", "run", "--rm",
            "--network", "none",        # BLOCK Internet access
            "--memory", "128m",         # LIMIT Memory to 128MB
            "--cpus", "0.5",            # LIMIT CPU usage
            "-v", f"{directory}:/app",  # Mount host directory to /app
            "-w", "/app",               # Set working directory to /app
            "python:3.11-slim",         # Image to use
            "timeout", "5s",            # LIMIT Time to 5 seconds
            "python", filename          # Command to run inside container
        ]
        
        # Run the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10 # Safety timeout for the subprocess itself
        )
        
        output = result.stdout
        if result.stderr:
            output += "\nError:\n" + result.stderr
        # Check for timeout (Success in blocking infinite loop)
        if result.returncode == 124: # Timeout command exit code
            return jsonify({"error": "Execution timed out after 5 seconds"}), 408
            
        return jsonify({"output": output.strip()})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out after 5 seconds"}), 408
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500
    finally:
        # Cleanup: Remove the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
if __name__ == '__main__':
    app.run(debug=True, port=5000)