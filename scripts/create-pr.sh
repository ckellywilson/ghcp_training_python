#!/bin/bash
# Creates a GitHub Pull Request from the current branch to main
# Uses GitHub CLI (gh) with proper formatting and checks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Creating Pull Request...${NC}\n"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Determine default branch (try main, fall back to master)
if git rev-parse --verify origin/main &> /dev/null; then
    DEFAULT_BRANCH="main"
elif git rev-parse --verify origin/master &> /dev/null; then
    DEFAULT_BRANCH="master"
else
    echo -e "${RED}Error: Cannot determine default branch${NC}"
    exit 1
fi

if [ "$CURRENT_BRANCH" = "$DEFAULT_BRANCH" ]; then
    echo -e "${RED}Error: Cannot create PR from $DEFAULT_BRANCH branch${NC}"
    exit 1
fi

# Check if branch is pushed
if ! git rev-parse --verify "origin/$CURRENT_BRANCH" &> /dev/null; then
    echo -e "${YELLOW}Branch not pushed to remote. Pushing now...${NC}"
    git push -u origin "$CURRENT_BRANCH"
fi

# Check if PR already exists
if gh pr view "$CURRENT_BRANCH" &> /dev/null; then
    echo -e "${YELLOW}Pull request already exists for this branch${NC}"
    gh pr view "$CURRENT_BRANCH" --web
    exit 0
fi

# Extract commit types from branch commits
COMMIT_TYPES=$(git log --oneline origin/$DEFAULT_BRANCH..HEAD 2>/dev/null | grep -oE '^[a-f0-9]+ (feat|fix|docs|style|refactor|test|chore)' | cut -d' ' -f2 | sort -u | tr '\n' ', ' | sed 's/,$//' || echo "")

# Generate PR title from branch name
# Convert feature/my-feature-name to "My Feature Name"
PR_TITLE=$(echo "$CURRENT_BRANCH" | sed 's/[_-]/ /g' | sed 's/\b\(.\)/\u\1/g')

# Add commit types prefix if present
if [ -n "$COMMIT_TYPES" ]; then
    PR_TITLE="[$COMMIT_TYPES] $PR_TITLE"
fi

echo -e "${GREEN}Creating PR:${NC}"
echo -e "  Branch: ${YELLOW}$CURRENT_BRANCH${NC} -> ${YELLOW}$DEFAULT_BRANCH${NC}"
echo -e "  Title: ${YELLOW}$PR_TITLE${NC}"
echo ""

# Create PR with template
gh pr create \
    --base "$DEFAULT_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$PR_TITLE" \
    --fill \
    --web

echo ""
echo -e "${GREEN}✓ Pull request created successfully!${NC}"
