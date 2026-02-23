import pandas as pd

class IndicatorManager:
    """Calculates various technical indicators for the strategy."""
    
    @staticmethod
    def calculate_sma(df, window):
        """Calculates a Simple Moving Average (SMA) for a given window."""
        return df['Close'].rolling(window=window).mean()
    
    @classmethod
    def apply_mas(cls, df, sma_period, mma_period, lma_period):
        """Calculates SMA, MMA, and LMA and adds them to the dataframe."""
        df = df.copy()
        df['sma'] = cls.calculate_sma(df, sma_period)
        df['mma'] = cls.calculate_sma(df, mma_period)
        df['lma'] = cls.calculate_sma(df, lma_period)
        return df
