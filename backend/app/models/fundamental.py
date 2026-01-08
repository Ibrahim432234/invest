"""Fundamental data model"""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Fundamental(Base):
    """Fundamental analysis data for stocks"""

    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Valuation ratios
    pe_ratio = Column(Float, nullable=True)  # Price-to-Earnings
    pb_ratio = Column(Float, nullable=True)  # Price-to-Book
    ps_ratio = Column(Float, nullable=True)  # Price-to-Sales
    peg_ratio = Column(Float, nullable=True)  # Price/Earnings to Growth

    # Profitability
    profit_margin = Column(Float, nullable=True)
    operating_margin = Column(Float, nullable=True)
    return_on_equity = Column(Float, nullable=True)  # ROE
    return_on_assets = Column(Float, nullable=True)  # ROA

    # Dividends
    dividend_yield = Column(Float, nullable=True)
    dividend_per_share = Column(Float, nullable=True)
    payout_ratio = Column(Float, nullable=True)

    # Growth
    revenue_growth = Column(Float, nullable=True)  # YoY
    earnings_growth = Column(Float, nullable=True)  # YoY
    eps = Column(Float, nullable=True)  # Earnings Per Share

    # Financial health
    debt_to_equity = Column(Float, nullable=True)
    current_ratio = Column(Float, nullable=True)
    quick_ratio = Column(Float, nullable=True)
    free_cash_flow = Column(Float, nullable=True)

    # Market data
    market_cap = Column(Float, nullable=True)
    enterprise_value = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)

    # Sector comparison
    sector_avg_pe = Column(Float, nullable=True)
    sector_avg_pb = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="fundamentals")

    def __repr__(self):
        return f"<Fundamental {self.stock_id} @ {self.date}>"
