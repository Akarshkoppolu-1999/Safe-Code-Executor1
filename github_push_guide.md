# How to Push to GitHub 🐙

Follow these steps to upload your "Safe Code Executor" project to GitHub.

## Step 1: Create a Repository on GitHub
1.  Log in to [GitHub.com](https://github.com).
2.  Click the **+** icon in the top right and select **New repository**.
3.  **Repository name**: `safe-code-executor` (or any name you like).
4.  **Description**: "A secure Python code execution API using Docker."
5.  **Public/Private**: Choose Public (if you want to share it) or Private.
6.  **Initialize this repository with**: DO NOT check any boxes (Readme, .gitignore, License). We want an empty repo.
7.  Click **Create repository**.
8.  Copy the HTTPS URL provided (e.g., `https://github.com/your-username/safe-code-executor.git`).

## Step 2: Prepare Your Local Project
Open your terminal (VS Code Terminal) inside your project folder (`c:\Users\lenovo\Desktop\Devops learning project2`).

### 1. Create a `.gitignore` file
We don't want to upload unnecessary files like temporary caches or the virtual environment.

Run this command to create it:
```powershell
New-Item -Path .gitignore -ItemType File -Value "
__pycache__/
*.pyc
.env
venv/
.DS_Store
verification_result.txt
experiments/__pycache__
tests/__pycache__
"
```

### 2. Initialize Git
Run these commands one by one:

```bash
# Initialize a new git repo
git init

# Add all files to staging
git add .

# Commit the files
git commit -m "Initial commit: Safe Code Executor with Docker security"
```

## Step 3: Link and Push

Replace `<YOUR_REPO_URL>` with the URL you copied in Step 1.

```bash
# Rename the default branch to main
git branch -M main

# Add the remote repository
git remote add origin <YOUR_REPO_URL>

# Push your code
git push -u origin main
```

**Note**: If it asks for a username/password:
-   **Username**: Your GitHub username.
-   **Password**: This is likely your **Personal Access Token** (not your login password), or use the browser authentication pop-up if prompted.

## Step 4: Verify
Refresh your GitHub repository page. You should see all your files (`app.py`, `README.md`, etc.) listed there!
