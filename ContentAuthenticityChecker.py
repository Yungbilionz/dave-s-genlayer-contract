# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class ContentAuthenticityChecker(gl.Contract):
    """
    Verifies if content is original or plagiarized
    Perfect for hackathons, grants, NFT authenticity
    """
    
    verification_results: TreeMap[str, str]
    
    def __init__(self):
        self.verification_results = TreeMap[str, str]()
    
    @gl.public.write
    def check_article_originality(self, article_url: str) -> str:
        """
        Checks if an article/blog post is original
        Example: https://blog.genlayer.com/some-article
        """
        input_prompt = f"""
Check the originality of this article: {article_url}

Analyze:
- Is the content original?
- Are there signs of copy-paste from other sources?
- Does the writing style seem authentic?
- Any duplicate content indicators?
"""
        
        task = """
Respond in JSON format:
{{
    "url": str,
    "is_original": bool,
    "originality_score": int (0-100),
    "plagiarism_indicators": list[str],
    "result": str (ORIGINAL or PLAGIARIZED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Originality score should reflect actual content uniqueness"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.verification_results[f"article_{article_url}"] = result
        return result
    
    @gl.public.write
    def check_code_originality(self, repo_url: str) -> str:
        """
        Checks if a GitHub repo contains original code
        Example: https://github.com/user/repo
        """
        input_prompt = f"""
Check the originality of code in this repository: {repo_url}

Analyze:
- Is the code original?
- Are there signs of copy-paste from other repos?
- Does it look like a fork without attribution?
- Any plagiarism indicators?
"""
        
        task = """
Respond in JSON format:
{{
    "repo_url": str,
    "is_original": bool,
    "originality_score": int (0-100),
    "plagiarism_indicators": list[str],
    "result": str (ORIGINAL or PLAGIARIZED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Score should reflect actual code uniqueness based on public repo data"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.verification_results[f"code_{repo_url}"] = result
        return result
    
    @gl.public.write
    def check_text_originality(self, text: str) -> str:
        """
        Checks if submitted text is original
        Paste any text directly for verification
        Example: "This is my original research about blockchain..."
        """
        input_prompt = f"""
Check the originality of this text:

"{text}"

Analyze:
- Does this appear to be original writing?
- Are there signs of copying from known sources?
- Writing style consistency
- Originality indicators
"""
        
        task = """
Respond in JSON format:
{{
    "text_preview": str (first 50 chars),
    "is_original": bool,
    "originality_score": int (0-100),
    "plagiarism_indicators": list[str],
    "result": str (ORIGINAL or PLAGIARIZED)
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Score should reflect actual text originality based on AI analysis"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.verification_results[f"text_{text[:20]}"] = result
        return result
    
    @gl.public.view
    def get_verification(self, key: str) -> str:
        """Get specific verification result"""
        return self.verification_results.get(key, '{"error": "Not found"}')
    
    @gl.public.view
    def get_all_verifications(self) -> dict[str, str]:
        """List all verifications"""
        result = {}
        for key, value in self.verification_results.items():
            result[key] = value
        return result
    
    @gl.public.view
    def get_verification_count(self) -> int:
        """Count total verifications"""
        count = 0
        for _ in self.verification_results:
            count += 1
        return count
