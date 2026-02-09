# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class ProductReviewAuthenticator(gl.Contract):
    verified_products: TreeMap[str, str]
    
    def __init__(self):
        self.verified_products = TreeMap[str, str]()
    
    @gl.public.write
    def verify_product_reviews(self, product_url: str, product_name: str) -> str:
        input_prompt = f"""
You are analyzing a product page for review authenticity.

Product: {product_name}
URL: {product_url}

Fetch the webpage and analyze its content for signs of fake reviews.
"""
        
        task = """
Look for these RED FLAGS in the content:
1. Repetitive language patterns across reviews
2. Generic phrases without specifics
3. Overly positive language with no criticisms

Provide a JSON response with the following format:
{{
    "authenticity_score": int (0-100),
    "is_genuine": bool,
    "reasoning": str
}}

It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
"""
        
        criteria = "The authenticity score should be between 0-100 and reasoning should explain the decision"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        self.verified_products[product_url] = result
        
        return result
    
    @gl.public.view
    def get_product_verification(self, product_url: str) -> str:
        return self.verified_products.get(product_url, '{"error": "Product not yet verified"}')
    
    @gl.public.view
    def get_verified_count(self) -> int:
        count = 0
        for _ in self.verified_products:
            count += 1
        return count
