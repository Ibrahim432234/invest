"""Fundamental data schemas"""
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class FundamentalBase(BaseModel):
    """Base fundamental schema"""
    date: date
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None
    dividend_yield: Optional[float] = None
    dividend_per_share: Optional[float] = None
    payout_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    eps: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    beta: Optional[float] = None
    sector_avg_pe: Optional[float] = None
    sector_avg_pb: Optional[float] = None


class FundamentalCreate(FundamentalBase):
    """Schema for creating fundamental data"""
    stock_id: int


class Fundamental(FundamentalBase):
    """Fundamental data response schema"""
    id: int
    stock_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FundamentalData(BaseModel):
    """Fundamental data response with analysis"""
    ticker: str
    data: FundamentalBase
    analysis: dict
