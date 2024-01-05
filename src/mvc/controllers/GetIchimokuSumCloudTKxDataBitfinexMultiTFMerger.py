from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/Bitfinex-cloud-merged.csv",
                "output/tkx/Bitfinex-tkx-merged.csv",
            ],
            "output/sum/Bitfinex-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "Cloud and TKx Scanner Dashboard - Bitfinex Instruments ",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
