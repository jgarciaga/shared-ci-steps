#!/usr/bin/env python3

"""
Check Code Owner Approvals

A Python script to verify that pull requests have been approved by all required code owners.

Usage: python check_codeowner_approvals.py

Environment variables:
- GITHUB_TOKEN: GitHub API token (required)
- GITHUB_REPOSITORY: Owner/repo (required)
- GITHUB_EVENT_PATH: Path to the event payload JSON file (required for GitHub Actions)
- CODEOWNERS_PATH: Path to the CODEOWNERS file (optional, default: .github/CODEOWNERS)
- REQUIRE_ALL_OWNERS: Whether to require all code owners to approve (optional, default: true)
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Set, Any, Tuple, Optional
import requests

# Configuration
CONFIG_DEFAULTS = {
    'codeowners_path': '.github/CODEOWNERS',
    'require_all_owners': True,
    'github_token': os.environ.get('GITHUB_TOKEN'),
    'repository': os.environ.get('GITHUB_REPOSITORY'),
    'event_path': os.environ.get('GITHUB_EVENT_PATH')
}


def parse_codeowners(content: str) -> List[Dict[str, Any]]:
    """
    Parse the CODEOWNERS file content
    
    Args:
        content: The content of the CODEOWNERS file
        
    Returns:
        A list of dictionaries with 'pattern' and 'owners' keys
    """
    result = []
    lines = content.split('\n')
    
    for line in lines:
        trimmed_line = line.strip()
        # Skip empty lines and comments
        if not trimmed_line or trimmed_line.startswith('#'):
            continue
        
        parts = re.split(r'\s+', trimmed_line)
        if len(parts) >= 2:
            pattern = parts[0]
            owners = [owner[1:] if owner.startswith('@') else owner for owner in parts[1:]]
            result.append({'pattern': pattern, 'owners': owners})
    
    return result


def is_file_matching_pattern(file_path: str, pattern: str) -> bool:
    """
    Check if a file path matches a pattern from CODEOWNERS
    
    Args:
        file_path: The path of the file to check
        pattern: The pattern to match against
        
    Returns:
        True if the file matches the pattern, False otherwise
    """
    # Convert the glob pattern to a Python regex
    # This is a simplified version, not handling all glob syntax
    regex_pattern = pattern
    
    # Handle directory wildcards
    regex_pattern = regex_pattern.replace('/**', '(/.*)?')
    
    # Handle single wildcards
    regex_pattern = regex_pattern.replace('*', '[^/]*')
    
    # Handle specific directory patterns
    regex_pattern = f"^{regex_pattern.replace('/', '/')}$"
    
    try:
        regex = re.compile(regex_pattern)
        return bool(regex.match(file_path))
    except re.error:
        print(f"Warning: Invalid regex pattern: {regex_pattern}")
        return False


def get_required_owners(changed_files: List[Dict[str, Any]], codeowners_map: List[Dict[str, Any]]) -> Set[str]:
    """
    Determine the required code owners for the changed files
    
    Args:
        changed_files: List of changed files from GitHub API
        codeowners_map: The parsed CODEOWNERS data
        
    Returns:
        A set of required code owners
    """
    required_owners = set()
    
    for file in changed_files:
        file_path = file['filename']
        
        # Find matching patterns in CODEOWNERS
        for entry in codeowners_map:
            if is_file_matching_pattern(file_path, entry['pattern']):
                for owner in entry['owners']:
                    required_owners.add(owner)
    
    return required_owners


def get_approvals(reviews: List[Dict[str, Any]]) -> Set[str]:
    """
    Get the list of users who have approved the PR
    
    Args:
        reviews: List of pull request reviews from GitHub API
        
    Returns:
        A set of usernames who have approved the PR
    """
    approvals = set()
    reviews_by_user = {}
    
    # Group reviews by user, keeping only the latest review
    for review in reviews:
        username = review['user']['login']
        submitted_at = datetime.fromisoformat(review['submitted_at'].replace('Z', '+00:00'))
        
        if username not in reviews_by_user or submitted_at > datetime.fromisoformat(reviews_by_user[username]['submitted_at'].replace('Z', '+00:00')):
            reviews_by_user[username] = review
    
    # Add users with approved reviews
    for username, review in reviews_by_user.items():
        if review['state'] == 'APPROVED':
            approvals.add(username)
    
    return approvals


def get_missing_approvals(required_owners: Set[str], approvals: Set[str]) -> Set[str]:
    """
    Determine which required owners have not approved the PR
    
    Args:
        required_owners: Set of required code owners
        approvals: Set of users who have approved the PR
        
    Returns:
        A set of code owners who have not approved the PR
    """
    return required_owners - approvals


def github_api_request(endpoint: str, token: str, repo: str, **params) -> Dict[str, Any]:
    """
    Make a request to the GitHub API
    
    Args:
        endpoint: The API endpoint to request
        token: The GitHub API token
        repo: The repository name (owner/repo)
        **params: Additional parameters for the request
        
    Returns:
        The JSON response from the API
    """
    url = f"https://api.github.com/repos/{repo}/{endpoint}"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f"token {token}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()


def check_code_owner_approvals(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main function to check code owner approvals
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        A dictionary with results of the check
    """
    # Merge provided config with defaults
    if config is None:
        config = {}
    
    config = {**CONFIG_DEFAULTS, **config}
    
    codeowners_path = config['codeowners_path']
    require_all_owners = config['require_all_owners']
    github_token = config['github_token']
    repository = config['repository']
    event_path = config['event_path']
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN is required")
    
    if not repository:
        raise ValueError("GITHUB_REPOSITORY is required")
    
    # Get PR number from event payload
    pr_number = None
    if event_path and os.path.exists(event_path):
        with open(event_path, 'r') as f:
            event_payload = json.load(f)
            pr_number = event_payload.get('pull_request', {}).get('number')
    
    if not pr_number:
        raise ValueError("Pull request number not found")
    
    print(f"Checking code owner approvals for PR #{pr_number}")
    
    # Check if CODEOWNERS file exists
    if not os.path.exists(codeowners_path):
        error_msg = f"CODEOWNERS file not found at {codeowners_path}"
        print(error_msg, file=sys.stderr)
        return {'success': False, 'error': error_msg}
    
    try:
        # 1. Get changed files in the PR
        changed_files = github_api_request(f"pulls/{pr_number}/files", github_token, repository)
        print(f"PR has {len(changed_files)} changed files")
        
        # 2. Parse CODEOWNERS file
        with open(codeowners_path, 'r') as f:
            codeowners_content = f.read()
        
        codeowners_map = parse_codeowners(codeowners_content)
        
        # 3. Determine required code owners for changed files
        required_owners = get_required_owners(changed_files, codeowners_map)
        
        if not required_owners:
            print("No code owners required for the changed files")
            return {'success': True, 'message': 'No code owners required for the changed files'}
        
        print(f"Required approvals from: {', '.join(required_owners)}")
        
        # 4. Get reviews for the PR
        reviews = github_api_request(f"pulls/{pr_number}/reviews", github_token, repository)
        
        # 5. Determine which code owners have approved
        approvals = get_approvals(reviews)
        print(f"PR has approvals from: {', '.join(approvals) if approvals else 'none'}")
        
        # 6. Check if all required owners have approved
        missing_approvals = get_missing_approvals(required_owners, approvals)
        
        if not missing_approvals:
            return {
                'success': True,
                'message': 'All required code owners have approved this PR',
                'requiredOwners': list(required_owners),
                'approvals': list(approvals)
            }
        else:
            return {
                'success': False,
                'message': f"Missing approvals from: {', '.join(missing_approvals)}",
                'requiredOwners': list(required_owners),
                'approvals': list(approvals),
                'missingApprovals': list(missing_approvals)
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f"Error checking approvals: {str(e)}"
        }


if __name__ == "__main__":
    try:
        result = check_code_owner_approvals()
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['success'] else 1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
