import openai
from typing import Dict, Optional
from app.core.config import settings
from app.models.appeal import AppealCategory, AppealPriority

# Категории и их ключевые слова для классификации
CATEGORY_KEYWORDS = {
    AppealCategory.ROADS: ["дорога", "яма", "асфальт", "тротуар", "транспорт", "пробка", "парковка"],
    AppealCategory.LIGHTING: ["освещение", "фонарь", "свет", "темно", "лампа"],
    AppealCategory.IMPROVEMENT: ["благоустройство", "скамейка", "парк", "сквер", "двор", "детская площадка"],
    AppealCategory.ECOLOGY: ["мусор", "отходы", "экология", "свалка", "загрязнение", "воздух"],
    AppealCategory.SAFETY: ["безопасность", "опасно", "травма", "авария", "преступление"],
    AppealCategory.HEALTHCARE: ["больница", "поликлиника", "врач", "здоровье", "медицина"],
    AppealCategory.UTILITIES: ["коммунальные", "вода", "отопление", "электричество", "канализация"],
    AppealCategory.SOCIAL: ["социальная помощь", "пенсия", "льготы", "инвалид", "малоимущий"],
}


class AIClassifier:
    """Классификатор обращений с использованием AI"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def classify_appeal(
        self,
        title: str,
        description: str
    ) -> Dict[str, any]:
        """
        Классифицирует обращение по категории и приоритету
        """
        text = f"{title}\n{description}"
        
        # Если есть OpenAI API ключ, используем GPT
        if settings.OPENAI_API_KEY:
            return await self._classify_with_gpt(text)
        else:
            # Fallback на правило-основанную классификацию
            return self._classify_with_rules(text)
    
    async def _classify_with_gpt(self, text: str) -> Dict[str, any]:
        """Классификация с использованием GPT"""
        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            prompt = f"""Проанализируй следующее обращение гражданина и определи:
1. Категорию из списка: roads, lighting, improvement, ecology, safety, healthcare, utilities, social, other
2. Приоритет: low, medium, high, urgent
3. Краткое резюме проблемы (1-2 предложения)

Обращение: {text}

Ответь в формате JSON:
{{
    "category": "category_name",
    "priority": "priority_level",
    "summary": "краткое резюме",
    "confidence": 0.0-1.0
}}"""
            
            response = client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {"role": "system", "content": "Ты помощник для классификации обращений граждан. Отвечай только валидным JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=200
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "category": AppealCategory(result.get("category", "other")),
                "priority": AppealPriority(result.get("priority", "medium")),
                "summary": result.get("summary", ""),
                "confidence": float(result.get("confidence", 0.7))
            }
        except Exception as e:
            # Fallback на правила
            return self._classify_with_rules(text)
    
    def _classify_with_rules(self, text: str) -> Dict[str, any]:
        """Правило-основанная классификация"""
        text_lower = text.lower()
        
        # Определение категории
        category_scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        if category_scores:
            category = max(category_scores, key=category_scores.get)
            if category_scores[category] == 0:
                category = AppealCategory.OTHER
        else:
            category = AppealCategory.OTHER
        
        # Определение приоритета
        urgent_keywords = ["срочно", "опасно", "авария", "травма", "пожар"]
        high_keywords = ["важно", "критично", "не работает", "сломан"]
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            priority = AppealPriority.URGENT
        elif any(keyword in text_lower for keyword in high_keywords):
            priority = AppealPriority.HIGH
        elif len(text) < 50:
            priority = AppealPriority.LOW
        else:
            priority = AppealPriority.MEDIUM
        
        return {
            "category": category,
            "priority": priority,
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "confidence": 0.6
        }
    
    async def detect_duplicate(
        self,
        new_text: str,
        existing_texts: list[str]
    ) -> Optional[int]:
        """Определение дубликатов обращений"""
        # Упрощенная проверка на дубликаты
        # В продакшне можно использовать embeddings
        new_text_lower = new_text.lower()
        
        for idx, existing_text in enumerate(existing_texts):
            existing_lower = existing_text.lower()
            # Простая проверка на схожесть
            if len(set(new_text_lower.split()) & set(existing_lower.split())) > 5:
                return idx
        
        return None

