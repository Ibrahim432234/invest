"""Pydantic schemas for request/response validation"""
from .stock import (
    StockBase,
    StockCreate,
    StockUpdate,
    Stock,
    StockSearch,
    StockQuote,
)
from .price_data import PriceData, PriceDataCreate, HistoricalData
from .fundamental import Fundamental, FundamentalCreate, FundamentalData
from .technical_indicator import TechnicalIndicator, TechnicalIndicatorCreate, TechnicalData
from .news import News, NewsCreate, NewsData
from .watchlist import Watchlist, WatchlistCreate, WatchlistResponse
from .recommendation import Recommendation, RecommendationRequest

__all__ = [
    "StockBase",
    "StockCreate",
    "StockUpdate",
    "Stock",
    "StockSearch",
    "StockQuote",
    "PriceData",
    "PriceDataCreate",
    "HistoricalData",
    "Fundamental",
    "FundamentalCreate",
    "FundamentalData",
    "TechnicalIndicator",
    "TechnicalIndicatorCreate",
    "TechnicalData",
    "News",
    "NewsCreate",
    "NewsData",
    "Watchlist",
    "WatchlistCreate",
    "WatchlistResponse",
    "Recommendation",
    "RecommendationRequest",
]
