from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/FTSE100-cloud-merged.csv",
                "output/tkx/FTSE100-tkx-merged.csv",
            ],
            "output/sum/FTSE100-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "FTSE100 Cloud Scan",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
