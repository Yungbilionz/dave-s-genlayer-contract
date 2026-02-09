# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class SecureApiGateway(gl.Contract):
    """
    Secure gateway for Intelligent Contracts to interact with external APIs
    - Weather data
    - Crypto price feeds
    - News sentiment analysis
    """
    
    api_responses: TreeMap[str, str]
    admin: Address
    
    def __init__(self):
        self.api_responses = TreeMap[str, str]()
        self.admin = gl.message.sender_address
    
    @gl.public.write
    def fetch_weather_data(self, city: str) -> str:
        """
        Fetches current weather data for a city
        """
        input_prompt = f"""
Fetch weather data for the city: {city}

You need to get current weather information including:
- Temperature
- Weather conditions (sunny, rainy, etc)
- Humidity
- Wind speed

Use publicly available weather data sources.
"""
        
        task = """
Provide weather information in the following JSON format:
{{
    "city": str,
    "temperature_celsius": float,
    "conditions": str,
    "humidity_percent": int,
    "wind_speed_kmh": float,
    "timestamp": str
}}

It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters.
"""
        
        criteria = "Temperature should be realistic for the location, conditions should be descriptive"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        cache_key = f"weather_{city}"
        self.api_responses[cache_key] = result
        
        return result
    
    @gl.public.write
    def fetch_crypto_price(self, symbol: str) -> str:
        """
        Fetches current cryptocurrency price
        Examples: BTC, ETH, SOL
        """
        input_prompt = f"""
Fetch the current price of cryptocurrency: {symbol}

Get real-time price data from multiple sources like:
- CoinGecko
- CoinMarketCap
- Binance
- Coinbase

Cross-reference multiple sources for accuracy.
"""
        
        task = """
Provide cryptocurrency price information in JSON format:
{{
    "symbol": str,
    "price_usd": float,
    "price_change_24h_percent": float,
    "market_cap_usd": float,
    "volume_24h_usd": float,
    "last_updated": str
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Price should be cross-verified from multiple sources, changes should be realistic"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        cache_key = f"crypto_{symbol}"
        self.api_responses[cache_key] = result
        
        return result
    
    @gl.public.write
    def fetch_news_sentiment(self, topic: str) -> str:
        """
        Analyzes news sentiment around a specific topic
        Useful for market predictions, reputation monitoring
        """
        input_prompt = f"""
Analyze recent news sentiment about: {topic}

Search recent news articles (last 24-48 hours) and determine:
- Overall sentiment (positive/negative/neutral)
- Key events or announcements
- Public perception
- Trending keywords
"""
        
        task = """
Provide news sentiment analysis in JSON format:
{{
    "topic": str,
    "overall_sentiment": str (positive/negative/neutral),
    "sentiment_score": float (-1.0 to 1.0),
    "key_events": list[str],
    "trending_keywords": list[str],
    "article_count": int,
    "last_updated": str
}}

It is mandatory that you respond only using the JSON format above.
"""
        
        criteria = "Sentiment should reflect actual news coverage, events should be verifiable"
        
        result = gl.eq_principle.prompt_non_comparative(
            lambda: input_prompt,
            task=task,
            criteria=criteria,
        ).replace("```json", "").replace("```", "")
        
        cache_key = f"sentiment_{topic}"
        self.api_responses[cache_key] = result
        
        return result
    
    # READ METHODS
    
    @gl.public.view
    def get_cached_response(self, cache_key: str) -> str:
        """
        Retrieve previously fetched API data
        """
        return self.api_responses.get(cache_key, '{"error": "No data found for this key"}')
    
    @gl.public.view
    def get_all_cache_keys(self) -> dict[str, str]:
        """
        List all cached API responses
        """
        result = {}
        for key, value in self.api_responses.items():
            result[key] = value
        return result
    
    @gl.public.view
    def get_data_count(self) -> int:
        """
        Count how many API responses are cached
        """
        count = 0
        for _ in self.api_responses:
            count += 1
        return count
