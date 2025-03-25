# Enforce Code Owner Approvals

## Overview

This CI step ensures that pull requests have been approved by all the required code owners as defined in the CODEOWNERS file before allowing a merge. This helps maintain code quality and ensures that changes are reviewed by the appropriate team members with domain expertise.

## Functionality

The workflow accomplishes the following:

1. **Parse CODEOWNERS File**: Extracts the relevant code owners for the specific files or directories that have been modified in the pull request.

2. **Retrieve Pull Request Reviews**: Uses the GitHub API to fetch the list of reviews associated with the pull request to identify who has reviewed and their approval status.

3. **Verify Approvals Against Code Owners**: Compares the list of approvers from the pull request reviews against the code owners to ensure that each required code owner has approved the pull request.

## Implementation

This CI step is implemented as a GitHub Actions workflow using Python that runs on pull request events and enforces that all necessary approvals are obtained before allowing a merge.

## Usage

To use this CI step in your repository, copy the workflow file to your `.github/workflows/` directory:

```yaml
# .github/workflows/enforce-codeowner-approvals.yml
name: Enforce Code Owner Approvals

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  pull_request_review:
    types: [submitted]

jobs:
  enforce-codeowner-approvals:
    uses: organization/shared-ci-steps/.github/workflows/enforce-codeowner-approvals.yml@v1.0.0
```

## Requirements

- A valid `CODEOWNERS` file in the repository (typically located at `.github/CODEOWNERS`)
- GitHub repository with pull request reviews enabled
- Appropriate GitHub token with permissions to read pull request data
- Python 3.6+ with the `requests` library

## Parameters

The workflow accepts the following parameters:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `codeowners_path` | No | `.github/CODEOWNERS` | Path to the CODEOWNERS file |
| `require_all_owners` | No | `true` | If true, requires approval from all code owners |

## Error Handling

The workflow handles the following error cases:

- Missing CODEOWNERS file
- Malformed CODEOWNERS file
- GitHub API request failures
- Invalid pattern matching in CODEOWNERS file

## Customization

You can customize the workflow by creating your own version with additional steps or modified logic. Common customizations include:

- Adding notifications for missing approvals
- Implementing team membership verification
- Adding exceptions for specific files or patterns
