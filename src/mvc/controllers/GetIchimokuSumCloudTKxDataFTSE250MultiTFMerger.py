from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/FTSE250-cloud-merged.csv",
                "output/tkx/FTSE250-tkx-merged.csv",
            ],
            "output/sum/FTSE250-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "FTSE250 Cloud and TKx score page",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
