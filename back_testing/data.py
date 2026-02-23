import pandas as pd
import numpy as np
import os

class DataLoader:
    """Handles downloading and initial processing of stock data."""
    
    @staticmethod
    def load_local_csv(ticker='MSFT', start=None, end=None):
        """Reads data from a local CSV file instead of downloading."""
        print(f"\n--- Data Loading for: {ticker} ---")
        print(f"Requested Range: {start} to {end}")
        
        file_path = os.path.join("data", "historical_data13081.csv")
        try:
            # col 1 is 'timestamp' based on file inspection
            df = pd.read_csv(file_path, index_col=1, parse_dates=True)
            
            # Remove redundant index column if present
            if 'Unnamed: 0' in df.columns:
                df.drop(columns=['Unnamed: 0'], inplace=True)
            
            # FORCE CHRONOLOGICAL ORDER (Earliest to Latest)
            df.sort_index(ascending=True, inplace=True)
            
            # Standardize 'Close' column name
            if 'close' in df.columns:
                df.rename(columns={'close': 'Close'}, inplace=True)
            
            # Log available range before filtering
            print(f"File availability: {df.index.min().date()} to {df.index.max().date()}")
            
            # Filter by date range
            if start:
                df = df[df.index >= pd.to_datetime(start)]
            if end:
                df = df[df.index <= pd.to_datetime(end)]

            print(f"Final loaded range: {df.index.min().date()} to {df.index.max().date()}")
            print(f"Total rows loaded: {len(df)}")
            return df
        except Exception as e:
            print(f"Error loading data from CSV: {e}")
            return pd.DataFrame()

    @staticmethod
    def generate_returns(df):
        """Calculates percentage returns for the 'Close' column."""
        if df is None or df.empty:
            return df
        df = df.copy()
        if 'Close' in df.columns:
            df['p_returns'] = df['Close'].pct_change()
        return df
