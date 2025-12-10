import urllib.request
import urllib.error
import json
import time
import os

BASE_URL = "http://localhost:5000/run"
TEST_DIR = "tests"

def log(msg):
    print(msg)
    with open("verification_result.txt", "a") as f:
        f.write(msg + "\n")

def run_test(filename, name):
    log(f"Testing {name} ({filename})...")
    filepath = os.path.join(TEST_DIR, filename)
    if not os.path.exists(filepath):
        log(f"FAILED: {filename} not found")
        return

    with open(filepath, "r") as f:
        code = f.read()

    try:
        start_time = time.time()
        req = urllib.request.Request(
            BASE_URL, 
            data=json.dumps({"code": code}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                output = result.get("output", "")
                duration = time.time() - start_time
                log(f"Response (Time: {duration:.2f}s):")
                log(f"--- OUTPUT START ---")
                log(output)
                log(f"--- OUTPUT END ---")
        except urllib.error.HTTPError as e:
            log(f"Error Status Code: {e.code}")
            log(e.read().decode('utf-8'))
            
    except Exception as e:
        log(f"Test Execution Failed: {e}")
    log("-" * 30)

def main():
    if os.path.exists("verification_result.txt"):
        os.remove("verification_result.txt")
    
    log("Waiting for server...")
    time.sleep(2)
    
    run_test("infinite_loop.py", "Infinite Loop")
    run_test("memory_hog.py", "Memory Hog")
    run_test("network_attack.py", "Network Attack")

if __name__ == "__main__":
    main()
