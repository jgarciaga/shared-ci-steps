# Shared CI Steps

This repository contains reusable GitHub Actions workflows and steps for CI/CD pipelines.

## Automatic Version Bumping

This repository includes a GitHub Action workflow that automatically bumps the version number whenever a new pull request is created.

### How It Works

The workflow performs the following steps:

1. Detects when a new pull request is opened against the main branch
2. Identifies the versioning system used in your project (package.json, pyproject.toml, or a VERSION file)
3. Extracts the current version number
4. Increments the patch version (e.g., 1.0.0 → 1.0.1)
5. Updates the version in the appropriate file
6. Commits and pushes the change to the PR branch
7. Adds a comment to the PR with the version change details

### Setup Instructions

#### 1. Add the Workflow File

The workflow file is already included in this repository at `.github/workflows/auto-version-bump.yml`.

#### 2. Configure Version File (Optional)

The workflow automatically detects and supports three common version file formats:

- **package.json** - For JavaScript/Node.js projects
- **pyproject.toml** - For Python projects
- **VERSION** - A simple text file containing just the version number

If none of these files exist, the workflow will create a `VERSION` file with an initial version of `0.1.0`.

#### 3. Repository Permissions

Ensure your repository has the appropriate permissions set:

1. Go to your repository settings
2. Navigate to Actions > General
3. Under "Workflow permissions", select "Read and write permissions"
4. Save the changes

### Customization

#### Modifying Version Increment Logic

By default, the workflow increments the patch version (z in x.y.z). To change this behavior:

1. Edit the `.github/workflows/auto-version-bump.yml` file
2. In the "Bump patch version" step, modify the logic to increment the minor or major version instead

#### Triggering on Different Events

To change when the version bump occurs:

1. Edit the `.github/workflows/auto-version-bump.yml` file
2. Modify the `on` section to trigger on different events (e.g., merged PRs instead of opened PRs)

### Troubleshooting

- **Workflow fails with permission errors**: Ensure you've set the correct repository permissions as described above.
- **Version not incrementing**: Check that your version file is in one of the supported formats.
- **Changes not appearing in PR**: Verify that the GitHub Action has permission to push to branches.
### Advanced Usage

#### Manual Version Control

If you need to skip the automatic version bump for a specific PR, include `[skip-version]` in your PR title.

#### Major/Minor Version Bumps

To manually trigger a specific version bump type:

- Include `[bump-minor]` in your PR title to bump the minor version (x.y.z → x.y+1.0)
- Include `[bump-major]` in your PR title to bump the major version (x.y.z → x+1.0.0)