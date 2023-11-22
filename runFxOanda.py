from src.mvc.controllers import (
    GetDataForexOanda,
    # GetIchimokuCloudDataForexOanda,
    # GetIchimokuCloudDataForexOandaAggregator,
    # GetIchimokuCloudDataForexOandaMerger,
    # GetIchimokuKijunDataForexOanda,
    # GetIchimokuKijunDataForexOandaAggregator,
    # GetKickerDataForexOanda,
    # GetKickerDataForexOandaAggregator,
)


fetch_symbols_latest = True

fetch_ForexOanda_1H = True

fetch_ForexOanda_4H = True

fetch_ForexOanda_D = True

fetch_ForexOanda_W = False

fetch_ForexOanda_M = False

fetch_Kicker_intraday = False


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Forex Oanda ----------------

    _getDataForexOanda = GetDataForexOanda
    _getDataForexOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )
    return
    _getIchimokuCloudDataForexOanda = GetIchimokuCloudDataForexOanda
    _getIchimokuCloudDataForexOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    _getIchimokuCloudDataForexOandaAggregator = (
        GetIchimokuCloudDataForexOandaAggregator
    )
    _getIchimokuCloudDataForexOandaAggregator.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    _getIchimokuCloudDataForexOandaMerger = (
        GetIchimokuCloudDataForexOandaMerger
    )
    _getIchimokuCloudDataForexOandaMerger.main()

    _getIchimokuKijunDataForexOanda = GetIchimokuKijunDataForexOanda
    _getIchimokuKijunDataForexOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    _getIchimokuKijunDataForexOandaAggregator = (
        GetIchimokuKijunDataForexOandaAggregator
    )
    _getIchimokuKijunDataForexOandaAggregator.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    _getKickerDataForexOanda = GetKickerDataForexOanda
    _getKickerDataForexOanda.main(
        fetch_Kicker_intraday,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    _getKickerDataForexOandaAggregator = GetKickerDataForexOandaAggregator
    _getKickerDataForexOandaAggregator.main(
        fetch_Kicker_intraday,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    print(f"Tasks completed.")


if __name__ == "__main__":
    main()
