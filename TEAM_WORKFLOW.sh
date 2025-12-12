############################################
# TEAM GIT WORKFLOW (READ & FOLLOW)
############################################

# ❗ RULE:
# NEVER work directly on main
# ALWAYS use: branch -> PR -> merge

############################################
# 1) START A NEW TASK
############################################

# Make sure you are up to date
git checkout main
git pull

# Create a new branch for your task
# Replace <topic> with what you are working on
git checkout -b feature/<topic>

# Examples:
# git checkout -b feature/backend-api
# git checkout -b feature/frontend-layout
# git checkout -b fix/login-bug


############################################
# 2) WORK ON CODE
############################################

# Edit files, write code, add files
# When a small logical change is done:


############################################
# 3) COMMIT YOUR WORK
############################################

git add .
git commit -m "feat: short description of what you did"

# Examples:
# git commit -m "feat: add text upload endpoint"
# git commit -m "fix: handle empty input"
# git commit -m "chore: add backend README"


############################################
# 4) PUSH YOUR BRANCH TO GITHUB
############################################

git push -u origin feature/<topic>

# (-u is only needed the first time)


############################################
# 5) OPEN A PULL REQUEST (PR)
############################################

# Go to GitHub:
# Pull Requests -> New Pull Request
# Base: main
# Compare: feature/<topic>
# Create PR


############################################
# 6) WAIT BEFORE MERGING
############################################

# DO NOT MERGE UNTIL:
# - CI checks are green
# - At least 1 teammate approved

# When approved:
# - Use "Squash and merge"
# - Delete the branch after merge


############################################
# 🚫 NEVER COMMIT THESE
############################################

# - .env files
# - API keys or tokens
# - User texts / private datasets
# - Model weights (unless approved)


############################################
# ONE-LINE SUMMARY
############################################

# Branch -> Commit -> Push -> PR -> Review -> Merge
