"""Stock schemas"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StockBase(BaseModel):
    """Base stock schema"""
    ticker: str = Field(..., max_length=10)
    name: str = Field(..., max_length=255)
    isin: Optional[str] = Field(None, max_length=12)
    wkn: Optional[str] = Field(None, max_length=6)
    sector: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=2)
    exchange: Optional[str] = Field(None, max_length=50)
    currency: Optional[str] = Field(None, max_length=3)
    market_cap: Optional[float] = None


class StockCreate(StockBase):
    """Schema for creating a stock"""
    pass


class StockUpdate(BaseModel):
    """Schema for updating a stock"""
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None


class Stock(StockBase):
    """Stock response schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StockSearch(BaseModel):
    """Search result for stocks"""
    ticker: str
    name: str
    sector: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None


class StockQuote(BaseModel):
    """Real-time stock quote"""
    ticker: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    day_high: float
    day_low: float
    year_high: Optional[float] = None
    year_low: Optional[float] = None
    open: float
    previous_close: float
    timestamp: datetime
