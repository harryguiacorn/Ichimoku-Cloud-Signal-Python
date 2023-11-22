from src.mvc.core.DataCloudSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/Oanda-cloud-1H.csv",
                "output/Oanda-cloud-4H.csv",
                "output/Oanda-cloud-D.csv",
                "output/Oanda-cloud-W.csv",
                "output/Oanda-cloud-M.csv",
            ],
            "output/Oanda-cloud-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
