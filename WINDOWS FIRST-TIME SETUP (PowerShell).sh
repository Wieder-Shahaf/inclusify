############################################
# WINDOWS FIRST-TIME SETUP (PowerShell)
############################################

# 0) Install Git for Windows (run once)
# Download + install: https://git-scm.com/download/win
# Then reopen PowerShell.

# 1) Set Git identity (run once)
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
git config --global init.defaultBranch main

# 2) Create SSH key (press Enter for defaults)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 3) Enable + start ssh-agent service
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# 4) Add your SSH private key
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# 5) Copy public key (paste into GitHub → Settings → SSH and GPG keys → New SSH key)
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# 6) Test GitHub SSH auth
ssh -T git@github.com

# 7) Clone repo
git clone git@github.com:Wieder-Shahaf/inclusify.git
cd inclusify

# 8) Quick push test (optional)
git checkout -b feature/first-setup-test
"setup ok" | Out-File -Encoding utf8 setup_test.txt
git add setup_test.txt
git commit -m "chore: setup test"
git push -u origin feature/first-setup-test
############################################
