from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMergerWithList import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        # ----- XLC - Communication Services -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlc.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLC-sum-cloud-tkx-merged.csv",
            "XLC - Communication Services",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLY - Consumer Discretionary -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlc.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLY-sum-cloud-tkx-merged.csv",
            "XLY - Consumer Discretionary",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
