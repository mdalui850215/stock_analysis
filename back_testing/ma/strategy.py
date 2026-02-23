import numpy as np
import pandas as pd

class MovingAverageStrategy:
    """Strategy logic based on three moving averages (SMA, MMA, LMA)."""

    def generate_signals(self, data):
        """Generates buy and sell signals based on conditions for 3 moving averages."""
        df = data.copy()
        df['signal'] = np.nan
        
        # Set the first day signal to zero
        df.loc[df.index[0], 'signal'] = 0.0

        # Loop through each day to compute the signal
        for i in range(1, len(df)):
            # Check if MAs have non-Nan values
            if pd.isna(df['sma'].iloc[i]) or pd.isna(df['mma'].iloc[i]) or pd.isna(df['lma'].iloc[i]):
                df.loc[df.index[i], 'signal'] = 0.0
                continue
            
            # Conditions per moving average
            close_i = df['Close'].iloc[i]
            cond_sma = close_i >= df['sma'].iloc[i]
            cond_mma = close_i >= df['mma'].iloc[i]
            cond_lma = close_i >= df['lma'].iloc[i]
            
            prev_signal = df['signal'].iloc[i-1]
            
            # No current position
            if pd.isna(prev_signal) or prev_signal == 0.0:
                if cond_sma and cond_mma and cond_lma:
                    df.loc[df.index[i], 'signal'] = 1.0  # Go long
                elif not cond_sma and not cond_mma and not cond_lma:
                    df.loc[df.index[i], 'signal'] = -1.0 # Go short
                else:
                    df.loc[df.index[i], 'signal'] = 0.0
            
            # Currently Long
            elif prev_signal == 1.0:
                if not cond_sma or not cond_mma or not cond_lma:
                    df.loc[df.index[i], 'signal'] = 0.0  # Exit long
                else:
                    df.loc[df.index[i], 'signal'] = 1.0  # Hold long
            
            # Currently Short
            elif prev_signal == -1.0:
                if cond_sma or cond_mma or cond_lma:
                    df.loc[df.index[i], 'signal'] = 0.0  # Exit short
                else:
                    df.loc[df.index[i], 'signal'] = -1.0 # Hold short
        
        # Calculate strategy returns
        df['strategy_returns'] = df['p_returns'] * df['signal'].shift(1)
        
        return df
