"""Recommendation schemas"""
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class Timeframe(str, Enum):
    """Investment timeframe"""
    SHORT = "short"  # 1-4 weeks
    MID = "mid"  # 1-6 months
    LONG = "long"  # 6+ months


class RecommendationAction(str, Enum):
    """Recommendation action"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class RecommendationRequest(BaseModel):
    """Request for stock recommendation"""
    ticker: str
    timeframe: Timeframe = Timeframe.MID


class RecommendationReason(BaseModel):
    """Reason for recommendation"""
    category: str  # technical, fundamental, sentiment
    indicator: str
    value: str
    impact: str  # positive, negative, neutral
    weight: float  # 0.0 - 1.0


class Recommendation(BaseModel):
    """Stock recommendation response"""
    ticker: str
    name: str
    timeframe: Timeframe
    action: RecommendationAction
    score: int  # -10 to +10
    confidence: float  # 0.0 - 1.0
    current_price: float
    target_price: Optional[float] = None
    reasons: List[RecommendationReason]
    technical_score: int
    fundamental_score: int
    sentiment_score: int
    summary: str
    risks: List[str]
    timestamp: str
