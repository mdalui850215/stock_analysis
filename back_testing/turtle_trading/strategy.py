import pandas as pd
import numpy as np

class TurtleStrategy:
    """Strategy logic based on N-day breakouts and ATR-based exits."""

    def generate_signals(self, df, sl_mult=1, tp_mult=2):
        """
        Runs the Turtle Trading strategy loop.
        sl_mult: Number of ATRs for Stop Loss.
        tp_mult: Number of ATRs for Take Profit.
        """
        data = df.copy()
        
        # Mapping column names
        cols = {
            'high': 'High' if 'High' in data.columns else 'high',
            'low': 'Low' if 'Low' in data.columns else 'low',
            'close': 'Close' if 'Close' in data.columns else 'close'
        }

        # Initializing columns for state management
        data['position'] = 0.0
        data['trade_price'] = 0.0
        data['trade_ret'] = 0.0
        data['signal'] = ""
        data['SL_price'] = 0.0
        data['TP_price'] = 0.0
        data['rep_ATR'] = 0.0

        n = len(data)

        # Iterative logic for event-driven simulation
        for i in range(1, n):
            prev_pos = data.iloc[i-1]['position']
            curr_high = data.iloc[i][cols['high']]
            curr_low = data.iloc[i][cols['low']]
            curr_close = data.iloc[i][cols['close']]
            
            # CASE: NO POSITION
            if prev_pos == 0.0:
                # Entry long: Price exceeds N-day high
                if curr_high > data.iloc[i]['ndays_high']:
                    data.iloc[i, data.columns.get_loc('position')] = 1.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = data.iloc[i]['ndays_high']
                    data.iloc[i, data.columns.get_loc('signal')] = "Entry long"
                    data.iloc[i, data.columns.get_loc('rep_ATR')] = data.iloc[i]['ATR']
                    # Calculate targets
                    price = data.iloc[i]['trade_price']
                    atr = data.iloc[i]['rep_ATR']
                    data.iloc[i, data.columns.get_loc('SL_price')] = price - (atr * sl_mult)
                    data.iloc[i, data.columns.get_loc('TP_price')] = price + (atr * tp_mult)

                # Entry short: Price falls below N-day low
                elif curr_low < data.iloc[i]['ndays_low']:
                    data.iloc[i, data.columns.get_loc('position')] = -1.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = data.iloc[i]['ndays_low']
                    data.iloc[i, data.columns.get_loc('signal')] = "Entry short"
                    data.iloc[i, data.columns.get_loc('rep_ATR')] = data.iloc[i]['ATR']
                    # Calculate targets
                    price = data.iloc[i]['trade_price']
                    atr = data.iloc[i]['rep_ATR']
                    data.iloc[i, data.columns.get_loc('SL_price')] = price + (atr * sl_mult)
                    data.iloc[i, data.columns.get_loc('TP_price')] = price - (atr * tp_mult)

            # CASE: LONG POSITION
            elif prev_pos == 1.0:
                sl_price = data.iloc[i-1]['SL_price']
                tp_price = data.iloc[i-1]['TP_price']
                
                # Check Stop Loss
                if curr_close <= sl_price:
                    data.iloc[i, data.columns.get_loc('position')] = 0.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = sl_price
                    data.iloc[i, data.columns.get_loc('trade_ret')] = (data.iloc[i]['trade_price'] / data.iloc[i-1]['trade_price']) - 1
                    data.iloc[i, data.columns.get_loc('signal')] = "SL long"
                # Check Take Profit
                elif curr_close >= tp_price:
                    data.iloc[i, data.columns.get_loc('position')] = 0.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = tp_price
                    data.iloc[i, data.columns.get_loc('trade_ret')] = (data.iloc[i]['trade_price'] / data.iloc[i-1]['trade_price']) - 1
                    data.iloc[i, data.columns.get_loc('signal')] = "TP long"
                # Carry Position
                else:
                    data.iloc[i, data.columns.get_loc('position')] = prev_pos
                    data.iloc[i, data.columns.get_loc('trade_price')] = data.iloc[i-1]['trade_price']
                    data.iloc[i, data.columns.get_loc('SL_price')] = sl_price
                    data.iloc[i, data.columns.get_loc('TP_price')] = tp_price
                    data.iloc[i, data.columns.get_loc('signal')] = data.iloc[i-1]['signal']

            # CASE: SHORT POSITION
            elif prev_pos == -1.0:
                sl_price = data.iloc[i-1]['SL_price']
                tp_price = data.iloc[i-1]['TP_price']
                
                # Check Stop Loss
                if curr_close >= sl_price:
                    data.iloc[i, data.columns.get_loc('position')] = 0.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = sl_price
                    # Return for short: (Entry Price / Exit Price) - 1 or exp approach from procedural
                    data.iloc[i, data.columns.get_loc('trade_ret')] = np.exp(np.log(data.iloc[i]['trade_price'] / data.iloc[i-1]['trade_price']) * (-1)) - 1
                    data.iloc[i, data.columns.get_loc('signal')] = "SL short"
                # Check Take Profit
                elif curr_close <= tp_price:
                    data.iloc[i, data.columns.get_loc('position')] = 0.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = tp_price
                    data.iloc[i, data.columns.get_loc('trade_ret')] = np.exp(np.log(data.iloc[i]['trade_price'] / data.iloc[i-1]['trade_price']) * (-1)) - 1
                    data.iloc[i, data.columns.get_loc('signal')] = "TP short"
                # Carry Position
                else:
                    data.iloc[i, data.columns.get_loc('position')] = prev_pos
                    data.iloc[i, data.columns.get_loc('trade_price')] = data.iloc[i-1]['trade_price']
                    data.iloc[i, data.columns.get_loc('SL_price')] = sl_price
                    data.iloc[i, data.columns.get_loc('TP_price')] = tp_price
                    data.iloc[i, data.columns.get_loc('signal')] = data.iloc[i-1]['signal']
        
        return data
