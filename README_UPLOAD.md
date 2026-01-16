# How to Upload Your Project to GitHub

Since this is a shared repository with your teacher, follow these steps to upload your work to the correct folder.

## Step 1: Install Git (Required)
You currently do not have Git installed (or it's not in your PATH).
1.  Download Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)
2.  Install it (click "Next" through the default options).
3.  **Restart your computer** or close and reopen your terminal/VS Code.

## Step 2: Run these commands
Once Git is installed, open your terminal in this project folder (`s:\PYTHON PROGRAM\Platforma invitatii de nunta`) and run the following commands one by one:

### 1. Configure your user (if you haven't already)
```bash
git config --global user.name "stcreativecoding25"
git config --global user.email "tudoraseby@gmail.com"
```

### 2. Clone the Teacher's Repository
We will clone it into a temporary folder to avoid messing up your current workspace.
```bash
# Go to the parent directory or a temp location
cd "S:\PYTHON PROGRAM\Platforma invitatii de nunta\Practica-AI---Python-2025-2026\Teme\01\09.Sebastian_Tudora"

git clone https://github.com/sojog/Practica-AI---Python-2025-2026.git temp_upload_folder
```
git commit -m "Proiect Django - Platforma invitatii de nunta (Sebastian Tudora)"

### 3. Copy Your Files
Now, copy your project files into the correct folder structure.
```bash
# Create the specific folder for your name
mkdir "temp_upload_folder/Teme/01/09.Sebastian_Tudora"

# Copy your project files (Manual Step is safest)
# Copy everything from "Platforma invitatii de nunta" 
# INTO "temp_upload_folder/Teme/01/09.Sebastian_Tudora"
```
*Note: Do not copy the `venv` folder or `__pycache__` folders.*

### 4. Push to GitHub
```bash
# Go into the cloned folder
cd temp_upload_folder

# Add changes
git add .

# Commit
git commit -m "Tema 09: Platforma Invitatii Nunta - Sebastian Tudora"

# Push
git push origin main
```

## Troubleshooting
-   **Permission Denied**: If you get an error about permissions, you might need to be added as a "Collaborator" to the repository by your teacher, or you might need to "Fork" the repository first.
-   **Login**: When you `git push`, it will ask for your GitHub username and password. For the password, you must use a **Personal Access Token** (Classic), not your actual account password.
