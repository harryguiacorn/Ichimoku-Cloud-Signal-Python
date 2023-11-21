from src.mvc.core.DataCloudSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FuturesCurrency-cloud-D.csv",
                "output/FuturesCurrency-cloud-W.csv",
                "output/FuturesCurrency-cloud-M.csv",
            ],
            "output/FuturesCurrency-cloud-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
