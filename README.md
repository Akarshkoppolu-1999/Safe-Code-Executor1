# Safe Code Executor

A secure, isolated Python code execution engine built with Flask and Docker. This API allows users to submit Python scripts which are then executed in sandboxed Docker containers with strict resource limits to prevent malicious activity.

## Features

*   **Sandboxed Execution**: Runs code inside isolated Docker containers.
*   **Resource Limits**:
    *   Memory: Limited to 128MB.
    *   CPU: Limited to 0.5 cores.
*   **Network Isolation**: Blocked internet access (`--network none`) to prevent external attacks.
*   **Timeouts**: Automatic 5-second timeout to stop infinite loops.
*   **Input Validation**: Strict code length limits (max 5000 chars).
*   **Web UI**: Simple interface to test code execution directly in the browser.

## Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Must be running)
*   [Python 3.10+](https://www.python.org/)

## Installation

1.  **Clone the repository** (or download files):
    ```bash
    git clone <your-repo-url>
    cd safe-code-executor
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Pull the Docker Image**:
    This uses the lightweight `python:3.11-slim` image.
    ```bash
    docker pull python:3.11-slim
    ```

## Usage

### 1. Start the Server
```bash
python app.py
```
The server will start at `http://localhost:5000`.

### 2. Using the Web UI
Open your browser and visit `http://localhost:5000`. You can type Python code and click "Run".

### 3. Using the API (via Postman or Curl)

**Endpoint**: `POST /run`

**Example Request:**
```json
{
    "code": "print(2 + 2)"
}
```

**Example Response:**
```json
{
    "output": "4"
}
```

##  Security Measures

This project defends against common attacks:

*   **Infinite Loops**: `while True: pass` -> Terminated after 5s.
*   **Fork Bombs**: Restricted by container PIDs and resource limits.
*   **Malware Downloading**: Blocked by network isolation.
*   **Filesystem Attacks**: Container is ephemeral (`--rm`) and does not mount sensitive host directories (only the temp code file).

##  Project Structure

*   `app.py`: Main Flask application handling API requests and Docker subprocesses.
*   `templates/`: HTML files for the Web UI.
*   `experiments/`: Scripts demonstrating security vulnerability tests.
*   `tests/`: Malicious scripts used for verification (infinite loops, etc).
*   `project_documentation.md`: Detailed project docs and learnings.

## License
This is a learning project created for DevOps training.
