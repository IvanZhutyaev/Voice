from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime


class AnalyticsResponse(BaseModel):
    total_appeals: int
    appeals_by_status: Dict[str, int]
    appeals_by_category: Dict[str, int]
    appeals_by_priority: Dict[str, int]
    average_resolution_time: float  # в часах
    resolution_rate: float  # процент решенных
    appeals_timeline: List[Dict[str, Any]]
    top_districts: List[Dict[str, Any]]
    sentiment_distribution: Dict[str, int]

