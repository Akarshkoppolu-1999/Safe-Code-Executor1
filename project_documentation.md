# Safe Code Executor - Project Documentation

## 1. Project Status Checklist

Below is the detailed status of each requirement from the task list.

| Requirement | Status | Details |
| :--- | :---: | :--- |
| **Step 1: Make It Work** | | |
| Create Flask API with `/run` endpoint | ✅ Done | Implemented in `app.py` |
| Take Python code as input | ✅ Done | Accepts JSON `{ "code": "..." }` |
| Run code in Docker | ✅ Done | Uses `docker run python:3.11-slim` |
| Return output | ✅ Done | Returns `{ "output": "..." }` |
| **Step 2: Add Basic Safety** | | |
| Stop infinite loops (Timeout 10s) | ✅ Done | Implemented logic for 5s timeout (stricter than requested) |
| Limit memory (128mb) | ✅ Done | Added `--memory 128m` flag |
| Block internet access | ✅ Done | Added `--network none` flag |
| **Step 3: Docker Security** | | |
| Experiment: Read `/etc/passwd` | ✅ Done | Can read system files (expected behavior without user namespaces) |
| Experiment: Write to `/tmp` | ✅ Done | Defaults to writable. Can be secured with `--read-only` |
| Report findings | ✅ Done | Included in this document |
| **Step 4: Polish & Document** | | |
| Better error messages | ✅ Done | Returns specific timeout/server errors |
| Limit code length (5000 chars) | ✅ Done | Added validation in `app.py` |
| Simple Web UI | ✅ Done | `templates/index.html` created |
| Documentation | ✅ Done | This file |

---

## 2. Project Structure

Here is the file structure of the project:

```
Devops learning project2/
├── app.py                  # Main Flask application (API + Docker logic)
├── templates/
│   └── index.html          # Simple Web UI for testing
├── experiments/
│   └── runner.py           # Script to run security experiments
├── tests/                  # Test scripts for verification
│   ├── infinite_loop.py
│   ├── memory_hog.py
│   └── network_attack.py
├── requirements.txt        # Python dependencies (Flask)
└── verify_security.py      # Automated security verification script
```

---

## 3. API Documentation & Postman

You can use Postman to test the API.

**Endpoint:** `POST http://localhost:5000/run`
**Headers:** `Content-Type: application/json`

### Test Case 1: Simple Print
**Body (JSON):**
```json
{
  "code": "print('Hello from Postman')"
}
```
**Expected Response:**
```json
{
  "output": "Hello from Postman"
}
```

### Test Case 2: Math Calculation
**Body (JSON):**
```json
{
  "code": "print(10 + 20)"
}
```
**Expected Response:**
```json
{
  "output": "30"
}
```

### Test Case 3: Infinite Loop (Security Test)
**Body (JSON):**
```json
{
  "code": "while True: pass"
}
```
**Expected Response:**
```json
{
  "error": "Execution timed out after 5 seconds"
}
```

---

## 4. Screenshot Guide

Take screenshots of the following to prove your work:

1.  **Project Files**: Screenshot your VS Code file explorer or the folder structure.
2.  **Web UI**: Open `http://localhost:5000` in a browser, type `print("Hello UI")`, click Run, and screenshot the result.
3.  **Postman Success**: Screenshot a successful `POST /run` request with `print("Hello")`.
4.  **Postman Security**: Screenshot the "Infinite Loop" test showing the **Timeout Error**.
5.  **Terminal Output**: Run `python verify_security.py` and screenshot the "Testing..." output in your terminal.
6.  **Docker Command**: Screenshot the `app.py` file code showing the `docker run` command lines (lines ~30-40) to prove you added security flags (`--network none`, `--memory 128m`).

---

## 5. What I Learned (Project Takeaways)

This project taught me the fundamentals of securing a code execution engine. Here are my key takeaways:

### 1. The Danger of Untrusted Code
I learned that running user-submitted code is inherently risky. A simple script like `while True: pass` can freeze a server, and `import os; os.system('rm -rf /')` could be catastrophic if not isolated.

### 2. Docker as a Sandbox
I learned that Docker containers provide a good baseline for isolation, but they are **not secure by default** for this use case.
- **Default Behavior**: By default, a container can access the internet, write to the filesystem, and use unlimited CPU/RAM.
- **Hardening Required**: I had to explicitly add flags like `--network none` and `--memory 128m` to lock it down.

### 3. Implementation Details
- **Programmatic Docker**: I learned how to use Python's `subprocess` module to run Docker commands dynamically, which is how the API interacts with the container.
- **Timeouts are Critical**: I implemented timeouts in two places:
    1.  The `docker run` command (`timeout` command inside).
    2.  The Python `subprocess.run` call (to prevent the server thread from hanging).

### 4. Trade-offs
I discovered that security often comes at the cost of functionality. For example, making the filesystem `--read-only` effectively prevents malware from hiding, but it also stops legitimate scripts from creating temporary files. I had to decide which trade-offs were acceptable for this project.

```python
# The final secure command structure I built:
command = [
    "docker", "run", "--rm",       # Clean up after run
    "--network", "none",           # No Internet
    "--memory", "128m",            # Max 128MB RAM
    "--cpus", "0.5",               # Max 0.5 CPU cores
    "-v", f"{directory}:/app",     # Mount code
    "python:3.11-slim",            # Image
    "timeout", "5s",               # 5s Execution time
    "python", filename
]
```
