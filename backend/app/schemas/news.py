"""News schemas"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class NewsBase(BaseModel):
    """Base news schema"""
    title: str = Field(..., max_length=500)
    source: Optional[str] = Field(None, max_length=100)
    url: Optional[str] = Field(None, max_length=1000)
    content: Optional[str] = None
    author: Optional[str] = Field(None, max_length=200)
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = Field(None, max_length=20)
    published_at: datetime


class NewsCreate(NewsBase):
    """Schema for creating news"""
    stock_id: int


class News(NewsBase):
    """News response schema"""
    id: int
    stock_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NewsData(BaseModel):
    """News feed response"""
    ticker: str
    news: List[NewsBase]
    sentiment_summary: dict
