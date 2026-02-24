from back_testing.data import DataLoader
from back_testing.turtle_trading.indicators import IndicatorManager
from back_testing.turtle_trading.strategy import TurtleStrategy
from back_testing.turtle_trading.backtester import Backtester
import numpy as np
import importlib
import back_testing.data

def run_backtest(symbol='MSFT', start_date='2010-01-01', end_date='2022-12-31', 
                 ndays_high=3, ndays_low=3, n_atr=20, sl_mult=1, tp_mult=2):
    """Orchestrates the Turtle Trading System workflow."""
    
    # Reload modules to catch any iterative fixes in Jupyter
    importlib.reload(back_testing.data)
    
    # Initialize components
    loader = DataLoader()
    indicator_manager = IndicatorManager()
    strategy = TurtleStrategy()
    backtester = Backtester()
    
    # Load data
    data = loader.load_local_csv(ticker=symbol, start=start_date, end=end_date)
    
    if data.empty:
        print(f"Warning: No data loaded for {symbol}.")
        return

    print(f"--- Running Turtle Trading Backtest for {symbol} ---")
    print(f"Parameters: High-Channel: {ndays_high}, Low-Channel: {ndays_low}, ATR: {n_atr}")
    print(f"Risk Management: StopLoss: {sl_mult} ATR, TakeProfit: {tp_mult} ATR")
    
    # Step 1: Calculate Indicators (ATR and Channels)
    data = indicator_manager.calculate_atr(data, period=n_atr)
    data = indicator_manager.calculate_channels(data, ndays_high=ndays_high, ndays_low=ndays_low)
    
    # Drop rows where indicators are NaN (initial rolling window)
    data.dropna(subset=['ATR', 'ndays_high', 'ndays_low'], inplace=True)
    
    # Step 2: Generate Signals and Calculate Returns
    data_backtested = strategy.generate_signals(data, sl_mult=sl_mult, tp_mult=tp_mult)
    
    # Step 3: Visualizations
    backtester.plot_results(data_backtested, symbol)
    
    # Step 4: Quantstats Report
    # Use pct_change of close as benchmark
    close_col = 'Close' if 'Close' in data_backtested.columns else 'close'
    benchmark = data_backtested[close_col].pct_change()
    
    backtester.generate_report(data_backtested['trade_ret'], benchmark=benchmark)

if __name__ == "__main__":
    run_backtest()
