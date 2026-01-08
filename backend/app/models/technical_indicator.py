"""Technical indicator model"""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TechnicalIndicator(Base):
    """Technical analysis indicators for stocks"""

    __tablename__ = "technical_indicators"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Moving Averages
    sma_20 = Column(Float, nullable=True)  # 20-day Simple Moving Average
    sma_50 = Column(Float, nullable=True)  # 50-day SMA
    sma_200 = Column(Float, nullable=True)  # 200-day SMA
    ema_12 = Column(Float, nullable=True)  # 12-day Exponential Moving Average
    ema_26 = Column(Float, nullable=True)  # 26-day EMA

    # RSI (Relative Strength Index)
    rsi_14 = Column(Float, nullable=True)  # 14-period RSI

    # MACD (Moving Average Convergence Divergence)
    macd = Column(Float, nullable=True)
    macd_signal = Column(Float, nullable=True)
    macd_histogram = Column(Float, nullable=True)

    # Bollinger Bands
    bb_upper = Column(Float, nullable=True)
    bb_middle = Column(Float, nullable=True)
    bb_lower = Column(Float, nullable=True)
    bb_bandwidth = Column(Float, nullable=True)

    # Stochastic Oscillator
    stoch_k = Column(Float, nullable=True)
    stoch_d = Column(Float, nullable=True)

    # ATR (Average True Range) - Volatility
    atr_14 = Column(Float, nullable=True)

    # Support and Resistance (calculated)
    support_level = Column(Float, nullable=True)
    resistance_level = Column(Float, nullable=True)

    # Volume indicators
    obv = Column(Float, nullable=True)  # On-Balance Volume
    volume_sma_20 = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="technical_indicators")

    # Composite index
    __table_args__ = (
        Index("idx_technical_stock_date", "stock_id", "date"),
    )

    def __repr__(self):
        return f"<TechnicalIndicator {self.stock_id} @ {self.date}>"
