"""Watchlist schemas"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class WatchlistBase(BaseModel):
    """Base watchlist schema"""
    notes: Optional[str] = Field(None, max_length=500)
    target_price: Optional[str] = Field(None, max_length=20)


class WatchlistCreate(WatchlistBase):
    """Schema for creating watchlist entry"""
    ticker: str
    user_id: str


class Watchlist(WatchlistBase):
    """Watchlist response schema"""
    id: int
    user_id: str
    stock_id: int
    added_at: datetime

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    """Watchlist with stock details"""
    id: int
    ticker: str
    name: str
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    notes: Optional[str] = None
    target_price: Optional[str] = None
    added_at: datetime
