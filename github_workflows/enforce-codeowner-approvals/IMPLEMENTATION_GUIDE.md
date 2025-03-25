# Implementation Guide: Enforce Code Owner Approvals

This guide explains how to implement and integrate the "Enforce Code Owner Approvals" CI step into your GitHub workflow to ensure that pull requests have been approved by all required code owners before allowing a merge.

## Overview

The CI step performs the following tasks:

1. **Parse the CODEOWNERS file** to extract the relevant code owners for the specific files changed in the pull request
2. **Retrieve pull request reviews** using the GitHub API
3. **Verify approvals against code owners** to ensure that each required code owner has approved the pull request

## Implementation Options

There are two ways to implement this CI step in your repository:

### Option 1: Use the Reusable Workflow (Recommended)

This approach uses GitHub Actions' reusable workflows feature to call the shared workflow.

1. Create a file in your repository at `.github/workflows/pr-checks.yml`:

```yaml
name: Pull Request Checks

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  pull_request_review:
    types: [submitted]

jobs:
  check-code-owner-approvals:
    uses: organization/shared-ci-steps/.github/workflows/enforce-codeowner-approvals.yml@v1.0.0
    with:
      codeowners_path: ".github/CODEOWNERS"  # Optional, default is .github/CODEOWNERS
      require_all_owners: true              # Optional, default is true
```

### Option 2: Use the GitHub Action

This approach uses the custom action defined in the `action.yml` file.

1. Create a file in your repository at `.github/workflows/pr-checks.yml`:

```yaml
name: Pull Request Checks

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  pull_request_review:
    types: [submitted]

jobs:
  check-approvals:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check code owner approvals
        uses: organization/shared-ci-steps/enforce-codeowner-approvals@v1.0.0
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          codeowners-path: '.github/CODEOWNERS'
          comment-on-pr: 'true'
```

## Configuration Options

### Workflow Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `codeowners_path` | No | `.github/CODEOWNERS` | Path to the CODEOWNERS file |
| `require_all_owners` | No | `true` | If true, requires approval from all code owners |

### Action Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `codeowners-path` | No | `.github/CODEOWNERS` | Path to the CODEOWNERS file |
| `require-all-owners` | No | `true` | If true, requires approval from all code owners |
| `repo-token` | Yes | `${{ github.token }}` | GitHub token to access the repository |
| `comment-on-pr` | No | `false` | Add a comment to the PR with the approval status |

## CODEOWNERS File Format

The `CODEOWNERS` file follows GitHub's syntax for assigning owners to specific files or patterns:

```
# This is a comment
* @default-team                          # Default owners for everything
/src/frontend/ @frontend-team            # Owners for specific directories
*.js @javascript-developers              # Owners for specific file types
/src/security/ @security-team @lead-dev  # Multiple owners for a path
```

## Implementation Details

### Python Script

The core of this CI step is a Python script that:

1. Parses the CODEOWNERS file to extract ownership rules
2. Retrieves the list of files modified in the pull request
3. Determines which code owners need to approve based on the modified files
4. Fetches the current review statuses from the pull request
5. Verifies if all required approvals have been obtained

The script uses Python's `requests` library to interact with the GitHub API and regular expressions to handle the pattern matching in CODEOWNERS rules.

## Customization

### Adding Custom Logic

If you need to add custom logic, such as team membership verification or specific approval rules, you can modify the Python implementation (`check_codeowner_approvals.py`) and update the workflow or action accordingly.

### Blocking Merges

To block merges when required code owners haven't approved, you can use branch protection rules in GitHub:

1. Go to your repository settings
2. Navigate to Branches > Branch protection rules
3. Add a rule for your main branch
4. Enable "Require status checks to pass before merging"
5. Add your code owner approval check as a required status check

## Troubleshooting

### Common Issues

1. **Missing CODEOWNERS file**: Ensure the CODEOWNERS file exists at the specified path
2. **Invalid patterns**: Check that patterns in the CODEOWNERS file follow the correct syntax
3. **Permission issues**: Make sure the GitHub token has sufficient permissions to read pull request data
4. **Python environment**: Ensure Python 3.6+ is available in your environment

### Debugging

To debug issues with the CI step, you can:

1. Set the log level to debug in your workflow
2. Examine the full output of the Python script
3. Test the script locally with sample inputs

## Example: Complete Workflow

Here's a complete example of a workflow that integrates the code owner approval check with other common CI checks:

```yaml
name: Pull Request Checks

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  pull_request_review:
    types: [submitted]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: |  
          # Your linting commands here

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          # Your test commands here

  check-code-owner-approvals:
    uses: organization/shared-ci-steps/.github/workflows/enforce-codeowner-approvals.yml@v1.0.0
    with:
      codeowners_path: ".github/CODEOWNERS"

  ready-to-merge:
    needs: [lint, test, check-code-owner-approvals]
    runs-on: ubuntu-latest
    steps:
      - name: Ready to merge
        run: echo "All checks passed, PR is ready to merge!"
```

This workflow runs linting and testing in parallel with the code owner approval check, and only proceeds to the "ready-to-merge" job if all of them pass.
