"""Market data service using yfinance"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MarketDataService:
    """Service for fetching stock market data"""

    @staticmethod
    def search_stock(query: str) -> List[Dict]:
        """
        Search for stocks by ticker or name

        Args:
            query: Search query

        Returns:
            List of matching stocks
        """
        try:
            # yfinance doesn't have a native search, so we use Ticker for validation
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            if info and 'symbol' in info:
                return [{
                    'ticker': info.get('symbol', query.upper()),
                    'name': info.get('longName', info.get('shortName', '')),
                    'sector': info.get('sector', ''),
                    'industry': info.get('industry', ''),
                    'country': info.get('country', ''),
                    'exchange': info.get('exchange', '')
                }]
        except Exception as e:
            logger.error(f"Error searching for stock {query}: {e}")

        return []

    @staticmethod
    def get_stock_info(ticker: str) -> Optional[Dict]:
        """
        Get detailed stock information

        Args:
            ticker: Stock ticker symbol

        Returns:
            Stock information dictionary
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'ticker': info.get('symbol', ticker),
                'name': info.get('longName', info.get('shortName', '')),
                'isin': info.get('isin', None),
                'sector': info.get('sector', None),
                'industry': info.get('industry', None),
                'country': info.get('country', None),
                'exchange': info.get('exchange', None),
                'currency': info.get('currency', None),
                'market_cap': info.get('marketCap', None),
                'description': info.get('longBusinessSummary', None),
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return None

    @staticmethod
    def get_quote(ticker: str) -> Optional[Dict]:
        """
        Get real-time quote for a stock

        Args:
            ticker: Stock ticker symbol

        Returns:
            Quote dictionary
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Get latest price data
            hist = stock.history(period='5d')
            if hist.empty:
                return None

            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest

            current_price = float(latest['Close'])
            previous_close = float(previous['Close'])
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100

            return {
                'ticker': ticker,
                'name': info.get('longName', info.get('shortName', ticker)),
                'price': current_price,
                'change': change,
                'change_percent': change_percent,
                'volume': int(latest['Volume']),
                'market_cap': info.get('marketCap', None),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE', None)),
                'dividend_yield': info.get('dividendYield', None),
                'day_high': float(latest['High']),
                'day_low': float(latest['Low']),
                'year_high': info.get('fiftyTwoWeekHigh', None),
                'year_low': info.get('fiftyTwoWeekLow', None),
                'open': float(latest['Open']),
                'previous_close': previous_close,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {ticker}: {e}")
            return None

    @staticmethod
    def get_historical_data(ticker: str, period: str = '1y') -> Optional[pd.DataFrame]:
        """
        Get historical price data

        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            DataFrame with historical data
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            if hist.empty:
                return None

            # Rename columns to lowercase
            hist.columns = [col.lower() for col in hist.columns]

            # Reset index to get date as column
            hist.reset_index(inplace=True)
            hist['date'] = pd.to_datetime(hist['date']).dt.date

            return hist
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return None

    @staticmethod
    def get_fundamentals(ticker: str) -> Optional[Dict]:
        """
        Get fundamental data for a stock

        Args:
            ticker: Stock ticker symbol

        Returns:
            Fundamentals dictionary
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'date': datetime.now().date(),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE', None)),
                'pb_ratio': info.get('priceToBook', None),
                'ps_ratio': info.get('priceToSalesTrailing12Months', None),
                'peg_ratio': info.get('pegRatio', None),
                'profit_margin': info.get('profitMargins', None),
                'operating_margin': info.get('operatingMargins', None),
                'return_on_equity': info.get('returnOnEquity', None),
                'return_on_assets': info.get('returnOnAssets', None),
                'dividend_yield': info.get('dividendYield', None),
                'dividend_per_share': info.get('dividendRate', None),
                'payout_ratio': info.get('payoutRatio', None),
                'revenue_growth': info.get('revenueGrowth', None),
                'earnings_growth': info.get('earningsGrowth', None),
                'eps': info.get('trailingEps', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'current_ratio': info.get('currentRatio', None),
                'quick_ratio': info.get('quickRatio', None),
                'free_cash_flow': info.get('freeCashflow', None),
                'market_cap': info.get('marketCap', None),
                'enterprise_value': info.get('enterpriseValue', None),
                'beta': info.get('beta', None),
            }
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {e}")
            return None

    @staticmethod
    def get_sector_avg_ratios(sector: str) -> Dict:
        """
        Get average ratios for a sector (placeholder)

        Args:
            sector: Sector name

        Returns:
            Dictionary with sector averages
        """
        # This is a placeholder. In production, you'd fetch from a database
        # or external API with sector averages
        sector_averages = {
            'Technology': {'pe_ratio': 25.0, 'pb_ratio': 5.0},
            'Healthcare': {'pe_ratio': 20.0, 'pb_ratio': 4.0},
            'Financial Services': {'pe_ratio': 15.0, 'pb_ratio': 1.5},
            'Consumer Cyclical': {'pe_ratio': 18.0, 'pb_ratio': 3.0},
            'Energy': {'pe_ratio': 12.0, 'pb_ratio': 1.2},
        }

        return sector_averages.get(sector, {'pe_ratio': 20.0, 'pb_ratio': 3.0})
