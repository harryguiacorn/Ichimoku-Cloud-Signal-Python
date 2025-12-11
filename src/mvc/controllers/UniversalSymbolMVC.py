import logging
import pandas as pd
import requests
import io
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

class Model(object):
    def __init__(self, 
                 url: str, 
                 output_path: str, 
                 match_string: str = "", 
                 read_html_match: str = "",
                 columns_map: Optional[Dict[str, str]] = None,
                 symbol_suffix: str = "",
                 symbol_pad_digits: int = 0):
        self.url = url
        self.output_path = output_path
        self.match_string = match_string
        self.read_html_match = read_html_match
        self.columns_map = columns_map or {}
        self.symbol_suffix = symbol_suffix
        self.symbol_pad_digits = symbol_pad_digits
        self.df_list = None
        self.df = pd.DataFrame()

    def readHtml(self):
        logger.info(f"Reading symbols from source: {self.url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Use io.StringIO to avoid FutureWarning
            html_content = io.StringIO(response.text)
            
            # Use read_html_match if provided, otherwise just read all
            match_arg = self.read_html_match if self.read_html_match else ".+"
            tables = pd.read_html(html_content, match=match_arg)
            
            if not tables:
                raise ValueError("No tables found in response")

            # Heuristic to find the best table if multiple returned
            # 1. If match_string provided, look for it in columns
            # 2. Look for 'Symbol' or 'Ticker'
            selected_table = None
            
            for i, df in enumerate(tables):
                cols_str = " ".join([str(c) for c in df.columns]).lower()
                if self.match_string and self.match_string.lower() in cols_str:
                    selected_table = df
                    break
                
                # Fallback heuristics
                if 'symbol' in cols_str or 'ticker' in cols_str:
                    selected_table = df
                    # Don't break yet, might find a better match if match_string was not used
                    if not self.match_string:
                        break
            
            if selected_table is None:
                selected_table = tables[0]
                logger.warning("No specific table matched criteria, defaulting to first table.")

            self.df_list = selected_table
            logger.info(f"Table found with {len(self.df_list)} rows.")
            return self.df_list

        except Exception as e:
            logger.exception(f"Error reading HTML: {e}")
            raise

    def cleanData(self):
        if self.df_list is None:
            return

        self.df = self.df_list.copy()
        
        # Flatten MultiIndex columns if present
        if isinstance(self.df.columns, pd.MultiIndex):
             self.df.columns = [' '.join(map(str, col)).strip() for col in self.df.columns.values]

        # Normalize columns
        # 1. Apply user map
        if self.columns_map:
            self.df.rename(columns=self.columns_map, inplace=True)
        
        # 2. Auto-detect common names if not mapped
        # Create a map of lower-case column names to actual column names
        cols_map_lower = {str(c).lower(): c for c in self.df.columns}
        
        # Helper to rename if target not exists but source does
        def try_rename(targets, source_candidates):
            for target in targets:
                if target in self.df.columns:
                    return # Target already exists
            
            for candidate in source_candidates:
                if candidate in cols_map_lower:
                    self.df.rename(columns={cols_map_lower[candidate]: targets[0]}, inplace=True)
                    return

        try_rename(['symbol'], ['symbol', 'ticker', 'code'])
        try_rename(['name'], ['name', 'company', 'security', 'issue', 'company name', 'security name'])

        # Validation
        if 'symbol' not in self.df.columns:
            logger.error(f"Could not find 'symbol' column. Available: {self.df.columns.tolist()}")
            # Create empty df to prevent further errors
            self.df = pd.DataFrame(columns=['symbol', 'name'])
            return

        # Cleaning
        # Convert to string
        self.df['symbol'] = self.df['symbol'].astype(str)
        
        # Regex extraction (e.g. for HSI "0005.HK")
        self.df['symbol'] = self.df['symbol'].str.replace('.', '-', regex=False)
        
        # Padding (e.g. for HSI 5 -> 0005)
        if self.symbol_pad_digits > 0:
             # Extract digits only
             self.df['symbol'] = self.df['symbol'].str.extract(r'(\d+)')
             self.df['symbol'] = self.df['symbol'].str.zfill(self.symbol_pad_digits)

        # Suffix
        if self.symbol_suffix:
            self.df['symbol'] = self.df['symbol'] + self.symbol_suffix

        # Final check
        self.df = self.df.dropna(subset=['symbol'])
        
        # Ensure name column exists
        if 'name' not in self.df.columns:
            self.df['name'] = self.df['symbol']

    def saveData(self):
        if self.df.empty:
            logger.warning("DataFrame is empty, not saving.")
            return

        columns_to_save = ['symbol', 'name']
        # Filter to only existing columns
        columns_to_save = [c for c in columns_to_save if c in self.df.columns]
        
        logger.info(f"Saving {len(self.df)} symbols to {self.output_path}")
        self.df.to_csv(self.output_path, columns=columns_to_save, index=False)


class View(object):
    pass


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def main(self):
        self.model.readHtml()
        self.model.cleanData()
        self.model.saveData()
