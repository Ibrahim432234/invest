"""Stock API endpoints"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from app.services.market_data import MarketDataService
from app.services.technical_analysis import TechnicalAnalysisService
from app.services.news_service import NewsService
from app.services.recommendation_service import RecommendationService
from app.schemas.stock import StockSearch, StockQuote
from app.schemas.price_data import HistoricalData, PriceDataBase
from app.schemas.technical_indicator import TechnicalData, TechnicalSignal
from app.schemas.fundamental import FundamentalData
from app.schemas.news import NewsData
from app.schemas.recommendation import Recommendation, Timeframe

router = APIRouter(prefix="/stocks", tags=["stocks"])
logger = logging.getLogger(__name__)


@router.get("/search", response_model=List[StockSearch])
async def search_stocks(
    q: str = Query(..., min_length=1, description="Search query (ticker or name)")
):
    """
    Search for stocks by ticker or name

    - **q**: Search query
    """
    try:
        results = MarketDataService.search_stock(q)
        return results
    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        raise HTTPException(status_code=500, detail="Error searching stocks")


@router.get("/{ticker}/quote", response_model=StockQuote)
async def get_stock_quote(ticker: str):
    """
    Get real-time quote for a stock

    - **ticker**: Stock ticker symbol (e.g., AAPL, MSFT)
    """
    try:
        quote = MarketDataService.get_quote(ticker.upper())
        if not quote:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
        return quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stock quote")


@router.get("/{ticker}/historical", response_model=HistoricalData)
async def get_historical_data(
    ticker: str,
    period: str = Query("1y", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$")
):
    """
    Get historical price data for a stock

    - **ticker**: Stock ticker symbol
    - **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    """
    try:
        hist_df = MarketDataService.get_historical_data(ticker.upper(), period)
        if hist_df is None or hist_df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for {ticker}"
            )

        # Convert DataFrame to list of dicts
        data = []
        for _, row in hist_df.iterrows():
            data.append(PriceDataBase(
                date=row['date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=int(row['volume'])
            ))

        return HistoricalData(ticker=ticker.upper(), period=period, data=data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching historical data")


@router.get("/{ticker}/technicals", response_model=TechnicalData)
async def get_technical_analysis(ticker: str):
    """
    Get technical analysis for a stock

    - **ticker**: Stock ticker symbol
    """
    try:
        # Fetch historical data
        hist_df = MarketDataService.get_historical_data(ticker.upper(), period='6mo')
        if hist_df is None or hist_df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {ticker}"
            )

        # Calculate technical indicators
        df_with_indicators = TechnicalAnalysisService.calculate_all_indicators(hist_df)

        # Get latest indicators
        latest = df_with_indicators.iloc[-1]
        current_price = float(latest['close'])

        # Get support and resistance
        support, resistance = TechnicalAnalysisService.find_support_resistance(
            df_with_indicators['close']
        )

        # Create indicators dict
        indicators_dict = {
            'date': latest['date'],
            'sma_20': float(latest['sma_20']) if not pd.isna(latest['sma_20']) else None,
            'sma_50': float(latest['sma_50']) if not pd.isna(latest['sma_50']) else None,
            'sma_200': float(latest['sma_200']) if not pd.isna(latest['sma_200']) else None,
            'ema_12': float(latest['ema_12']) if not pd.isna(latest['ema_12']) else None,
            'ema_26': float(latest['ema_26']) if not pd.isna(latest['ema_26']) else None,
            'rsi_14': float(latest['rsi_14']) if not pd.isna(latest['rsi_14']) else None,
            'macd': float(latest['macd']) if not pd.isna(latest['macd']) else None,
            'macd_signal': float(latest['macd_signal']) if not pd.isna(latest['macd_signal']) else None,
            'macd_histogram': float(latest['macd_histogram']) if not pd.isna(latest['macd_histogram']) else None,
            'bb_upper': float(latest['bb_upper']) if not pd.isna(latest['bb_upper']) else None,
            'bb_middle': float(latest['bb_middle']) if not pd.isna(latest['bb_middle']) else None,
            'bb_lower': float(latest['bb_lower']) if not pd.isna(latest['bb_lower']) else None,
            'bb_bandwidth': float(latest['bb_bandwidth']) if not pd.isna(latest['bb_bandwidth']) else None,
            'stoch_k': float(latest['stoch_k']) if not pd.isna(latest['stoch_k']) else None,
            'stoch_d': float(latest['stoch_d']) if not pd.isna(latest['stoch_d']) else None,
            'atr_14': float(latest['atr_14']) if not pd.isna(latest['atr_14']) else None,
            'support_level': support,
            'resistance_level': resistance,
            'obv': float(latest['obv']) if not pd.isna(latest['obv']) else None,
            'volume_sma_20': float(latest['volume_sma_20']) if not pd.isna(latest['volume_sma_20']) else None,
        }

        # Generate signals
        signals = TechnicalAnalysisService.generate_signals(indicators_dict)

        # Calculate overall score
        score, overall_signal = TechnicalAnalysisService.calculate_overall_score(signals)

        return TechnicalData(
            ticker=ticker.upper(),
            current_price=current_price,
            indicators=indicators_dict,
            signals=signals,
            overall_signal=overall_signal,
            score=score
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating technical analysis for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating technical analysis: {str(e)}")


@router.get("/{ticker}/fundamentals", response_model=FundamentalData)
async def get_fundamental_analysis(ticker: str):
    """
    Get fundamental analysis for a stock

    - **ticker**: Stock ticker symbol
    """
    try:
        fundamentals = MarketDataService.get_fundamentals(ticker.upper())
        if not fundamentals:
            raise HTTPException(
                status_code=404,
                detail=f"No fundamental data found for {ticker}"
            )

        # Get stock info for sector
        stock_info = MarketDataService.get_stock_info(ticker.upper())
        sector = stock_info.get('sector', '') if stock_info else ''

        # Get sector averages
        if sector:
            sector_avgs = MarketDataService.get_sector_avg_ratios(sector)
            fundamentals['sector_avg_pe'] = sector_avgs.get('pe_ratio')
            fundamentals['sector_avg_pb'] = sector_avgs.get('pb_ratio')

        # Simple analysis
        analysis = {}
        if fundamentals.get('pe_ratio'):
            pe = fundamentals['pe_ratio']
            sector_pe = fundamentals.get('sector_avg_pe', 20)
            if pe < sector_pe * 0.8:
                analysis['valuation'] = 'undervalued'
            elif pe > sector_pe * 1.5:
                analysis['valuation'] = 'overvalued'
            else:
                analysis['valuation'] = 'fairly valued'

        if fundamentals.get('dividend_yield'):
            dy = fundamentals['dividend_yield']
            if dy > 0.03:
                analysis['dividend'] = 'attractive'
            else:
                analysis['dividend'] = 'low'

        return FundamentalData(
            ticker=ticker.upper(),
            data=fundamentals,
            analysis=analysis
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching fundamental data")


@router.get("/{ticker}/news", response_model=NewsData)
async def get_stock_news(
    ticker: str,
    days: int = Query(7, ge=1, le=30, description="Number of days to look back")
):
    """
    Get news and sentiment for a stock

    - **ticker**: Stock ticker symbol
    - **days**: Number of days to look back (1-30)
    """
    try:
        news_service = NewsService()
        articles = news_service.fetch_stock_news(ticker.upper(), days)

        sentiment_summary = news_service.calculate_sentiment_summary(articles)

        return NewsData(
            ticker=ticker.upper(),
            news=articles,
            sentiment_summary=sentiment_summary
        )
    except Exception as e:
        logger.error(f"Error fetching news for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching news")


@router.get("/{ticker}/recommendation", response_model=Recommendation)
async def get_recommendation(
    ticker: str,
    timeframe: Timeframe = Query(Timeframe.MID, description="Investment timeframe")
):
    """
    Get investment recommendation for a stock

    - **ticker**: Stock ticker symbol
    - **timeframe**: Investment timeframe (short, mid, long)
    """
    try:
        # Get stock info
        stock_info = MarketDataService.get_stock_info(ticker.upper())
        if not stock_info:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")

        # Get current price
        quote = MarketDataService.get_quote(ticker.upper())
        if not quote:
            raise HTTPException(status_code=404, detail=f"Cannot get quote for {ticker}")

        current_price = quote['price']
        name = stock_info['name']

        # Get technical data
        try:
            hist_df = MarketDataService.get_historical_data(ticker.upper(), period='6mo')
            if hist_df is not None and not hist_df.empty:
                df_with_indicators = TechnicalAnalysisService.calculate_all_indicators(hist_df)
                latest = df_with_indicators.iloc[-1]

                technical_data = {
                    'current_price': current_price,
                    'indicators': {
                        'rsi_14': float(latest['rsi_14']) if not pd.isna(latest['rsi_14']) else None,
                        'macd_histogram': float(latest['macd_histogram']) if not pd.isna(latest['macd_histogram']) else None,
                        'sma_50': float(latest['sma_50']) if not pd.isna(latest['sma_50']) else None,
                        'sma_200': float(latest['sma_200']) if not pd.isna(latest['sma_200']) else None,
                        'bb_upper': float(latest['bb_upper']) if not pd.isna(latest['bb_upper']) else None,
                        'bb_lower': float(latest['bb_lower']) if not pd.isna(latest['bb_lower']) else None,
                    }
                }
            else:
                technical_data = None
        except Exception as e:
            logger.warning(f"Could not fetch technical data: {e}")
            technical_data = None

        # Get fundamental data
        try:
            fundamental_data = MarketDataService.get_fundamentals(ticker.upper())
        except Exception as e:
            logger.warning(f"Could not fetch fundamental data: {e}")
            fundamental_data = None

        # Get sentiment data
        try:
            news_service = NewsService()
            articles = news_service.fetch_stock_news(ticker.upper(), 7)
            sentiment_data = news_service.calculate_sentiment_summary(articles)
        except Exception as e:
            logger.warning(f"Could not fetch sentiment data: {e}")
            sentiment_data = None

        # Generate recommendation
        recommendation = RecommendationService.generate_recommendation(
            ticker=ticker.upper(),
            name=name,
            current_price=current_price,
            timeframe=timeframe,
            technical_data=technical_data,
            fundamental_data=fundamental_data,
            sentiment_data=sentiment_data
        )

        return recommendation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendation for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")


# Add pandas import at the top
import pandas as pd
