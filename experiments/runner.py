import urllib.request
import json
import time

BASE_URL = "http://localhost:5000/run"

def run_experiment(name, code, expected_behavior):
    print(f"Running Experiment: {name}")
    try:
        req = urllib.request.Request(
            BASE_URL, 
            data=json.dumps({"code": code}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Output: {result}")
            print(f"Expected: {expected_behavior}")
            print("-" * 30)
    except Exception as e:
        print(f"Experiment Error: {e}")

if __name__ == "__main__":
    # Experiment 1: Read sensitive file
    run_experiment(
        "Read /etc/passwd", 
        "with open('/etc/passwd') as f: print(f.read())",
        "Should show passwd file content (Docker default behavior) or fail if user restricted it."
    )

    # Experiment 2: Write to file
    run_experiment(
        "Write to /tmp/hacked.txt", 
        "with open('/tmp/hacked.txt', 'w') as f: f.write('hacked!')\nprint('Wrote file')",
        "Should succeed on default Docker, fail if --read-only is used (we haven't enabled read-only yet!)."
    )
