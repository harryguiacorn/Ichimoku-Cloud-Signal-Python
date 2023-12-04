from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/Futures-cloud-merged.csv",
                "output/tkx/Futures-tkx-merged.csv",
            ],
            "output/sum/Futures-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "Futures Cloud and TKx score page",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
