from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/Russell1000-cloud-merged.csv",
                "output/tkx/Russell1000-tkx-merged.csv",
            ],
            "output/sum/Russell1000-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "Russell 1000 Cloud Scan",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
