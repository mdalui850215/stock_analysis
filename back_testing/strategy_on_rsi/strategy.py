import pandas as pd
import numpy as np

class RSIStrategy:
    """Strategy: Buy when RSI < 30. Exit when TP/SL hit or RSI > 70."""

    def generate_signals(self, df, rsi_lower=30, rsi_upper=70, tp_level=0.05, sl_level=0.02):
        """
        Generates buy and sell signals based on RSI and price targets.
        TP_level: Take profit target in percent (e.g. 0.05 for 5%)
        SL_level: Stop loss target in percent (e.g. 0.02 for 2%)
        """
        data = df.copy()
        
        # Check for column names (support both Open/Close/High/Low and open/close/high/low)
        cols = {
            'open': 'Open' if 'Open' in data.columns else 'open',
            'high': 'High' if 'High' in data.columns else 'high',
            'low': 'Low' if 'Low' in data.columns else 'low',
            'close': 'Close' if 'Close' in data.columns else 'close'
        }
        
        # Initializing four new columns for state management
        data['trade_price'] = 0.0
        data['RSI_signal'] = 0.0
        data['take_profit_price'] = 0.0
        data['stop_loss_price'] = 0.0
        
        n = data.shape[0]

        # Ported procedural logic for RSI strategy
        for i in range(1, n): 
            prev_signal = data['RSI_signal'].iloc[i-1]
            
            # Check if we have NO position in the asset
            if prev_signal == 0:
                # Entry condition: Buy if RSI is below lower threshold
                if data['RSI'].iloc[i] <= rsi_lower:
                    data.iloc[i, data.columns.get_loc('RSI_signal')] = 1.0  # Go long
                    data.iloc[i, data.columns.get_loc('trade_price')] = data[cols['close']].iloc[i]
                    data.iloc[i, data.columns.get_loc('take_profit_price')] = data['trade_price'].iloc[i] * (1 + tp_level)
                    data.iloc[i, data.columns.get_loc('stop_loss_price')] = data['trade_price'].iloc[i] * (1 - sl_level)
                else:
                    data.iloc[i, data.columns.get_loc('trade_price')] = data[cols['close']].iloc[i]  
            
            # Check if we have a LONG position
            elif prev_signal == 1:
                # Condition: Breach STOP LOSS
                if data[cols['low']].iloc[i] < data['stop_loss_price'].iloc[i-1]:
                    data.iloc[i, data.columns.get_loc('RSI_signal')] = 0.0  # Exit (SL)
                    data.iloc[i, data.columns.get_loc('trade_price')] = data['stop_loss_price'].iloc[i-1]
                    data.iloc[i, data.columns.get_loc('take_profit_price')] = 0.0
                    data.iloc[i, data.columns.get_loc('stop_loss_price')] = 0.0

                # Condition: Breach TAKE PROFIT
                elif data[cols['high']].iloc[i] > data['take_profit_price'].iloc[i-1]:
                    data.iloc[i, data.columns.get_loc('RSI_signal')] = 0.0  # Exit (TP)
                    data.iloc[i, data.columns.get_loc('trade_price')] = data['take_profit_price'].iloc[i-1]
                    data.iloc[i, data.columns.get_loc('take_profit_price')] = 0.0
                    data.iloc[i, data.columns.get_loc('stop_loss_price')] = 0.0

                # Condition: RSI Exit target (e.g. > 70)
                elif data['RSI'].iloc[i] >= rsi_upper:
                    data.iloc[i, data.columns.get_loc('RSI_signal')] = 0.0  # Exit (RSI Target)
                    data.iloc[i, data.columns.get_loc('trade_price')] = data[cols['close']].iloc[i]
                    data.iloc[i, data.columns.get_loc('take_profit_price')] = 0.0
                    data.iloc[i, data.columns.get_loc('stop_loss_price')] = 0.0

                # Still holding position
                else:
                    data.iloc[i, data.columns.get_loc('RSI_signal')] = data['RSI_signal'].iloc[i-1]
                    data.iloc[i, data.columns.get_loc('trade_price')] = data[cols['close']].iloc[i]
                    data.iloc[i, data.columns.get_loc('take_profit_price')] = data['take_profit_price'].iloc[i-1]
                    data.iloc[i, data.columns.get_loc('stop_loss_price')] = data['stop_loss_price'].iloc[i-1]
        
        # Calculate daily log returns for the strategy
        # Using shift(1) on signal to avoid look-ahead bias
        data['daily_log_returns'] = np.log(data[cols['close']]/data[cols['close']].shift(1))
        data['strategy_returns'] = data['daily_log_returns'] * data['RSI_signal'].shift(1)
        
        # Alternative calculation using trade_price (as in procedural code's last line)
        data['trade_price_returns'] = (np.log(data['trade_price']/data['trade_price'].shift(1)) * data['RSI_signal'].shift(1))
        
        return data
