import openai
from typing import Dict
from app.core.config import settings


class AIAnalyzer:
    """Анализатор тональности и содержания обращений"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """Анализ тональности обращения"""
        if settings.OPENAI_API_KEY:
            return await self._analyze_with_gpt(text)
        else:
            return self._analyze_with_rules(text)
    
    async def _analyze_with_gpt(self, text: str) -> Dict[str, any]:
        """Анализ тональности с GPT"""
        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            prompt = f"""Определи тональность следующего обращения: positive, negative, или neutral.

Обращение: {text}

Ответь в формате JSON:
{{
    "sentiment": "positive|negative|neutral",
    "confidence": 0.0-1.0
}}"""
            
            response = client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {"role": "system", "content": "Ты помощник для анализа тональности. Отвечай только валидным JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "sentiment": result.get("sentiment", "neutral"),
                "confidence": float(result.get("confidence", 0.7))
            }
        except Exception as e:
            return self._analyze_with_rules(text)
    
    def _analyze_with_rules(self, text: str) -> Dict[str, any]:
        """Правило-основанный анализ тональности"""
        text_lower = text.lower()
        
        negative_words = ["плохо", "ужасно", "не работает", "сломан", "проблема", "жалоба"]
        positive_words = ["спасибо", "хорошо", "отлично", "благодарю"]
        
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        if negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + negative_count * 0.1)
        elif positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + positive_count * 0.1)
        else:
            sentiment = "neutral"
            confidence = 0.6
        
        return {
            "sentiment": sentiment,
            "confidence": confidence
        }

