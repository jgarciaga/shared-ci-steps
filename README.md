# Shared CI Steps

This repository contains reusable GitHub Actions workflows and steps for CI/CD pipelines.

## Automatic Version Bumping

This repository includes a GitHub Action workflow that automatically bumps the version number based on labels applied to pull requests and creates GitHub releases.

### How It Works

The workflow performs the following steps:

1. Detects when a pull request is opened or labeled against the main branch
2. Determines the type of version bump based on PR labels (major, minor, patch)
3. Identifies the versioning system used in your project (package.json, pyproject.toml, or a VERSION file)
4. Extracts the current version number
5. Increments the version according to the label:
   - `major` label: x.y.z → (x+1).0.0
   - `minor` label: x.y.z → x.(y+1).0
   - `patch` label: x.y.z → x.y.(z+1)
6. Updates the version in the appropriate file
7. Commits and pushes the change to the PR branch
8. Adds a comment to the PR with the version change details
9. Creates a GitHub release with the new version number

### Setup Instructions

#### 1. Add the Workflow File

The workflow file is already included in this repository at `.github/workflows/auto-version-bump.yml`.

#### 2. Configure Version File (Optional)

The workflow automatically detects and supports three common version file formats:

- **package.json** - For JavaScript/Node.js projects
- **pyproject.toml** - For Python projects
- **VERSION** - A simple text file containing just the version number

If none of these files exist, the workflow will create a `VERSION` file with an initial version of `0.1.0`.

#### 3. Set Up PR Labels

Create labels in your repository for semantic versioning:

1. Go to your repository → Issues → Labels
2. Create the following labels:
   - `major` - For breaking changes
   - `minor` - For new features (non-breaking)
   - `patch` - For bug fixes and small changes

#### 4. Repository Permissions

Ensure your repository has the appropriate permissions set:

1. Go to your repository settings
2. Navigate to Actions → General
3. Under "Workflow permissions", select "Read and write permissions"
4. Save the changes

### Using the Workflow

1. Create a new pull request
2. Add one of the version labels (`major`, `minor`, or `patch`) to the PR
3. The workflow will automatically detect the label and bump the version accordingly
4. A comment will be added to the PR with the version change details
5. When the PR is merged to the master branch, a GitHub release will be created automatically

### Customization

#### Modifying Trigger Events

To change when the version bump occurs:

1. Edit the `.github/workflows/auto-version-bump.yml` file
2. Modify the `on` section to trigger on different events

#### Changing Label Names

If you wish to use different label names:

1. Edit the `.github/workflows/auto-version-bump.yml` file
2. Modify the label detection logic in the "Determine version bump type" step

### Troubleshooting

- **Workflow fails with permission errors**: Ensure you've set the correct repository permissions as described above.
- **Version not incrementing**: Check that your version file is in one of the supported formats and that you've applied one of the required labels to the PR.
- **Changes not appearing in PR**: Verify that the GitHub Action has permission to push to branches.
- **Releases not being created**: Make sure the GitHub Action has write permissions for contents and that your GitHub token has the necessary permissions.