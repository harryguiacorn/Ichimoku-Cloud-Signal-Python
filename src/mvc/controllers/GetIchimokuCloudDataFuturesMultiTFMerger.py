from src.mvc.core.DataCloudSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/Futures-cloud-D.csv",
                "output/Futures-cloud-W.csv",
                "output/Futures-cloud-M.csv",
            ],
            "output/Futures-cloud-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
