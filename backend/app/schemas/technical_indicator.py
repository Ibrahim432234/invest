"""Technical indicator schemas"""
from typing import Optional, Dict, List
from datetime import date, datetime
from pydantic import BaseModel


class TechnicalIndicatorBase(BaseModel):
    """Base technical indicator schema"""
    date: date
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    bb_bandwidth: Optional[float] = None
    stoch_k: Optional[float] = None
    stoch_d: Optional[float] = None
    atr_14: Optional[float] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    obv: Optional[float] = None
    volume_sma_20: Optional[float] = None


class TechnicalIndicatorCreate(TechnicalIndicatorBase):
    """Schema for creating technical indicator"""
    stock_id: int


class TechnicalIndicator(TechnicalIndicatorBase):
    """Technical indicator response schema"""
    id: int
    stock_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TechnicalSignal(BaseModel):
    """Trading signal from technical analysis"""
    indicator: str
    signal: str  # buy, sell, neutral
    value: float
    description: str


class TechnicalData(BaseModel):
    """Technical analysis response"""
    ticker: str
    current_price: float
    indicators: TechnicalIndicatorBase
    signals: List[TechnicalSignal]
    overall_signal: str  # strong_buy, buy, neutral, sell, strong_sell
    score: int  # -5 to +5
