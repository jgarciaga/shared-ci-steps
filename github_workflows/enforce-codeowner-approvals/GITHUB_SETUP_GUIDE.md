# GitHub Setup Guide: Testing Code Owner Approval Checks

This guide will walk you through setting up a test repository on GitHub to test the code owner approval check workflow.

## Step 1: Create a New Repository on GitHub

1. Login to your GitHub account
2. Click the '+' icon in the top-right corner and select 'New repository'
3. Name your repository (e.g., 'codeowner-approval-test')
4. Add a description (optional)
5. Choose 'Public' visibility (makes it easier to add collaborators for testing)
6. Initialize with a README (optional)
7. Click 'Create repository'

## Step 2: Upload the Test Repository Files

You can either use the GitHub web interface or Git commands to upload the test repository files.

### Option A: Using GitHub Web Interface

1. In your new GitHub repository, click the 'Add file' button and select 'Upload files'
2. Upload all files from the `test-repo` directory
3. Make sure to maintain the directory structure
4. Commit the changes directly to the main branch

### Option B: Using Git Commands

1. Clone your new GitHub repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/codeowner-approval-test.git
   ```

2. Copy all files from the `test-repo` directory to your cloned repository

3. Add, commit, and push the files:
   ```bash
   git add .
   git commit -m "Initial commit with test repository setup"
   git push origin main
   ```

## Step 3: Add Collaborators for Testing

To properly test code owner approvals, you need other GitHub users who can review your pull requests:

1. Go to your repository's 'Settings' tab
2. Click on 'Collaborators and teams' in the left sidebar
3. Click 'Add people' and invite collaborators using their GitHub usernames or email addresses
4. Assign roles based on the code owner patterns in `.github/CODEOWNERS`:
   - Invite someone as `@frontend-developer`
   - Invite someone as `@backend-developer` 
   - Invite someone as `@documentation-team`
   - Invite someone as `@tech-writer`

   **Note:** If you don't have collaborators available, you can create alternate GitHub accounts for testing.

## Step 4: Configure Branch Protection Rules

To enforce the code owner approval check, set up branch protection rules:

1. Go to your repository's 'Settings' tab
2. Click on 'Branches' in the left sidebar
3. Under 'Branch protection rules', click 'Add rule'
4. In the 'Branch name pattern' field, enter `master`
5. Check the following options:
   - [x] Require a pull request before merging
   - [x] Require approvals
   - [x] Require review from Code Owners
   - [x] Require status checks to pass before merging
6. Click 'Create' to save the rule

## Step 5: Test the Workflow with a Pull Request

1. Create a new branch:
   ```bash
   git checkout -b test-feature
   ```

2. Make changes to files in different directories:
   - Edit a file in `/src/frontend/` (requires @frontend-developer approval)
   - Edit a file in `/src/backend/` (requires @backend-developer approval)
   - Edit the README.md (requires @documentation-team and @tech-writer approval)

3. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Test changes for code owner approval check"
   git push origin test-feature
   ```

4. Create a pull request:
   - Go to your repository on GitHub
   - You should see a notification to create a pull request for your recent push
   - Click 'Compare & pull request'
   - Add a title and description
   - Click 'Create pull request'

5. Observe the workflow in action:
   - Go to the 'Actions' tab in your repository
   - You should see the 'Code Owner Approval Check' workflow running
   - When it completes, it will add a comment to the PR listing the required approvals

6. Test the approval process:
   - Have the required code owners review and approve the PR
   - After each approval, the workflow will run again and update the comment
   - Once all required approvals are obtained, the PR should be eligible for merging

## Troubleshooting

### Workflow Doesn't Run

- Check that the workflow file (`.github/workflows/codeowner-approval-check.yml`) is properly formatted
- Verify that GitHub Actions is enabled for your repository (Settings > Actions > General)

### Missing Approvals Not Detected

- Ensure your CODEOWNERS file is properly formatted
- Check that collaborators' GitHub usernames exactly match the names in the CODEOWNERS file
- Verify that the PR contains changes to files that match the patterns in CODEOWNERS

### Review Approvals Not Recognized

- Make sure reviewers are clicking 'Approve' and not just commenting
- Verify that reviewers have proper permissions in the repository

## Next Steps

After successfully testing with this setup, you can incorporate the code owner approval check workflow into your actual repositories by:

1. Adding a proper CODEOWNERS file that reflects your team structure
2. Setting up the GitHub Actions workflow in your main repositories
3. Configuring branch protection rules to require code owner approvals
