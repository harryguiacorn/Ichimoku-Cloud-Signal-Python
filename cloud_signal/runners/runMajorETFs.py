from __future__ import annotations

import logging
from collections.abc import Iterable

from cloud_signal.mvc.core.DataChikouSignalAggregatorMVC import (
    Control as ChikouAggregatorControl,
    Model as ChikouAggregatorModel,
    View as ChikouAggregatorView,
)
from cloud_signal.mvc.core.DataChikouSignalMVC import (
    Control as ChikouSignalControl,
    Model as ChikouSignalModel,
    View as ChikouSignalView,
)
from cloud_signal.mvc.core.DataChikouSignalMultiTimeframeMerger import (
    Control as ChikouMergerControl,
    Model as ChikouMergerModel,
    View as ChikouMergerView,
)
from cloud_signal.mvc.core.DataCloudSignalAggregatorMVC import (
    Control as CloudAggregatorControl,
    Model as CloudAggregatorModel,
    View as CloudAggregatorView,
)
from cloud_signal.mvc.core.DataCloudSignalMVC import (
    Control as CloudSignalControl,
    Model as CloudModel,
    View as CloudSignalView,
)
from cloud_signal.mvc.core.DataCloudSignalMultiTimeframeMerger import (
    Control as CloudMergerControl,
    Model as CloudMergerModel,
    View as CloudMergerView,
)
from cloud_signal.mvc.core.DataPandasMVC import (
    Control as MarketDataControl,
    Model as MarketDataModel,
    View as MarketDataView,
)
from cloud_signal.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control as CombinedMergerControl,
    Model as CombinedMergerModel,
    View as CombinedMergerView,
)
from cloud_signal.mvc.core.DataTKxSignalAggregatorMVC import (
    Control as TKxAggregatorControl,
    Model as TKxAggregatorModel,
    View as TKxAggregatorView,
)
from cloud_signal.mvc.core.DataTKxSignalMVC import (
    Control as TKxSignalControl,
    Model as TKxSignalModel,
    View as TKxSignalView,
)
from cloud_signal.mvc.core.DataTKxSignalMultiTimeframeMerger import (
    Control as TKxMergerControl,
    Model as TKxMergerModel,
    View as TKxMergerView,
)
from cloud_signal.runners._bootstrap import (
    ensure_repo_root,
    setup_runner_logging,
    timed_stage,
)

ensure_repo_root()
setup_runner_logging(__name__, "MajorETFs")
logger = logging.getLogger(__name__)

ASSET_LIST = "asset_list/MajorETFs.csv"
TIMEFRAMES = (
    ("1H", "1h", "1h", "1y", "1H", True),
    ("D", "d", "1d", "max", "1D", False),
    ("W", "w", "1wk", "max", "1W", False),
    ("M", "m", "1mo", "max", "1M", False),
)


def _run_timeframe(suffix, folder, interval, lookback, prefix, use_datetime):
    data_path = f"data/major_etfs/{folder}/"
    data_control = MarketDataControl(
        MarketDataModel(data_path, ASSET_LIST, interval, lookback, True),
        MarketDataView(),
    )
    cloud_signal_control = CloudSignalControl(
        CloudModel(data_path, ASSET_LIST, use_datetime),
        CloudSignalView(),
    )
    tkx_signal_control = TKxSignalControl(
        TKxSignalModel(data_path, ASSET_LIST, use_datetime),
        TKxSignalView(),
    )
    chikou_signal_control = ChikouSignalControl(
        ChikouSignalModel(data_path, ASSET_LIST, use_datetime),
        ChikouSignalView(),
    )

    symbols = data_control.getAssetList()
    with timed_stage(logger, f"{prefix} market data fetch"):
        market_data = data_control.model.getDataOHLC()

    processed_symbols = 0
    with timed_stage(logger, f"{prefix} indicator and signal processing"):
        for symbol in symbols:
            ichimoku_data = data_control.process_data(
                symbol, market_data.get(symbol)
            )
            if ichimoku_data is None:
                continue
            cloud_signal_control.process_dataframe(symbol, ichimoku_data)
            tkx_signal_control.process_dataframe(symbol, ichimoku_data)
            chikou_signal_control.process_dataframe(symbol, ichimoku_data)
            processed_symbols += 1
    logger.info("%s processed %d symbols", prefix, processed_symbols)

    with timed_stage(logger, f"{prefix} signal aggregation"):
        CloudAggregatorControl(
            CloudAggregatorModel(
                data_path,
                ASSET_LIST,
                "output/cloud/",
                f"MajorETFs-cloud-{suffix}",
                prefix,
                use_datetime,
            ),
            CloudAggregatorView(),
        ).main()

        TKxAggregatorControl(
            TKxAggregatorModel(
                data_path,
                ASSET_LIST,
                "output/tkx/",
                f"MajorETFs-tkx-{suffix}",
                prefix,
                use_datetime,
            ),
            TKxAggregatorView(),
        ).main()

        ChikouAggregatorControl(
            ChikouAggregatorModel(
                data_path,
                ASSET_LIST,
                "output/chikou/",
                f"MajorETFs-chikou-{suffix}",
                prefix,
            ),
            ChikouAggregatorView(),
        ).main()


def _merge_cloud_and_tkx():
    cloud_suffixes = [suffix for suffix, *_ in TIMEFRAMES]
    cloud_paths = [
        f"output/cloud/MajorETFs-cloud-{suffix}.csv"
        for suffix in cloud_suffixes
    ]
    tkx_paths = [
        f"output/tkx/MajorETFs-tkx-{suffix}.csv"
        for suffix in cloud_suffixes
    ]
    cloud_labels = [prefix for *_, prefix, _ in TIMEFRAMES]

    CloudMergerControl(
        CloudMergerModel(
            cloud_paths,
            "output/cloud/MajorETFs-cloud-merged.csv",
            [
                [f"{label} Cloud Direction", f"{label} Cloud Count"]
                for label in cloud_labels
            ],
            [f"{label} Cloud Score" for label in cloud_labels]
            + ["Cloud Score Sum"],
        ),
        CloudMergerView(),
    ).main()

    TKxMergerControl(
        TKxMergerModel(
            tkx_paths,
            "output/tkx/MajorETFs-tkx-merged.csv",
            [
                [f"{label} TKx Direction", f"{label} TKx Count"]
                for label in cloud_labels
            ],
            [f"{label} TKx Score" for label in cloud_labels]
            + ["TKx Score Sum"],
        ),
        TKxMergerView(),
    ).main()

    CombinedMergerControl(
        CombinedMergerModel(
            [
                "output/cloud/MajorETFs-cloud-merged.csv",
                "output/tkx/MajorETFs-tkx-merged.csv",
            ],
            "output/sum/MajorETFs-sum-cloud-tkx-merged.csv",
            ["Cloud Score Sum", "TKx Score Sum"],
            ["Total Score Sum"],
            "Major ETFs Cloud Scan",
        ),
        CombinedMergerView(),
    ).main()


def _merge_chikou():
    suffixes = [suffix for suffix, *_ in TIMEFRAMES]
    prefixes = [prefix for *_, prefix, _ in TIMEFRAMES]
    ChikouMergerControl(
        ChikouMergerModel(
            [
                f"output/chikou/MajorETFs-chikou-{suffix}.csv"
                for suffix in suffixes
            ],
            "output/chikou/MajorETFs-chikou-merged.csv",
            [
                [f"{prefix} Chikou Direction", f"{prefix} Chikou Count"]
                for prefix in prefixes
            ],
            ["Chikou Score Sum"],
            "Major ETFs Chikou Scan",
        ),
        ChikouMergerView(),
    ).main()


def main(timeframes: Iterable[str] | None = None):
    logger.info("Major ETFs scan begins")
    selected = _select_timeframes(timeframes)
    for timeframe in selected:
        _run_timeframe(*timeframe)
    if len(selected) == len(TIMEFRAMES):
        with timed_stage(logger, "Major ETFs cloud and TKx merge"):
            _merge_cloud_and_tkx()
        with timed_stage(logger, "Major ETFs Chikou merge"):
            _merge_chikou()
    else:
        logger.info(
            "Skipping multi-timeframe merges because only a subset of "
            "timeframes was selected"
        )
    logger.info("Major ETFs Cloud and Chikou scans completed")


def _select_timeframes(timeframes: Iterable[str] | None):
    if timeframes is None:
        return TIMEFRAMES

    if isinstance(timeframes, str):
        timeframes = [timeframes]
    requested = {timeframe.lower() for timeframe in timeframes}
    available = {timeframe[1].lower() for timeframe in TIMEFRAMES}
    unknown = requested - available
    if unknown:
        raise ValueError(
            f"Unknown Major ETFs timeframe(s): {', '.join(sorted(unknown))}"
        )
    if not requested:
        raise ValueError("At least one timeframe must be selected")
    return tuple(
        timeframe
        for timeframe in TIMEFRAMES
        if timeframe[1].lower() in requested
    )


if __name__ == "__main__":
    main()