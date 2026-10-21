# Publish this portfolio safely to GitHub

## Before you begin

This repository includes only synthetic datasets, demo code and a sanitized case study. **Do not append your actual OPNsense files, credentials, `.env`, collector databases, original private Word report, screenshots or host inventory.**

## Recommended process: create private first, review, then make public

1. Download and extract the `jt-ai-security-ops-lab-github-ready.zip` archive on your own computer. Verify the folder contains `README.md`, `src/`, `fixtures/`, `configs/`, `tests/`, `.github/` and `docs/`.
2. On GitHub, create an **empty private** repository named `jt-ai-security-ops-lab`. Do not initialize with a README, license or `.gitignore`; those are already included here.
3. In the extracted folder, run the local safety checks:

   ```bash
   PYTHONPATH=src python -m unittest discover -s tests -v
   python scripts/check_public_safety.py
   ```

4. Initialize and commit locally:

   ```bash
   git init
   git branch -M main
   git add .
   git diff --cached --stat
   git diff --cached
   git commit -m "Add sanitized AI security operations portfolio demo"
   ```

5. Configure a remote, replacing `YOUR-GITHUB-USERNAME` with your actual account username:

   ```bash
   git remote add origin https://github.com/YOUR-GITHUB-USERNAME/jt-ai-security-ops-lab.git
   git push -u origin main
   ```

6. Review the rendered README, example files, Actions run, **all committed files and full commit history** on GitHub. Enable available secret scanning features. Consider additional independent scanning with `gitleaks` before making public.
7. Only after review, change GitHub **Settings → General → Danger Zone → Change repository visibility → Public**.

### Windows PowerShell

From the extracted repository root:

```powershell
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
python scripts/check_public_safety.py
```

Then run the same `git` commands above in PowerShell (Git for Windows required).

### Browser-only alternative

Create a private repository with a README first, open its **Add file → Upload files** page and drag the **extracted individual files/folders** into the upload area. GitHub does not automatically unpack the contents of an uploaded ZIP into repository files. Ensure hidden `.github`, `.gitignore` and `.env.example` paths are included. The Git command-line method is more reliable for preserving all subdirectories.

## Suggested repository description

> Self-hosted AI cybersecurity lab: OPNsense + Python + Ollama/Qwen + Linux monitoring, evidence-grounded tool calling, safe automation, and synthetic reproducible demos.

## Suggested GitHub topics

`cybersecurity`, `homelab`, `ai-agents`, `opnsense`, `ollama`, `qwen`, `python`, `security-automation`, `network-security`, `devsecops`

## LinkedIn / resume link

Add the eventual repository URL under a Projects section on your resume and LinkedIn. Refer to `docs/CAREER_PRESENTATION.md` for accurate project descriptions without exaggerating deployed capabilities.
