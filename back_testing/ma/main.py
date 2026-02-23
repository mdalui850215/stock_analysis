from back_testing.ma.indicators import IndicatorManager
from back_testing.ma.strategy import MovingAverageStrategy
from back_testing.ma.backtester import Backtester
from back_testing.ma.optimizer import Optimizer
import numpy as np
import importlib
import back_testing.data
importlib.reload(back_testing.data)
from back_testing.data import DataLoader
import quantstats as qs

def run_backtest(symbol='NSEI', start_date='2001-01-01', end_date='2025-12-31', sma=20, mma=40, lma=80, optimize=False):
    """Orchestrates the backtesting and optimization workflow."""
    
    # Initialize components
    loader = DataLoader()
    indicator_manager = IndicatorManager()
    strategy = MovingAverageStrategy()
    backtester = Backtester()
    
    # Load data
    data = loader.load_local_csv(ticker=symbol, start=start_date, end=end_date)
    data = loader.generate_returns(data)
    
    # Simple Backtest
    print(f"--- Running Initial Backtest for {symbol} ---")
    data_backtested = indicator_manager.apply_mas(data, sma, mma, lma)
    data_backtested = strategy.generate_signals(data_backtested)
    
    bnh, s_returns = backtester.calculate_metrics(data_backtested)
    print(f'Buy and hold returns: {np.round(bnh, 2)}')
    print(f'Strategy returns: {np.round(s_returns, 2)}')
    
    # Generate full report using daily returns series and benchmark
    qs.reports.full(data_backtested['strategy_returns'], benchmark=data_backtested['p_returns'])

    # Plot results
    print(f"\nDisplaying chart for {symbol}...")
    backtester.plot_results(data_backtested)
    
    # Optimization
    if optimize:
        print("\n--- Starting Parameter Optimization ---")
        # Sample optimization ranges
        sma_range = range(30, 40, 5)
        mma_range = range(60, 75, 5)
        lma_range = range(100, 115, 5)
        
        optimizer = Optimizer(data)
        optimizer.optimize(sma_range, mma_range, lma_range)

if __name__ == "__main__":
    run_backtest(symbol='NSEI', start_date='2001-01-01', end_date='2020-12-31', sma=20, mma=40, lma=80, optimize=True)
