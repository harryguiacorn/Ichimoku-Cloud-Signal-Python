#!/usr/bin/env python3
import logging
import argparse
import sys
from datetime import datetime
from pytz import timezone
from dataclasses import dataclass, field
from typing import Optional, Dict

# Ensure src is in path
from scripts import _bootstrap
_bootstrap.ensure_repo_root()

# Import Core MVC classes directly
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

# Import Universal Symbol MVC
from src.mvc.controllers import UniversalSymbolMVC

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w",
)
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
    symbol_columns_map: Optional[Dict[str, str]] = None
    symbol_suffix: str = ""
    symbol_pad_digits: int = 0
    
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

# Market Configurations
MARKET_CONFIGS = {
    "SPX500": MarketConfig(
        symbol_name="SPX500",
        asset_list_path="asset_list/SPX500.csv",
        data_path_root="data/spx500/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks",
        symbol_read_html_match="",
        fetch_1H=True,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=False,
        run_merger=True
    ),
    "DJ30": MarketConfig(
        symbol_name="DowJones30",
        asset_list_path="asset_list/DowJones30.csv",
        data_path_root="data/dowjones30/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components",
        symbol_read_html_match="DJIA component companies",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "FTSE100": MarketConfig(
        symbol_name="FTSE100",
        asset_list_path="asset_list/FTSE100.csv",
        data_path_root="data/ftse100/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/FTSE_100_Index",
        symbol_read_html_match="Company",
        symbol_suffix=".L",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "FTSE250": MarketConfig(
        symbol_name="FTSE250",
        asset_list_path="asset_list/FTSE250.csv",
        data_path_root="data/ftse250/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/FTSE_250_Index",
        symbol_read_html_match="Company",
        symbol_suffix=".L",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "Futures": MarketConfig(
        symbol_name="Futures",
        asset_list_path="asset_list/Futures.csv",
        data_path_root="data/futures/",
        output_path_root="output/cloud/",
        symbol_url="https://finance.yahoo.com/markets/commodities/",
        symbol_read_html_match="",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "CurrencyFutures": MarketConfig(
        symbol_name="FuturesCurrency",
        asset_list_path="asset_list/FuturesCurrency.csv",
        data_path_root="data/futurescurrency/",
        output_path_root="output/cloud/",
        # Currency Futures symbols are hardcoded in the original script or asset list is pre-populated
        symbol_url=None, 
        fetch_1H=True,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "HSI": MarketConfig(
        symbol_name="HSI",
        asset_list_path="asset_list/HSI.csv",
        data_path_root="data/hsi/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/Hang_Seng_Index",
        symbol_read_html_match="Ticker",
        symbol_pad_digits=4,
        symbol_suffix=".HK",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=False,
        run_merger=True
    ),
    "Nas100": MarketConfig(
        symbol_name="Nas100",
        asset_list_path="asset_list/Nasdaq100.csv",
        data_path_root="data/nas100/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/Nasdaq-100",
        symbol_read_html_match="Components",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=True,
        run_kicker=True,
        run_merger=True
    ),
    "Russell1000": MarketConfig(
        symbol_name="Russell1000",
        asset_list_path="asset_list/Russell1000.csv",
        data_path_root="data/russell1000/",
        output_path_root="output/cloud/",
        symbol_url="https://en.wikipedia.org/wiki/Russell_1000_Index",
        symbol_read_html_match="Company",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=False,
        run_merger=True
    ),
    "SPDR_ETFs": MarketConfig(
        symbol_name="SPDR_ETFs",
        asset_list_path="asset_list/SPDR_ETFs.csv",
        data_path_root="data/spdr_etfs/",
        output_path_root="output/cloud/",
        symbol_url=None,
        symbol_read_html_match="Symbol",
        fetch_1H=False,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=True,
        run_merger=True
    ),
    "Kraken": MarketConfig(
        symbol_name="Kraken",
        asset_list_path="asset_list/Kraken.csv",
        data_path_root="data/kraken/",
        output_path_root="output/cloud/",
        symbol_url=None,
        fetch_1H=True,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=False,
        run_merger=True
    ),
    "Oanda": MarketConfig(
        symbol_name="Oanda",
        asset_list_path="asset_list/Oanda.csv",
        data_path_root="data/oanda/",
        output_path_root="output/cloud/",
        symbol_url=None,
        fetch_1H=True,
        fetch_D=True,
        fetch_W=True,
        fetch_M=True,
        run_cloud=True,
        run_tkx=True,
        run_kijun=False,
        run_kicker=False,
        run_merger=True
    ),
}

def run_pipeline(config: MarketConfig):
    logger.info(f"Starting pipeline for {config.symbol_name}")
    
    # ---------------------------------------------------------
    # Step 1: Fetch Symbols
    # ---------------------------------------------------------
    if config.symbol_url:
        logger.info("Step 1: Fetching Symbols...")
        model = UniversalSymbolMVC.Model(
            url=config.symbol_url,
            output_path=config.asset_list_path,
            match_string=config.symbol_match,
            read_html_match=config.symbol_read_html_match,
            columns_map=config.symbol_columns_map,
            symbol_suffix=config.symbol_suffix,
            symbol_pad_digits=config.symbol_pad_digits
        )
        UniversalSymbolMVC.Control(model, UniversalSymbolMVC.View()).main()
    else:
        logger.info("Step 1: Skipping Symbol Fetch (No URL provided)")

    # ---------------------------------------------------------
    # Step 2: Fetch OHLC Data
    # ---------------------------------------------------------
    logger.info("Step 2: Fetching OHLC Data...")
    if config.fetch_1H:
        model = DataPandasModel(f"{config.data_path_root}1h/", config.asset_list_path, "1h", "1y", True)
        DataPandasControl(model, DataPandasView()).main()
    if config.fetch_D:
        model = DataPandasModel(f"{config.data_path_root}d/", config.asset_list_path, "1d", "max", True)
        DataPandasControl(model, DataPandasView()).main()
    if config.fetch_W:
        model = DataPandasModel(f"{config.data_path_root}w/", config.asset_list_path, "1wk", "max", True)
        DataPandasControl(model, DataPandasView()).main()
    if config.fetch_M:
        model = DataPandasModel(f"{config.data_path_root}m/", config.asset_list_path, "1mo", "max", True)
        DataPandasControl(model, DataPandasView()).main()

    # ---------------------------------------------------------
    # Step 3: Cloud Analysis
    # ---------------------------------------------------------
    if config.run_cloud:
        logger.info("Step 3: Processing Ichimoku Cloud Data...")
        # 3.1 Calculate
        if config.fetch_1H:
            CloudControl(CloudModel(f"{config.data_path_root}1h/", config.asset_list_path, True), CloudView()).main()
        if config.fetch_D:
            CloudControl(CloudModel(f"{config.data_path_root}d/", config.asset_list_path), CloudView()).main()
        if config.fetch_W:
            CloudControl(CloudModel(f"{config.data_path_root}w/", config.asset_list_path), CloudView()).main()
        if config.fetch_M:
            CloudControl(CloudModel(f"{config.data_path_root}m/", config.asset_list_path), CloudView()).main()

        # 3.2 Aggregate
        name = config.symbol_name
        output_root = config.output_path_root
        
        if config.fetch_1H:
            CloudAggControl(CloudAggModel(f"{config.data_path_root}1h/", config.asset_list_path, output_root, f"{name}-cloud-1H", "1H", True), CloudAggView()).main()
        if config.fetch_D:
            CloudAggControl(CloudAggModel(f"{config.data_path_root}d/", config.asset_list_path, output_root, f"{name}-cloud-D", "1D"), CloudAggView()).main()
        if config.fetch_W:
            CloudAggControl(CloudAggModel(f"{config.data_path_root}w/", config.asset_list_path, output_root, f"{name}-cloud-W", "1W"), CloudAggView()).main()
        if config.fetch_M:
            CloudAggControl(CloudAggModel(f"{config.data_path_root}m/", config.asset_list_path, output_root, f"{name}-cloud-M", "1M"), CloudAggView()).main()

        # 3.3 Merge
        if config.run_merger:
            files = []
            cols = []
            scores = []
            
            if config.fetch_1H:
                files.append(f"{output_root}{name}-cloud-1H.csv")
                cols.append(["1H Cloud Direction", "1H Cloud Count"])
                scores.append("1H Cloud Score")
            if config.fetch_D:
                files.append(f"{output_root}{name}-cloud-D.csv")
                cols.append(["1D Cloud Direction", "1D Cloud Count"])
                scores.append("1D Cloud Score")
            if config.fetch_W:
                files.append(f"{output_root}{name}-cloud-W.csv")
                cols.append(["1W Cloud Direction", "1W Cloud Count"])
                scores.append("1W Cloud Score")
            if config.fetch_M:
                files.append(f"{output_root}{name}-cloud-M.csv")
                cols.append(["1M Cloud Direction", "1M Cloud Count"])
                scores.append("1M Cloud Score")
            
            scores.append("Cloud Score Sum")
            
            if files:
                CloudMergerControl(CloudMergerModel(files, f"{output_root}{name}-cloud-merged.csv", cols, scores), CloudMergerView()).main()

    # ---------------------------------------------------------
    # Step 4: TKx Analysis
    # ---------------------------------------------------------
    if config.run_tkx:
        logger.info("Step 4: Processing TKx Data...")
        # 4.1 Calculate
        if config.fetch_1H:
            TKxControl(TKxModel(f"{config.data_path_root}1h/", config.asset_list_path, True), TKxView()).main()
        if config.fetch_D:
            TKxControl(TKxModel(f"{config.data_path_root}d/", config.asset_list_path), TKxView()).main()
        if config.fetch_W:
            TKxControl(TKxModel(f"{config.data_path_root}w/", config.asset_list_path), TKxView()).main()
        if config.fetch_M:
            TKxControl(TKxModel(f"{config.data_path_root}m/", config.asset_list_path), TKxView()).main()

        # 4.2 Aggregate
        name = config.symbol_name
        output_root = config.output_path_root
        
        if config.fetch_1H:
            TKxAggControl(TKxAggModel(f"{config.data_path_root}1h/", config.asset_list_path, output_root, f"{name}-tkx-1H", "1H", True), TKxAggView()).main()
        if config.fetch_D:
            TKxAggControl(TKxAggModel(f"{config.data_path_root}d/", config.asset_list_path, output_root, f"{name}-tkx-D", "1D"), TKxAggView()).main()
        if config.fetch_W:
            TKxAggControl(TKxAggModel(f"{config.data_path_root}w/", config.asset_list_path, output_root, f"{name}-tkx-W", "1W"), TKxAggView()).main()
        if config.fetch_M:
            TKxAggControl(TKxAggModel(f"{config.data_path_root}m/", config.asset_list_path, output_root, f"{name}-tkx-M", "1M"), TKxAggView()).main()

        # 4.3 Merge
        if config.run_merger:
            files = []
            cols = []
            scores = []
            
            if config.fetch_1H:
                files.append(f"{output_root}{name}-tkx-1H.csv")
                cols.append(["1H TKx Direction", "1H TKx Count"])
                scores.append("1H TKx Score")
            if config.fetch_D:
                files.append(f"{output_root}{name}-tkx-D.csv")
                cols.append(["1D TKx Direction", "1D TKx Count"])
                scores.append("1D TKx Score")
            if config.fetch_W:
                files.append(f"{output_root}{name}-tkx-W.csv")
                cols.append(["1W TKx Direction", "1W TKx Count"])
                scores.append("1W TKx Score")
            if config.fetch_M:
                files.append(f"{output_root}{name}-tkx-M.csv")
                cols.append(["1M TKx Direction", "1M TKx Count"])
                scores.append("1M TKx Score")
            
            scores.append("TKx Score Sum")
            
            if files:
                TKxMergerControl(TKxMergerModel(files, f"{output_root}{name}-tkx-merged.csv", cols, scores), TKxMergerView()).main()

    # ---------------------------------------------------------
    # Step 5: Sum Cloud & TKx Merger
    # ---------------------------------------------------------
    if config.run_cloud and config.run_tkx and config.run_merger:
        logger.info("Step 5: Processing Sum Cloud & TKx Merger...")
        name = config.symbol_name
        output_root = config.output_path_root
        
        files = [
            f"{output_root}{name}-cloud-merged.csv",
            f"{output_root}{name}-tkx-merged.csv"
        ]
        output = f"{output_root}{name}-cloud-tkx-merged.csv"
        
        SumMergerControl(
            SumMergerModel(
                files, 
                output,
                ["Cloud Score Sum", "TKx Score Sum"],
                ["Total Score Sum"]
            ), 
            SumMergerView()
        ).main()

    # ---------------------------------------------------------
    # Step 6: Kijun Analysis
    # ---------------------------------------------------------
    if config.run_kijun:
        logger.info("Step 6: Processing Kijun Data...")
        # 6.1 Calculate
        if config.fetch_1H:
            KijunControl(KijunModel(f"{config.data_path_root}1h/", config.asset_list_path, True), KijunView()).main()
        if config.fetch_D:
            KijunControl(KijunModel(f"{config.data_path_root}d/", config.asset_list_path), KijunView()).main()
        if config.fetch_W:
            KijunControl(KijunModel(f"{config.data_path_root}w/", config.asset_list_path), KijunView()).main()
        if config.fetch_M:
            KijunControl(KijunModel(f"{config.data_path_root}m/", config.asset_list_path), KijunView()).main()

        # 6.2 Aggregate
        name = config.symbol_name
        output_root = config.output_path_root
        
        if config.fetch_1H:
            KijunAggControl(KijunAggModel(f"{config.data_path_root}1h/", config.asset_list_path, output_root, f"{name}-kijun-1H", "1H", True), KijunAggView()).main()
        if config.fetch_D:
            KijunAggControl(KijunAggModel(f"{config.data_path_root}d/", config.asset_list_path, output_root, f"{name}-kijun-D", "1D"), KijunAggView()).main()
        if config.fetch_W:
            KijunAggControl(KijunAggModel(f"{config.data_path_root}w/", config.asset_list_path, output_root, f"{name}-kijun-W", "1W"), KijunAggView()).main()
        if config.fetch_M:
            KijunAggControl(KijunAggModel(f"{config.data_path_root}m/", config.asset_list_path, output_root, f"{name}-kijun-M", "1M"), KijunAggView()).main()

    # ---------------------------------------------------------
    # Step 7: Kicker Analysis
    # ---------------------------------------------------------
    if config.run_kicker:
        logger.info("Step 7: Processing Kicker Data...")
        # 7.1 Calculate
        if config.fetch_D:
            KickerControl(KickerModel(f"{config.data_path_root}d/", config.asset_list_path), KickerView()).main()
        if config.fetch_W:
            KickerControl(KickerModel(f"{config.data_path_root}w/", config.asset_list_path), KickerView()).main()
        if config.fetch_M:
            KickerControl(KickerModel(f"{config.data_path_root}m/", config.asset_list_path), KickerView()).main()

        # 7.2 Aggregate
        name = config.symbol_name
        output_root = config.output_path_root
        
        if config.fetch_D:
            KickerAggControl(KickerAggModel(f"{config.data_path_root}d/", config.asset_list_path, output_root, f"{name}-kicker-D"), KickerAggView()).main()
        if config.fetch_W:
            KickerAggControl(KickerAggModel(f"{config.data_path_root}w/", config.asset_list_path, output_root, f"{name}-kicker-W"), KickerAggView()).main()
        if config.fetch_M:
            KickerAggControl(KickerAggModel(f"{config.data_path_root}m/", config.asset_list_path, output_root, f"{name}-kicker-M"), KickerAggView()).main()


def main():
    parser = argparse.ArgumentParser(description="Run Cloud Signal Analysis for a specific market.")
    parser.add_argument("--market", type=str, required=True, help="Market name (e.g., SPX500, DJ30)")
    args = parser.parse_args()

    market_name = args.market
    if market_name not in MARKET_CONFIGS:
        logger.error(f"Unknown market: {market_name}. Available markets: {list(MARKET_CONFIGS.keys())}")
        sys.exit(1)

    config = MARKET_CONFIGS[market_name]
    
    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{market_name} task begins at: {time_start_formatted} [UK]")

    run_pipeline(config)

    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        f"{market_name} tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})"
    )

if __name__ == "__main__":
    main()
