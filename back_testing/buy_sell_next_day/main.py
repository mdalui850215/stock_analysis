from back_testing.data import DataLoader
import back_testing.data
import importlib
importlib.reload(back_testing.data)
from back_testing.buy_sell_next_day.indicators import IndicatorManager
from back_testing.buy_sell_next_day.strategy import BuySellNextDayStrategy
from back_testing.buy_sell_next_day.backtester import Backtester
import numpy as np

def run_backtest(symbol='TSLA', start_date='2010-01-01', end_date='2020-03-31', down_days=3, exit_type='next_day_open'):
    """Orchestrates the backtesting workflow for Buy and Sell Next Day."""
    
    # Initialize components
    loader = DataLoader()
    indicator_manager = IndicatorManager()
    strategy = BuySellNextDayStrategy()
    backtester = Backtester()
    
    # Load data
    data = loader.load_local_csv(ticker=symbol, start=start_date, end=end_date)
    
    if data.empty:
        print(f"Warning: No data loaded for {symbol} in the requested date range.")
        return
    
    # Simple Backtest
    print(f"--- Running Buy and Sell Next Day Backtest for {symbol} ---")
    print(f"Parameters: Consecutive Down Days: {down_days}, Exit: {exit_type}")
    
    # Step 1: Calculate Returns
    data = indicator_manager.calculate_returns(data)
    
    # Step 2: Calculate Down Days
    data = indicator_manager.calculate_down_days(data)
    
    # Step 3: Generate Signals
    data = strategy.generate_signals(data, down_days=down_days)
    
    # Step 4: Calculate Strategy Returns
    data = strategy.calculate_strategy_returns(data, exit_type=exit_type)
    
    # Step 5: Calculate and print metrics
    bnh, s_returns = backtester.calculate_metrics(data)
    print(f'Total Buy and Hold (Log) returns: {np.round(bnh, 2)}')
    print(f'Total Strategy (Log) returns: {np.round(s_returns, 2)}')
    
    # Step 6: Generate Full Report using quantstats
    # Strategy returns needs to be passed to quantstats
    backtester.generate_report(data['strategy_returns'], benchmark=data['cc_returns'])

    # Step 7: Plot results
    print(f"Displaying chart for {symbol}...")
    backtester.plot_results(data, symbol)

if __name__ == "__main__":
    # Example execution with the parameters from the user's procedural code
    # Symbol 'TSLA' assumes it's in the data loader, but DataLoader currently filters data based on what's in 'data/historical_data13081.csv'.
    # In actual use, make sure the CSV contains the requested ticker.
    run_backtest(symbol='TSLA', start_date='2010-01-01', end_date='2020-03-31', down_days=3, exit_type='next_day_open')
