"""Technical analysis service for calculating indicators"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
from datetime import datetime


class TechnicalAnalysisService:
    """Service for calculating technical indicators"""

    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average

        Args:
            data: Price data series
            period: Period for SMA calculation

        Returns:
            SMA series
        """
        return data.rolling(window=period, min_periods=period).mean()

    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average

        Args:
            data: Price data series
            period: Period for EMA calculation

        Returns:
            EMA series
        """
        return data.ewm(span=period, adjust=False, min_periods=period).mean()

    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index

        Args:
            data: Price data series
            period: Period for RSI calculation (default: 14)

        Returns:
            RSI series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_macd(
        data: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Args:
            data: Price data series
            fast_period: Fast EMA period (default: 12)
            slow_period: Slow EMA period (default: 26)
            signal_period: Signal line period (default: 9)

        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        fast_ema = TechnicalAnalysisService.calculate_ema(data, fast_period)
        slow_ema = TechnicalAnalysisService.calculate_ema(data, slow_period)

        macd_line = fast_ema - slow_ema
        signal_line = TechnicalAnalysisService.calculate_ema(macd_line, signal_period)
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    @staticmethod
    def calculate_bollinger_bands(
        data: pd.Series,
        period: int = 20,
        std_dev: int = 2
    ) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands

        Args:
            data: Price data series
            period: Period for moving average (default: 20)
            std_dev: Number of standard deviations (default: 2)

        Returns:
            Tuple of (Upper band, Middle band, Lower band, Bandwidth)
        """
        middle_band = TechnicalAnalysisService.calculate_sma(data, period)
        std = data.rolling(window=period, min_periods=period).std()

        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        bandwidth = (upper_band - lower_band) / middle_band

        return upper_band, middle_band, lower_band, bandwidth

    @staticmethod
    def calculate_stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        k_period: int = 14,
        d_period: int = 3
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator

        Args:
            high: High price series
            low: Low price series
            close: Close price series
            k_period: Period for %K (default: 14)
            d_period: Period for %D (default: 3)

        Returns:
            Tuple of (%K, %D)
        """
        lowest_low = low.rolling(window=k_period, min_periods=k_period).min()
        highest_high = high.rolling(window=k_period, min_periods=k_period).max()

        stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        stoch_d = stoch_k.rolling(window=d_period, min_periods=d_period).mean()

        return stoch_k, stoch_d

    @staticmethod
    def calculate_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Calculate Average True Range (volatility indicator)

        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: Period for ATR calculation (default: 14)

        Returns:
            ATR series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period, min_periods=period).mean()

        return atr

    @staticmethod
    def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        Calculate On-Balance Volume

        Args:
            close: Close price series
            volume: Volume series

        Returns:
            OBV series
        """
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        return obv

    @staticmethod
    def find_support_resistance(
        prices: pd.Series,
        window: int = 20
    ) -> Tuple[float, float]:
        """
        Find support and resistance levels

        Args:
            prices: Price series
            window: Window for finding levels

        Returns:
            Tuple of (support_level, resistance_level)
        """
        recent_prices = prices.tail(window)
        support = recent_prices.min()
        resistance = recent_prices.max()

        return float(support), float(resistance)

    @staticmethod
    def generate_signals(indicators: Dict) -> List[Dict]:
        """
        Generate trading signals from indicators

        Args:
            indicators: Dictionary of calculated indicators

        Returns:
            List of signal dictionaries
        """
        signals = []

        # RSI signals
        if 'rsi_14' in indicators and indicators['rsi_14'] is not None:
            rsi = indicators['rsi_14']
            if rsi < 30:
                signals.append({
                    'indicator': 'RSI',
                    'signal': 'buy',
                    'value': rsi,
                    'description': f'RSI at {rsi:.2f} indicates oversold condition'
                })
            elif rsi > 70:
                signals.append({
                    'indicator': 'RSI',
                    'signal': 'sell',
                    'value': rsi,
                    'description': f'RSI at {rsi:.2f} indicates overbought condition'
                })
            else:
                signals.append({
                    'indicator': 'RSI',
                    'signal': 'neutral',
                    'value': rsi,
                    'description': f'RSI at {rsi:.2f} is in neutral territory'
                })

        # MACD signals
        if all(k in indicators for k in ['macd', 'macd_signal', 'macd_histogram']):
            macd = indicators['macd']
            signal = indicators['macd_signal']
            histogram = indicators['macd_histogram']

            if histogram > 0 and macd > signal:
                signals.append({
                    'indicator': 'MACD',
                    'signal': 'buy',
                    'value': histogram,
                    'description': 'MACD shows bullish momentum'
                })
            elif histogram < 0 and macd < signal:
                signals.append({
                    'indicator': 'MACD',
                    'signal': 'sell',
                    'value': histogram,
                    'description': 'MACD shows bearish momentum'
                })
            else:
                signals.append({
                    'indicator': 'MACD',
                    'signal': 'neutral',
                    'value': histogram,
                    'description': 'MACD shows neutral momentum'
                })

        # Moving Average signals
        if 'sma_50' in indicators and 'sma_200' in indicators:
            sma_50 = indicators['sma_50']
            sma_200 = indicators['sma_200']

            if sma_50 is not None and sma_200 is not None:
                if sma_50 > sma_200:
                    signals.append({
                        'indicator': 'Moving Average',
                        'signal': 'buy',
                        'value': sma_50 - sma_200,
                        'description': 'Golden Cross: 50-day MA above 200-day MA'
                    })
                elif sma_50 < sma_200:
                    signals.append({
                        'indicator': 'Moving Average',
                        'signal': 'sell',
                        'value': sma_50 - sma_200,
                        'description': 'Death Cross: 50-day MA below 200-day MA'
                    })

        # Bollinger Bands signals
        if all(k in indicators for k in ['bb_upper', 'bb_lower']):
            # This would need current price to be passed in
            pass

        return signals

    @staticmethod
    def calculate_overall_score(signals: List[Dict]) -> Tuple[int, str]:
        """
        Calculate overall technical score from signals

        Args:
            signals: List of signal dictionaries

        Returns:
            Tuple of (score, overall_signal)
        """
        score = 0

        for signal in signals:
            if signal['signal'] == 'buy':
                score += 1
            elif signal['signal'] == 'sell':
                score -= 1

        # Determine overall signal
        if score >= 3:
            overall_signal = 'strong_buy'
        elif score >= 1:
            overall_signal = 'buy'
        elif score <= -3:
            overall_signal = 'strong_sell'
        elif score <= -1:
            overall_signal = 'sell'
        else:
            overall_signal = 'neutral'

        return score, overall_signal

    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all technical indicators for a dataframe

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with all indicators added
        """
        # Ensure we have the required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")

        # Moving Averages
        df['sma_20'] = TechnicalAnalysisService.calculate_sma(df['close'], 20)
        df['sma_50'] = TechnicalAnalysisService.calculate_sma(df['close'], 50)
        df['sma_200'] = TechnicalAnalysisService.calculate_sma(df['close'], 200)
        df['ema_12'] = TechnicalAnalysisService.calculate_ema(df['close'], 12)
        df['ema_26'] = TechnicalAnalysisService.calculate_ema(df['close'], 26)

        # RSI
        df['rsi_14'] = TechnicalAnalysisService.calculate_rsi(df['close'], 14)

        # MACD
        macd, signal, histogram = TechnicalAnalysisService.calculate_macd(df['close'])
        df['macd'] = macd
        df['macd_signal'] = signal
        df['macd_histogram'] = histogram

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower, bb_bandwidth = TechnicalAnalysisService.calculate_bollinger_bands(df['close'])
        df['bb_upper'] = bb_upper
        df['bb_middle'] = bb_middle
        df['bb_lower'] = bb_lower
        df['bb_bandwidth'] = bb_bandwidth

        # Stochastic
        stoch_k, stoch_d = TechnicalAnalysisService.calculate_stochastic(
            df['high'], df['low'], df['close']
        )
        df['stoch_k'] = stoch_k
        df['stoch_d'] = stoch_d

        # ATR
        df['atr_14'] = TechnicalAnalysisService.calculate_atr(
            df['high'], df['low'], df['close'], 14
        )

        # OBV
        df['obv'] = TechnicalAnalysisService.calculate_obv(df['close'], df['volume'])

        # Volume SMA
        df['volume_sma_20'] = TechnicalAnalysisService.calculate_sma(df['volume'], 20)

        return df
