############################################
# MAC FIRST-TIME SETUP (Terminal)
############################################

# 0) Install Git tools (run once)
xcode-select --install

# 1) Set Git identity (run once)
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
git config --global init.defaultBranch main

# 2) Create SSH key (press Enter for defaults)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 3) Start ssh-agent + add key (macOS)
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# 4) Copy public key (paste into GitHub → Settings → SSH and GPG keys → New SSH key)
pbcopy < ~/.ssh/id_ed25519.pub

# 5) Test GitHub SSH auth
ssh -T git@github.com

# 6) Clone repo
git clone git@github.com:Wieder-Shahaf/inclusify.git
cd inclusify

# 7) Quick push test (optional)
git checkout -b feature/first-setup-test
echo "setup ok" > setup_test.txt
git add setup_test.txt
git commit -m "chore: setup test"
git push -u origin feature/first-setup-test
############################################
