import os
from codeowners import CodeOwners

CHOSEN_FILE = "ci-steps/test_codeowners.py"

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
codeowners_fp = os.path.join(project_dir, ".github", "CODEOWNERS")

with open(codeowners_fp) as f:
    codeowners_content = f.read()
    codeowners_data = CodeOwners(codeowners_content)

approvers = codeowners_data.of(CHOSEN_FILE)
print(f"Here are the approvers of {CHOSEN_FILE}: {approvers}")