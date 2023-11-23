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
            [
                ["1H Cloud Direction", "1H Cloud Count"],
                ["4H Cloud Direction", "4H Cloud Count"],
                ["1D Cloud Direction", "1D Cloud Count"],
                ["1W Cloud Direction", "1W Cloud Count"],
                ["1M Cloud Direction", "1M Cloud Count"],
            ],
            [
                "1H Cloud Score",
                "4H Cloud Score",
                "1D Cloud Score",
                "1W Cloud Score",
                "1M Cloud Score",
            ],
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
