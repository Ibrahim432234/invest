"""Price data schemas"""
from typing import List
from datetime import date, datetime
from pydantic import BaseModel


class PriceDataBase(BaseModel):
    """Base price data schema"""
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: float | None = None


class PriceDataCreate(PriceDataBase):
    """Schema for creating price data"""
    stock_id: int


class PriceData(PriceDataBase):
    """Price data response schema"""
    id: int
    stock_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HistoricalData(BaseModel):
    """Historical price data response"""
    ticker: str
    period: str
    data: List[PriceDataBase]
