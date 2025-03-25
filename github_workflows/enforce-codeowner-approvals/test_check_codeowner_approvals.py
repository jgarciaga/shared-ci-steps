#!/usr/bin/env python3

"""
Test Check Code Owner Approvals

Simple test script for the check_codeowner_approvals.py module

Usage: python test_check_codeowner_approvals.py
"""

import unittest
from check_codeowner_approvals import (
    parse_codeowners,
    is_file_matching_pattern,
    get_missing_approvals
)


class TestCodeOwnerApprovals(unittest.TestCase):
    def test_parse_codeowners(self):
        """Test parsing of CODEOWNERS file"""
        print('Testing parse_codeowners...')
        
        codeowners_content = """
        # This is a comment
        * @default-team
        /src/frontend/ @frontend-team
        *.js @javascript-developers
        /src/security/ @security-team @lead-developer
        """
        
        result = parse_codeowners(codeowners_content)
        
        print('Parsed CODEOWNERS:', result)
        
        # Verify the result
        self.assertEqual(len(result), 4, "Expected 4 patterns")
        self.assertEqual(result[0]['pattern'], '*')
        self.assertEqual(result[0]['owners'], ['default-team'])
        self.assertEqual(result[3]['pattern'], '/src/security/')
        self.assertEqual(result[3]['owners'], ['security-team', 'lead-developer'])
        
        print('parse_codeowners test passed')
        print('-----------------------------------')
    
    def test_is_file_matching_pattern(self):
        """Test pattern matching for files"""
        print('Testing is_file_matching_pattern...')
        
        test_cases = [
            {'file': 'src/frontend/app.js', 'pattern': '/src/frontend/', 'expected_match': True},
            {'file': 'src/backend/server.js', 'pattern': '/src/frontend/', 'expected_match': False},
            {'file': 'config.js', 'pattern': '*.js', 'expected_match': True},
            {'file': 'src/utils/helper.js', 'pattern': '*.js', 'expected_match': True},
            {'file': 'src/utils/helper.ts', 'pattern': '*.js', 'expected_match': False},
            {'file': 'src/security/auth.js', 'pattern': '/src/security/', 'expected_match': True},
            {'file': 'README.md', 'pattern': '*', 'expected_match': True},
            {'file': 'src/components/Button.jsx', 'pattern': '/src/components/**/*.jsx', 'expected_match': True},
        ]
        
        for case in test_cases:
            file_path = case['file']
            pattern = case['pattern']
            expected_match = case['expected_match']
            
            actual_match = is_file_matching_pattern(file_path, pattern)
            print(f"File: {file_path}, Pattern: {pattern}, Match: {actual_match}")
            
            self.assertEqual(actual_match, expected_match, 
                            f"Expected {expected_match} but got {actual_match} for {file_path} with pattern {pattern}")
        
        print('is_file_matching_pattern test passed')
        print('-----------------------------------')
    
    def test_get_missing_approvals(self):
        """Test identification of missing approvals"""
        print('Testing get_missing_approvals...')
        
        required_owners = {'frontend-team', 'security-team', 'lead-developer'}
        approvals = {'frontend-team', 'lead-developer'}
        
        missing_approvals = get_missing_approvals(required_owners, approvals)
        
        print('Required owners:', required_owners)
        print('Approvals:', approvals)
        print('Missing approvals:', missing_approvals)
        
        self.assertEqual(len(missing_approvals), 1, "Expected 1 missing approval")
        self.assertTrue('security-team' in missing_approvals, "Expected security-team to be missing")
        
        print('get_missing_approvals test passed')
        print('-----------------------------------')


if __name__ == '__main__':
    print('Running tests for check_codeowner_approvals.py')
    print('===================================')
    
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    print('All tests completed')
