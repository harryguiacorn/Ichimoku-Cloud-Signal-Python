from src.mvc.core.DataCloudSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FuturesCurrency-cloud-1H.csv",
                "output/FuturesCurrency-cloud-D.csv",
                "output/FuturesCurrency-cloud-W.csv",
                "output/FuturesCurrency-cloud-M.csv",
            ],
            "output/FuturesCurrency-cloud-merged.csv",
            [
                ["1H Cloud Direction", "1H Cloud Count"],
                ["1D Cloud Direction", "1D Cloud Count"],
                ["1W Cloud Direction", "1W Cloud Count"],
                ["1M Cloud Direction", "1M Cloud Count"],
            ],
            [
                "1H Cloud Score",
                "1D Cloud Score",
                "1W Cloud Score",
                "1M Cloud Score",
                "Cloud Score Sum",
            ],
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
