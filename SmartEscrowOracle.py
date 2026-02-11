# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class SmartEscrowOracle(gl.Contract):
    """
    Simple escrow that verifies GitHub PRs and issues for payment release
    """
    
    escrows: TreeMap[str, str]
    
    def __init__(self):
        self.escrows = TreeMap[str, str]()
    
    @gl.public.write
    def verify_github_pr_merged(self, pr_url: str) -> str:
        """
        Checks if a GitHub PR has been merged
        Example: https://github.com/ethereum/go-ethereum/pull/28000
        """
        input_prompt = f"""
Check if this GitHub Pull Request has been merged: {pr_url}

Determine:
- Is the PR merged? (yes/no)
- What is the current status?
"""
        
        task = """
Respond in JSON format:
{{
    "pr_url": str,
    "is_merged": bool,
    "status": str,
    "result": str (APPROVED or REJECTED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "PR must be actually merged for APPROVED result"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.escrows[f"pr_{pr_url}"] = result
        return result
    
    @gl.public.write
    def verify_github_issue_closed(self, issue_url: str) -> str:
        """
        Checks if a GitHub issue has been closed
        Example: https://github.com/ethereum/go-ethereum/issues/30000
        """
        input_prompt = f"""
Check if this GitHub Issue has been closed: {issue_url}

Determine:
- Is the issue closed? (yes/no)
- What is the current status?
"""
        
        task = """
Respond in JSON format:
{{
    "issue_url": str,
    "is_closed": bool,
    "status": str,
    "result": str (APPROVED or REJECTED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Issue must be actually closed for APPROVED result"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.escrows[f"issue_{issue_url}"] = result
        return result
    
    @gl.public.write
    def verify_webpage_contains_text(self, url: str, required_text: str) -> str:
        """
        Checks if a webpage contains specific text (milestone verification)
        Example: url = "https://example.org", required_text = "Example Domain"
        """
        input_prompt = f"""
Check if this webpage contains the required text:

URL: {url}
Required text: "{required_text}"

Search the webpage and verify if the text appears.
"""
        
        task = """
Respond in JSON format:
{{
    "url": str,
    "required_text": str,
    "text_found": bool,
    "result": str (APPROVED or REJECTED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Text must be found on the actual webpage for APPROVED result"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.escrows[f"webpage_{url}"] = result
        return result
    
    @gl.public.view
    def get_verification(self, key: str) -> str:
        """
        Get verification result
        """
        return self.escrows.get(key, '{"error": "Not found"}')
    
    @gl.public.view
    def get_all_verifications(self) -> dict[str, str]:
        """
        List all verifications
        """
        result = {}
        for key, value in self.escrows.items():
            result[key] = value
        return result
