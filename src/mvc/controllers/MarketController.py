import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

# Import Core MVC classes
from src.mvc.core.DataPandasMVC import Control as DataPandasControl, Model as DataPandasModel, View as DataPandasView
from src.mvc.core.DataCloudSignalMVC import Control as CloudControl, Model as CloudModel, View as CloudView
from src.mvc.core.DataCloudSignalAggregatorMVC import Control as CloudAggControl, Model as CloudAggModel, View as CloudAggView
from src.mvc.core.DataCloudSignalMultiTimeframeMerger import Control as CloudMergerControl, Model as CloudMergerModel, View as CloudMergerView
from src.mvc.core.DataTKxSignalMVC import Control as TKxControl, Model as TKxModel, View as TKxView
from src.mvc.core.DataTKxSignalAggregatorMVC import Control as TKxAggControl, Model as TKxAggModel, View as TKxAggView
from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control as TKxMergerControl, Model as TKxMergerModel, View as TKxMergerView
from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import Control as SumMergerControl, Model as SumMergerModel, View as SumMergerView
from src.mvc.core.DataKijunSignalMVC import Control as KijunControl, Model as KijunModel, View as KijunView
from src.mvc.core.DataKijunSignalAggregatorMVC import Control as KijunAggControl, Model as KijunAggModel, View as KijunAggView
from src.mvc.core.DataKickerSignalMVC import Control as KickerControl, Model as KickerModel, View as KickerView
from src.mvc.core.DataKickerSignalAggregatorMVC import Control as KickerAggControl, Model as KickerAggModel, View as KickerAggView

# Import generic Symbol Fetcher (we will implement a simple one here or import if complex)
import pandas as pd
import requests
import io

logger = logging.getLogger(__name__)

@dataclass
class MarketConfig:
    symbol_name: str
    asset_list_path: str
    data_path_root: str  # e.g. "data/spx500/"
    output_path_root: str # e.g. "output/cloud/"
    
    # Symbol Fetching
    symbol_url: Optional[str] = None
    symbol_match: str = ""
    symbol_read_html_match: str = ""
    
    # Fetch Flags
    fetch_1H: bool = False
    fetch_D: bool = True
    fetch_W: bool = False
    fetch_M: bool = False
    
    # Analysis Flags
    run_cloud: bool = True
    run_tkx: bool = True
    run_kijun: bool = False
    run_kicker: bool = False
    run_merger: bool = True
    
    # Kicker specific
    kicker_use_datetime: bool = False

class MarketController:
    def __init__(self, config: MarketConfig):
        self.config = config

    def fetch_symbols(self):
        if not self.config.symbol_url:
            logger.info("No symbol URL provided, skipping symbol fetch.")
            return

        logger.info(f"Fetching symbols for {self.config.symbol_name} from {self.config.symbol_url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(self.config.symbol_url, headers=headers)
            response.raise_for_status()
            
            # Basic generic parsing logic similar to GetSymbolSPX500
            tables = pd.read_html(io.StringIO(response.text), match=self.config.symbol_read_html_match)
            
            selected_table = None
            # Try to find a table with 'Symbol' or 'Ticker'
            for df in tables:
                cols = [str(c).lower() for c in df.columns]
                if any(x in cols for x in ['symbol', 'ticker']) and any(x in cols for x in ['security', 'company', 'name']):
                    selected_table = df
                    break
            
            if selected_table is None and tables:
                selected_table = tables[0] # Fallback
            
            if selected_table is not None:
                # Normalize columns
                df = selected_table.copy()
                cols_map = {}
                cols_lower = {str(c).lower(): c for c in df.columns}
                
                for k, v in cols_lower.items():
                    if k in ['symbol', 'ticker']:
                        cols_map[v] = 'symbol'
                    elif k in ['security', 'company', 'name']:
                        cols_map[v] = 'name'
                
                df.rename(columns=cols_map, inplace=True)
                
                if 'symbol' in df.columns:
                    df['symbol'] = df['symbol'].astype(str).str.replace('.', '-', regex=False)
                    
                    # Save
                    df.to_csv(self.config.asset_list_path, columns=['symbol', 'name'], index=False)
                    logger.info(f"Saved asset list to {self.config.asset_list_path}")
                else:
                    logger.error("Could not find 'symbol' column in fetched table.")
            else:
                logger.error("No tables found in URL.")

        except Exception as e:
            logger.exception(f"Error fetching symbols: {e}")

    def fetch_ohlc_data(self):
        logger.info("Fetching OHLC Data...")
        # 1H
        if self.config.fetch_1H:
            model = DataPandasModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, "1h", "1y", True)
            DataPandasControl(model, DataPandasView()).main()
        # Daily
        if self.config.fetch_D:
            model = DataPandasModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, "1d", "max", True)
            DataPandasControl(model, DataPandasView()).main()
        # Weekly
        if self.config.fetch_W:
            model = DataPandasModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, "1wk", "max", True)
            DataPandasControl(model, DataPandasView()).main()
        # Monthly
        if self.config.fetch_M:
            model = DataPandasModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, "1mo", "max", True)
            DataPandasControl(model, DataPandasView()).main()

    def process_cloud_data(self):
        logger.info("Processing Ichimoku Cloud Data...")
        # 1. Calculate Cloud Signals
        if self.config.fetch_1H:
            CloudControl(CloudModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, True), CloudView()).main()
        if self.config.fetch_D:
            CloudControl(CloudModel(f"{self.config.data_path_root}d/", self.config.asset_list_path), CloudView()).main()
        if self.config.fetch_W:
            CloudControl(CloudModel(f"{self.config.data_path_root}w/", self.config.asset_list_path), CloudView()).main()
        if self.config.fetch_M:
            CloudControl(CloudModel(f"{self.config.data_path_root}m/", self.config.asset_list_path), CloudView()).main()

        # 2. Aggregate Cloud Signals
        output_root = self.config.output_path_root
        name = self.config.symbol_name
        
        if self.config.fetch_1H:
            CloudAggControl(CloudAggModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, output_root, f"{name}-cloud-1H", "1H", True), CloudAggView()).main()
        if self.config.fetch_D:
            CloudAggControl(CloudAggModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, output_root, f"{name}-cloud-D", "1D"), CloudAggView()).main()
        if self.config.fetch_W:
            CloudAggControl(CloudAggModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, output_root, f"{name}-cloud-W", "1W"), CloudAggView()).main()
        if self.config.fetch_M:
            CloudAggControl(CloudAggModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, output_root, f"{name}-cloud-M", "1M"), CloudAggView()).main()

        # 3. Merge Multi-Timeframe Cloud Signals
        if self.config.run_merger:
            files = []
            cols = []
            scores = []
            
            if self.config.fetch_1H:
                files.append(f"{output_root}{name}-cloud-1H.csv")
                cols.append(["1H Cloud Direction", "1H Cloud Count"])
                scores.append("1H Cloud Score")
            if self.config.fetch_D:
                files.append(f"{output_root}{name}-cloud-D.csv")
                cols.append(["1D Cloud Direction", "1D Cloud Count"])
                scores.append("1D Cloud Score")
            if self.config.fetch_W:
                files.append(f"{output_root}{name}-cloud-W.csv")
                cols.append(["1W Cloud Direction", "1W Cloud Count"])
                scores.append("1W Cloud Score")
            if self.config.fetch_M:
                files.append(f"{output_root}{name}-cloud-M.csv")
                cols.append(["1M Cloud Direction", "1M Cloud Count"])
                scores.append("1M Cloud Score")
            
            scores.append("Cloud Score Sum")
            
            if files:
                CloudMergerControl(CloudMergerModel(files, f"{output_root}{name}-cloud-merged.csv", cols, scores), CloudMergerView()).main()

    def process_tkx_data(self):
        logger.info("Processing TKx Data...")
        # 1. Calculate TKx Signals
        if self.config.fetch_1H:
            TKxControl(TKxModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, True), TKxView()).main()
        if self.config.fetch_D:
            TKxControl(TKxModel(f"{self.config.data_path_root}d/", self.config.asset_list_path), TKxView()).main()
        if self.config.fetch_W:
            TKxControl(TKxModel(f"{self.config.data_path_root}w/", self.config.asset_list_path), TKxView()).main()
        if self.config.fetch_M:
            TKxControl(TKxModel(f"{self.config.data_path_root}m/", self.config.asset_list_path), TKxView()).main()

        # 2. Aggregate TKx Signals
        output_root = self.config.output_path_root
        name = self.config.symbol_name
        
        if self.config.fetch_1H:
            TKxAggControl(TKxAggModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, output_root, f"{name}-tkx-1H", "1H", True), TKxAggView()).main()
        if self.config.fetch_D:
            TKxAggControl(TKxAggModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, output_root, f"{name}-tkx-D", "1D"), TKxAggView()).main()
        if self.config.fetch_W:
            TKxAggControl(TKxAggModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, output_root, f"{name}-tkx-W", "1W"), TKxAggView()).main()
        if self.config.fetch_M:
            TKxAggControl(TKxAggModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, output_root, f"{name}-tkx-M", "1M"), TKxAggView()).main()

        # 3. Merge Multi-Timeframe TKx Signals
        if self.config.run_merger:
            files = []
            cols = []
            scores = []
            
            if self.config.fetch_1H:
                files.append(f"{output_root}{name}-tkx-1H.csv")
                cols.append(["1H TKx Direction", "1H TKx Count"])
                scores.append("1H TKx Score")
            if self.config.fetch_D:
                files.append(f"{output_root}{name}-tkx-D.csv")
                cols.append(["1D TKx Direction", "1D TKx Count"])
                scores.append("1D TKx Score")
            if self.config.fetch_W:
                files.append(f"{output_root}{name}-tkx-W.csv")
                cols.append(["1W TKx Direction", "1W TKx Count"])
                scores.append("1W TKx Score")
            if self.config.fetch_M:
                files.append(f"{output_root}{name}-tkx-M.csv")
                cols.append(["1M TKx Direction", "1M TKx Count"])
                scores.append("1M TKx Score")
            
            scores.append("TKx Score Sum")
            
            if files:
                TKxMergerControl(TKxMergerModel(files, f"{output_root}{name}-tkx-merged.csv", cols, scores), TKxMergerView()).main()

    def process_sum_cloud_tkx_merger(self):
        if not self.config.run_merger:
            return
        
        logger.info("Processing Sum Cloud & TKx Merger...")
        output_root = self.config.output_path_root
        name = self.config.symbol_name
        
        files = [
            f"{output_root}{name}-cloud-merged.csv",
            f"{output_root}{name}-tkx-merged.csv"
        ]
        output = f"{output_root}{name}-cloud-tkx-merged.csv"
        
        # This part might need adjustment based on specific implementation of SumMerger
        # The original code hardcodes columns in the Model init, let's check DataSumCloudTKxSignalMultiTimeframeMerger.py
        # Assuming it takes [cloud_file, tkx_file], output_file
        
        SumMergerControl(SumMergerModel(files, output), SumMergerView()).main()

    def process_kijun_data(self):
        if not self.config.run_kijun:
            return

        logger.info("Processing Kijun Data...")
        # Kijun logic often runs on all timeframes if enabled
        # The original code passed fetch flags to main(), but here we can just check config
        
        # 1. Calculate
        if self.config.fetch_1H:
            KijunControl(KijunModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, True), KijunView()).main()
        if self.config.fetch_D:
            KijunControl(KijunModel(f"{self.config.data_path_root}d/", self.config.asset_list_path), KijunView()).main()
        if self.config.fetch_W:
            KijunControl(KijunModel(f"{self.config.data_path_root}w/", self.config.asset_list_path), KijunView()).main()
        if self.config.fetch_M:
            KijunControl(KijunModel(f"{self.config.data_path_root}m/", self.config.asset_list_path), KijunView()).main()

        # 2. Aggregate
        output_root = self.config.output_path_root
        name = self.config.symbol_name
        
        if self.config.fetch_1H:
            KijunAggControl(KijunAggModel(f"{self.config.data_path_root}1h/", self.config.asset_list_path, output_root, f"{name}-kijun-1H", "1H", True), KijunAggView()).main()
        if self.config.fetch_D:
            KijunAggControl(KijunAggModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, output_root, f"{name}-kijun-D", "1D"), KijunAggView()).main()
        if self.config.fetch_W:
            KijunAggControl(KijunAggModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, output_root, f"{name}-kijun-W", "1W"), KijunAggView()).main()
        if self.config.fetch_M:
            KijunAggControl(KijunAggModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, output_root, f"{name}-kijun-M", "1M"), KijunAggView()).main()

    def process_kicker_data(self):
        if not self.config.run_kicker:
            return
            
        logger.info("Processing Kicker Data...")
        # Kicker usually only on D, W, M
        
        # 1. Calculate
        if self.config.fetch_D:
            KickerControl(KickerModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, self.config.kicker_use_datetime), KickerView()).main()
        if self.config.fetch_W:
            KickerControl(KickerModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, self.config.kicker_use_datetime), KickerView()).main()
        if self.config.fetch_M:
            KickerControl(KickerModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, self.config.kicker_use_datetime), KickerView()).main()

        # 2. Aggregate
        output_root = self.config.output_path_root
        name = self.config.symbol_name
        
        if self.config.fetch_D:
            KickerAggControl(KickerAggModel(f"{self.config.data_path_root}d/", self.config.asset_list_path, output_root, f"{name}-kicker-D", "1D", self.config.kicker_use_datetime), KickerAggView()).main()
        if self.config.fetch_W:
            KickerAggControl(KickerAggModel(f"{self.config.data_path_root}w/", self.config.asset_list_path, output_root, f"{name}-kicker-W", "1W", self.config.kicker_use_datetime), KickerAggView()).main()
        if self.config.fetch_M:
            KickerAggControl(KickerAggModel(f"{self.config.data_path_root}m/", self.config.asset_list_path, output_root, f"{name}-kicker-M", "1M", self.config.kicker_use_datetime), KickerAggView()).main()


    def run(self):
        logger.info(f"Starting pipeline for {self.config.symbol_name}")
        
        # 1. Fetch Symbols
        self.fetch_symbols()
        
        # 2. Fetch OHLC Data
        self.fetch_ohlc_data()
        
        # 3. Cloud Analysis
        if self.config.run_cloud:
            self.process_cloud_data()
            
        # 4. TKx Analysis
        if self.config.run_tkx:
            self.process_tkx_data()
            
        # 5. Sum Cloud & TKx Merger
        if self.config.run_cloud and self.config.run_tkx and self.config.run_merger:
            self.process_sum_cloud_tkx_merger()
            
        # 6. Kijun Analysis
        if self.config.run_kijun:
            self.process_kijun_data()
            
        # 7. Kicker Analysis
        if self.config.run_kicker:
            self.process_kicker_data()
            
        logger.info(f"Pipeline completed for {self.config.symbol_name}")
