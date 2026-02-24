from back_testing.data import DataLoader
from back_testing.high_low_price.indicators import IndicatorManager
from back_testing.high_low_price.strategy import HighLowStrategy
from back_testing.high_low_price.backtester import Backtester
import numpy as np
import importlib
import back_testing.data

def run_backtest(symbol='MSFT', start_date='2010-01-01', end_date='2022-12-31', 
                 ndays_high=20, ndays_low=20):
    """Orchestrates the High/Low Price strategy workflow."""
    
    # Reload modules for Jupyter iterative development
    importlib.reload(back_testing.data)
    
    # Initialize components
    loader = DataLoader()
    indicator_manager = IndicatorManager()
    strategy = HighLowStrategy()
    backtester = Backtester()
    
    # Load data
    data = loader.load_local_csv(ticker=symbol, start=start_date, end=end_date)
    
    if data.empty:
        print(f"Warning: No data loaded for {symbol}.")
        return

    print(f"--- Running High/Low Strategy Backtest for {symbol} ---")
    print(f"Parameters: Entry (High) Period: {ndays_high}, Exit (Low) Period: {ndays_low}")
    
    # Step 1: Calculate Indicators
    data = indicator_manager.calculate_channels(data, ndays_high=ndays_high, ndays_low=ndays_low)
    
    # Step 2: Generate Signals
    data_backtested = strategy.generate_signals(data)
    
    # Step 3: Visualizations
    backtester.plot_results(data_backtested, symbol)
    
    # Step 4: Quantstats Report
    close_col = 'Close' if 'Close' in data_backtested.columns else 'close'
    benchmark = data_backtested[close_col].pct_change()
    
    backtester.generate_report(data_backtested['trade_ret'], benchmark=benchmark)

if __name__ == "__main__":
    run_backtest()
