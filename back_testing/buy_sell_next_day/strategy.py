import pandas as pd
import numpy as np

class BuySellNextDayStrategy:
    """Strategy: Buy if stock closes down consecutively for N days."""

    def generate_signals(self, data, down_days=3):
        """Generates raw signals based on consecutive down days."""
        df = data.copy()
        
        # Signal is 1 if we had at least 'down_days' consecutive down closes
        # This signal is 'known' at the end of the day.
        df['raw_signal'] = np.where(df['consecutive_down'] >= down_days, 1, 0)
        
        # Shift by 1: we buy at the OPEN of the NEXT day
        df['signal'] = df['raw_signal'].shift(1)
        
        return df

    def calculate_strategy_returns(self, data, exit_type='next_day_open'):
        """
        Calculates strategy returns based on the exit logic.
        exit_type: 'next_day_open' or 'same_day_close'
        """
        df = data.copy()
        
        if exit_type == 'next_day_open':
            # Buy at Open(t), Sell at Open(t+1)
            # Returns are oo_returns(t+1)
            df['strategy_returns'] = df['signal'].shift(1) * df['oo_returns']
        elif exit_type == 'same_day_close':
            # Buy at Open(t), Sell at Close(t)
            # Returns are oc_returns(t)
            df['strategy_returns'] = df['signal'] * df['oc_returns']
        else:
            raise ValueError("exit_type must be 'next_day_open' or 'same_day_close'")
            
        return df
