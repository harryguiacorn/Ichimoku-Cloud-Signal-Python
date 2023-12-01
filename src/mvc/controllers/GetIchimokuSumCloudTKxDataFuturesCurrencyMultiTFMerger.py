from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FuturesCurrency-cloud-merged.csv",
                "output/FuturesCurrency-tkx-merged.csv",
            ],
            "output/FuturesCurrency-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
