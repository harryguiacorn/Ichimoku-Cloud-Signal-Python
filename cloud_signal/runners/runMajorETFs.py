from __future__ import annotations

import logging

from cloud_signal.mvc.core.DataChikouSignalAggregatorMVC import (
    Control as ChikouAggregatorControl,
    Model as ChikouAggregatorModel,
    View as ChikouAggregatorView,
)
from cloud_signal.mvc.core.DataChikouSignalMVC import (
    Control as ChikouControl,
    Model as ChikouModel,
    View as ChikouView,
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
    Control as CloudControl,
    Model as CloudModel,
    View as CloudView,
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
    Control as TKxControl,
    Model as TKxModel,
    View as TKxView,
)
from cloud_signal.mvc.core.DataTKxSignalMultiTimeframeMerger import (
    Control as TKxMergerControl,
    Model as TKxMergerModel,
    View as TKxMergerView,
)
from cloud_signal.runners._bootstrap import ensure_repo_root, setup_runner_logging

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
    data_control.main()

    CloudControl(CloudModel(data_path, ASSET_LIST, use_datetime), CloudView()).main()
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

    TKxControl(TKxModel(data_path, ASSET_LIST, use_datetime), TKxView()).main()
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

    ChikouControl(ChikouModel(data_path, ASSET_LIST, use_datetime), ChikouView()).main()
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
            [f"output/chikou/MajorETFs-chikou-{suffix}.csv" for suffix in suffixes],
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


def main():
    logger.info("Major ETFs scan begins")
    for timeframe in TIMEFRAMES:
        _run_timeframe(*timeframe)
    _merge_cloud_and_tkx()
    _merge_chikou()
    logger.info("Major ETFs Cloud and Chikou scans completed")


if __name__ == "__main__":
    main()