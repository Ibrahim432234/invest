"""Recommendation service for generating investment recommendations"""
from typing import Dict, List, Optional
from datetime import datetime
import logging
from app.schemas.recommendation import (
    Timeframe,
    RecommendationAction,
    RecommendationReason
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating stock recommendations"""

    @staticmethod
    def generate_recommendation(
        ticker: str,
        name: str,
        current_price: float,
        timeframe: Timeframe,
        technical_data: Optional[Dict] = None,
        fundamental_data: Optional[Dict] = None,
        sentiment_data: Optional[Dict] = None
    ) -> Dict:
        """
        Generate investment recommendation based on timeframe

        Args:
            ticker: Stock ticker symbol
            name: Stock name
            current_price: Current stock price
            timeframe: Investment timeframe (short, mid, long)
            technical_data: Technical analysis data
            fundamental_data: Fundamental analysis data
            sentiment_data: Sentiment analysis data

        Returns:
            Recommendation dictionary
        """
        reasons = []
        technical_score = 0
        fundamental_score = 0
        sentiment_score = 0
        risks = []

        # Weight factors based on timeframe
        if timeframe == Timeframe.SHORT:
            tech_weight = 0.7
            fund_weight = 0.1
            sent_weight = 0.2
        elif timeframe == Timeframe.MID:
            tech_weight = 0.4
            fund_weight = 0.4
            sent_weight = 0.2
        else:  # LONG
            tech_weight = 0.2
            fund_weight = 0.6
            sent_weight = 0.2

        # Technical Analysis
        if technical_data:
            tech_result = RecommendationService._analyze_technical(technical_data)
            technical_score = tech_result['score']
            reasons.extend(tech_result['reasons'])
            risks.extend(tech_result['risks'])

        # Fundamental Analysis
        if fundamental_data:
            fund_result = RecommendationService._analyze_fundamental(fundamental_data)
            fundamental_score = fund_result['score']
            reasons.extend(fund_result['reasons'])
            risks.extend(fund_result['risks'])

        # Sentiment Analysis
        if sentiment_data:
            sent_result = RecommendationService._analyze_sentiment(sentiment_data)
            sentiment_score = sent_result['score']
            reasons.extend(sent_result['reasons'])

        # Calculate weighted score
        total_score = (
            technical_score * tech_weight +
            fundamental_score * fund_weight +
            sentiment_score * sent_weight
        )

        # Determine action and confidence
        action, confidence = RecommendationService._determine_action(
            total_score, timeframe
        )

        # Calculate target price (simplified)
        target_price = RecommendationService._calculate_target_price(
            current_price, total_score, timeframe
        )

        # Generate summary
        summary = RecommendationService._generate_summary(
            action, timeframe, technical_score, fundamental_score, sentiment_score
        )

        return {
            'ticker': ticker,
            'name': name,
            'timeframe': timeframe,
            'action': action,
            'score': round(total_score, 2),
            'confidence': round(confidence, 2),
            'current_price': current_price,
            'target_price': target_price,
            'reasons': reasons,
            'technical_score': technical_score,
            'fundamental_score': fundamental_score,
            'sentiment_score': sentiment_score,
            'summary': summary,
            'risks': risks,
            'timestamp': datetime.now().isoformat()
        }

    @staticmethod
    def _analyze_technical(data: Dict) -> Dict:
        """Analyze technical indicators"""
        score = 0
        reasons = []
        risks = []

        indicators = data.get('indicators', {})

        # RSI Analysis
        rsi = indicators.get('rsi_14')
        if rsi is not None:
            if rsi < 30:
                score += 2
                reasons.append({
                    'category': 'technical',
                    'indicator': 'RSI',
                    'value': f'{rsi:.2f}',
                    'impact': 'positive',
                    'weight': 0.8
                })
            elif rsi > 70:
                score -= 2
                reasons.append({
                    'category': 'technical',
                    'indicator': 'RSI',
                    'value': f'{rsi:.2f}',
                    'impact': 'negative',
                    'weight': 0.8
                })
                risks.append('Overbought condition (RSI > 70) may lead to price correction')

        # MACD Analysis
        macd_histogram = indicators.get('macd_histogram')
        if macd_histogram is not None:
            if macd_histogram > 0:
                score += 1.5
                reasons.append({
                    'category': 'technical',
                    'indicator': 'MACD',
                    'value': 'Bullish',
                    'impact': 'positive',
                    'weight': 0.7
                })
            elif macd_histogram < 0:
                score -= 1.5
                reasons.append({
                    'category': 'technical',
                    'indicator': 'MACD',
                    'value': 'Bearish',
                    'impact': 'negative',
                    'weight': 0.7
                })

        # Moving Average Analysis
        sma_50 = indicators.get('sma_50')
        sma_200 = indicators.get('sma_200')
        if sma_50 is not None and sma_200 is not None:
            if sma_50 > sma_200:
                score += 1
                reasons.append({
                    'category': 'technical',
                    'indicator': 'Moving Average',
                    'value': 'Golden Cross',
                    'impact': 'positive',
                    'weight': 0.9
                })
            elif sma_50 < sma_200:
                score -= 1
                reasons.append({
                    'category': 'technical',
                    'indicator': 'Moving Average',
                    'value': 'Death Cross',
                    'impact': 'negative',
                    'weight': 0.9
                })
                risks.append('Death Cross pattern indicates bearish trend')

        # Bollinger Bands
        bb_upper = indicators.get('bb_upper')
        bb_lower = indicators.get('bb_lower')
        current_price = data.get('current_price')

        if all([bb_upper, bb_lower, current_price]):
            if current_price < bb_lower:
                score += 1
                reasons.append({
                    'category': 'technical',
                    'indicator': 'Bollinger Bands',
                    'value': 'Below lower band',
                    'impact': 'positive',
                    'weight': 0.6
                })
            elif current_price > bb_upper:
                score -= 1
                reasons.append({
                    'category': 'technical',
                    'indicator': 'Bollinger Bands',
                    'value': 'Above upper band',
                    'impact': 'negative',
                    'weight': 0.6
                })

        return {'score': score, 'reasons': reasons, 'risks': risks}

    @staticmethod
    def _analyze_fundamental(data: Dict) -> Dict:
        """Analyze fundamental data"""
        score = 0
        reasons = []
        risks = []

        # P/E Ratio Analysis
        pe_ratio = data.get('pe_ratio')
        sector_avg_pe = data.get('sector_avg_pe', 20.0)

        if pe_ratio is not None:
            if pe_ratio < sector_avg_pe * 0.8:
                score += 2
                reasons.append({
                    'category': 'fundamental',
                    'indicator': 'P/E Ratio',
                    'value': f'{pe_ratio:.2f} vs sector {sector_avg_pe:.2f}',
                    'impact': 'positive',
                    'weight': 0.9
                })
            elif pe_ratio > sector_avg_pe * 1.5:
                score -= 1
                reasons.append({
                    'category': 'fundamental',
                    'indicator': 'P/E Ratio',
                    'value': f'{pe_ratio:.2f} vs sector {sector_avg_pe:.2f}',
                    'impact': 'negative',
                    'weight': 0.9
                })
                risks.append(f'High P/E ratio ({pe_ratio:.2f}) indicates potential overvaluation')

        # Dividend Yield
        dividend_yield = data.get('dividend_yield')
        if dividend_yield is not None and dividend_yield > 0.03:  # > 3%
            score += 1
            reasons.append({
                'category': 'fundamental',
                'indicator': 'Dividend Yield',
                'value': f'{dividend_yield*100:.2f}%',
                'impact': 'positive',
                'weight': 0.7
            })

        # Growth Metrics
        revenue_growth = data.get('revenue_growth')
        earnings_growth = data.get('earnings_growth')

        if revenue_growth is not None and revenue_growth > 0.1:  # > 10%
            score += 1.5
            reasons.append({
                'category': 'fundamental',
                'indicator': 'Revenue Growth',
                'value': f'{revenue_growth*100:.2f}%',
                'impact': 'positive',
                'weight': 0.8
            })

        if earnings_growth is not None and earnings_growth > 0.15:  # > 15%
            score += 1.5
            reasons.append({
                'category': 'fundamental',
                'indicator': 'Earnings Growth',
                'value': f'{earnings_growth*100:.2f}%',
                'impact': 'positive',
                'weight': 0.8
            })
        elif earnings_growth is not None and earnings_growth < -0.1:  # < -10%
            score -= 2
            reasons.append({
                'category': 'fundamental',
                'indicator': 'Earnings Growth',
                'value': f'{earnings_growth*100:.2f}%',
                'impact': 'negative',
                'weight': 0.8
            })
            risks.append('Negative earnings growth indicates declining profitability')

        # Debt to Equity
        debt_to_equity = data.get('debt_to_equity')
        if debt_to_equity is not None:
            if debt_to_equity > 2.0:
                score -= 1
                risks.append(f'High debt-to-equity ratio ({debt_to_equity:.2f}) increases financial risk')

        # ROE (Return on Equity)
        roe = data.get('return_on_equity')
        if roe is not None and roe > 0.15:  # > 15%
            score += 1
            reasons.append({
                'category': 'fundamental',
                'indicator': 'ROE',
                'value': f'{roe*100:.2f}%',
                'impact': 'positive',
                'weight': 0.7
            })

        return {'score': score, 'reasons': reasons, 'risks': risks}

    @staticmethod
    def _analyze_sentiment(data: Dict) -> Dict:
        """Analyze sentiment data"""
        score = 0
        reasons = []

        avg_sentiment = data.get('average_score', 0)
        overall_sentiment = data.get('overall_sentiment', 'neutral')

        if overall_sentiment == 'positive':
            score += 1.5
            reasons.append({
                'category': 'sentiment',
                'indicator': 'News Sentiment',
                'value': f'{avg_sentiment:.2f} (Positive)',
                'impact': 'positive',
                'weight': 0.6
            })
        elif overall_sentiment == 'negative':
            score -= 1.5
            reasons.append({
                'category': 'sentiment',
                'indicator': 'News Sentiment',
                'value': f'{avg_sentiment:.2f} (Negative)',
                'impact': 'negative',
                'weight': 0.6
            })

        return {'score': score, 'reasons': reasons, 'risks': []}

    @staticmethod
    def _determine_action(score: float, timeframe: Timeframe) -> tuple[RecommendationAction, float]:
        """Determine recommendation action based on score"""
        # Adjust thresholds based on timeframe
        if timeframe == Timeframe.SHORT:
            # More aggressive thresholds for short-term
            if score >= 4:
                return RecommendationAction.STRONG_BUY, 0.9
            elif score >= 2:
                return RecommendationAction.BUY, 0.75
            elif score <= -4:
                return RecommendationAction.STRONG_SELL, 0.9
            elif score <= -2:
                return RecommendationAction.SELL, 0.75
            else:
                return RecommendationAction.HOLD, 0.5
        else:
            # More conservative for mid and long-term
            if score >= 5:
                return RecommendationAction.STRONG_BUY, 0.85
            elif score >= 2.5:
                return RecommendationAction.BUY, 0.7
            elif score <= -5:
                return RecommendationAction.STRONG_SELL, 0.85
            elif score <= -2.5:
                return RecommendationAction.SELL, 0.7
            else:
                return RecommendationAction.HOLD, 0.6

    @staticmethod
    def _calculate_target_price(
        current_price: float,
        score: float,
        timeframe: Timeframe
    ) -> Optional[float]:
        """Calculate target price based on score and timeframe"""
        if score == 0:
            return None

        # Target price growth based on timeframe
        if timeframe == Timeframe.SHORT:
            max_change = 0.15  # 15% max change for short-term
        elif timeframe == Timeframe.MID:
            max_change = 0.30  # 30% max change for mid-term
        else:
            max_change = 0.50  # 50% max change for long-term

        # Normalize score to -1 to 1 range
        normalized_score = max(min(score / 10, 1), -1)

        # Calculate target price
        price_change = current_price * (normalized_score * max_change)
        target_price = current_price + price_change

        return round(target_price, 2)

    @staticmethod
    def _generate_summary(
        action: RecommendationAction,
        timeframe: Timeframe,
        tech_score: float,
        fund_score: float,
        sent_score: float
    ) -> str:
        """Generate human-readable summary"""
        timeframe_text = {
            Timeframe.SHORT: 'kurzfristig (1-4 Wochen)',
            Timeframe.MID: 'mittelfristig (1-6 Monate)',
            Timeframe.LONG: 'langfristig (6+ Monate)'
        }

        action_text = {
            RecommendationAction.STRONG_BUY: 'starkes Kaufsignal',
            RecommendationAction.BUY: 'Kaufsignal',
            RecommendationAction.HOLD: 'Halten-Empfehlung',
            RecommendationAction.SELL: 'Verkaufssignal',
            RecommendationAction.STRONG_SELL: 'starkes Verkaufssignal'
        }

        summary = f"Für einen {timeframe_text[timeframe]} Anlagehorizont ergibt sich ein {action_text[action]}. "

        # Add score breakdown
        if timeframe == Timeframe.SHORT:
            summary += f"Die technische Analyse (Score: {tech_score:.1f}) dominiert die Einschätzung."
        elif timeframe == Timeframe.LONG:
            summary += f"Die Fundamentalanalyse (Score: {fund_score:.1f}) hat das größte Gewicht."
        else:
            summary += f"Technische (Score: {tech_score:.1f}) und fundamentale Analyse (Score: {fund_score:.1f}) werden gleichgewichtet."

        return summary
