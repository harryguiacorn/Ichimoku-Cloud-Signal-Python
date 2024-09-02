from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/Kraken-cloud-merged.csv",
                "output/tkx/Kraken-tkx-merged.csv",
            ],
            "output/sum/Kraken-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "Kraken Cloud Scan",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
