# Scripts

This directory contains utility scripts for development, testing, and deployment.

## Available Scripts

### `build-all.sh`
Builds Docker images for all microservices.

```bash
./scripts/build-all.sh
```

### `deploy-local.sh`
Deploys all services locally using docker-compose.

```bash
./scripts/deploy-local.sh
```

### `test-all.sh`
Runs tests for all microservices with coverage reports.

```bash
./scripts/test-all.sh
```

### `create-pr.sh`
Creates a GitHub Pull Request from the current branch with proper formatting.

```bash
./scripts/create-pr.sh
```

**Features:**
- ✅ Validates GitHub CLI is installed and authenticated
- ✅ Automatically pushes branch if needed
- ✅ Extracts commit types from branch commits
- ✅ Generates descriptive PR title
- ✅ Uses PR template automatically
- ✅ Opens PR in browser

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated
- Current branch must not be `main`

**Example:**
```bash
# From feature branch
./scripts/create-pr.sh

# Output:
# Creating Pull Request...
# ✓ Branch pushed
# ✓ PR created: [feat, test] Feature Booking Service
# Opening in browser...
```

## Usage Notes

All scripts should be run from the repository root:

```bash
# ✅ Correct
./scripts/test-all.sh

# ❌ Incorrect
cd scripts && ./test-all.sh
```

## Prerequisites

- **Docker**: Required for build-all.sh and deploy-local.sh
- **Python 3.11+**: Required for test-all.sh
- **GitHub CLI (gh)**: Required for create-pr.sh

Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install --id GitHub.cli
```

Authenticate with GitHub:
```bash
gh auth login
```
