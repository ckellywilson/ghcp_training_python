# Git Commit Configuration Guide

This document explains how to configure Git to use the repository's commit message standards.

## Quick Setup

Run these commands in the repository root:

```bash
# Configure git hooks path to use repository hooks
git config core.hooksPath .githooks

# Configure commit message template
git config commit.template .gitmessage
```

## What This Does

### 1. Git Hooks (`.githooks/commit-msg`)

The commit-msg hook validates your commit messages before they're accepted:

- ✅ Ensures Conventional Commits format: `type(scope): subject`
- ✅ Validates commit types: feat, fix, docs, style, refactor, test, chore
- ✅ Warns if subject line exceeds 72 characters
- ✅ Skips validation for merge commits

**Example validation error:**

```
❌ ERROR: Commit message doesn't follow Conventional Commits format

Expected format:
  <type>(<scope>): <subject>

Example:
  feat(airline-service): add flight booking endpoint
  fix(domain): ensure airline entity immutability

Valid types: feat, fix, docs, style, refactor, test, chore
```

### 2. Commit Template (`.gitmessage`)

When you run `git commit` (without `-m`), your editor opens with a helpful template:

```
# <type>(<scope>): <subject>
# |<----  Using a Maximum Of 72 Characters  ---->|

# Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# Provide links or keys to any relevant tickets, articles or other resources
# Example: Closes #123

# --- COMMIT END ---
# Type can be:
#    feat     (new feature)
#    fix      (bug fix)
#    ...
```

## Usage

### With GitHub Copilot (Recommended)

In VS Code:
1. Stage your changes
2. Click the sparkle icon (✨) in the Source Control commit message box
3. Copilot generates a properly formatted commit message
4. Review and commit

### Manual Commits

```bash
# With template (opens editor)
git commit

# Inline commit
git commit -m "feat(airline-service): add booking validation"
```

## Creating Pull Requests

### Using the Helper Script (Recommended)

The repository includes a script for easy PR creation:

```bash
# From any branch (except main)
./scripts/create-pr.sh
```

**What it does:**
- Checks if GitHub CLI (`gh`) is installed and authenticated
- Pushes your branch if not already pushed
- Extracts commit types from your commits (feat, fix, etc.)
- Generates a descriptive PR title from branch name and commit types
- Uses the PR template automatically
- Opens the PR in your browser for final review

**Example output:**
```
Creating Pull Request...

✓ Authenticated with GitHub
✓ Pushing branch feature/booking-service...

Creating PR:
  Branch: feature/booking-service -> main
  Title: [feat, test] Feature Booking Service

✓ Pull request created successfully!
Opening in browser...
```

### Using GitHub CLI Directly

```bash
# Push your branch
git push -u origin your-branch-name

# Create PR interactively
gh pr create --base main --fill --web

# Or with explicit title and body
gh pr create \
  --base main \
  --title "feat(booking): add booking service" \
  --body "Adds new booking microservice following Clean Architecture" \
  --web
```

### GitHub CLI Prerequisites

Install GitHub CLI if not already available:

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Windows
winget install --id GitHub.cli
```

Authenticate:

```bash
gh auth login
```

## Examples

### Good Commit Messages

```bash
feat(airline-service): add flight search endpoint
fix(domain): ensure Flight entity immutability
test(use-cases): add booking cancellation tests
docs(readme): update GitHub Copilot setup instructions
refactor(infrastructure): extract database connection logic
chore(deps): update FastAPI to version 0.110.0
style(api): format routes with black
```

### Bad Commit Messages

```bash
# ❌ Missing type
airline-service: add booking

# ❌ Wrong format
Added booking feature

# ❌ Too vague
fix bug

# ❌ Subject too long (>72 chars)
feat(airline-service): add a new endpoint that allows users to search for flights with various filters

# ❌ Wrong mood (not imperative)
Added new booking feature
```

## Bypassing the Hook

In rare cases where you need to bypass validation (not recommended):

```bash
git commit --no-verify -m "your message"
```

## Troubleshooting

### Hook Not Running

```bash
# Verify hooks path is configured
git config core.hooksPath
# Should output: .githooks

# Verify hook is executable
ls -la .githooks/commit-msg
# Should show: -rwxr-xr-x

# Make it executable if needed
chmod +x .githooks/commit-msg
```

### Template Not Loading

```bash
# Verify template is configured
git config commit.template
# Should output: .gitmessage

# Reconfigure if needed
git config commit.template .gitmessage
```

## Per-User vs Repository Configuration

The commands above configure settings for this repository only. To configure globally:

```bash
# Global hook path (not recommended - conflicts with other repos)
git config --global core.hooksPath ~/.githooks

# Global commit template
git config --global commit.template ~/.gitmessage
```

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Writing Good Commit Messages](https://cbea.ms/git-commit/)
