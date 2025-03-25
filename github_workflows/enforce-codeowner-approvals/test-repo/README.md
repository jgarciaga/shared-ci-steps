# Test Repository

This repository is set up to test GitHub Actions workflows, particularly the code owner approval check.

## Structure

- `.github/CODEOWNERS` - Defines ownership rules for code review
- `.github/workflows/` - Contains GitHub Actions workflow definitions
- `src/frontend/` - Frontend code (owned by @frontend-developer)
- `src/backend/` - Backend code (owned by @backend-developer)

## Testing Code Owner Approvals

When a pull request is created, the GitHub Actions workflow will automatically check if all required code owners have approved the changes based on the files modified in the PR.
