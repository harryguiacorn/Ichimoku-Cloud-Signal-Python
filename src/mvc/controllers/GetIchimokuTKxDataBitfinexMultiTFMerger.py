from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/tkx/Bitfinex-tkx-1H.csv",
                "output/tkx/Bitfinex-tkx-4H.csv",
                "output/tkx/Bitfinex-tkx-D.csv",
                "output/tkx/Bitfinex-tkx-W.csv",
                "output/tkx/Bitfinex-tkx-M.csv",
            ],
            "output/tkx/Bitfinex-tkx-merged.csv",
            [
                ["1H TKx Direction", "1H TKx Count"],
                ["4H TKx Direction", "4H TKx Count"],
                ["1D TKx Direction", "1D TKx Count"],
                ["1W TKx Direction", "1W TKx Count"],
                ["1M TKx Direction", "1M TKx Count"],
            ],
            [
                "1H TKx Score",
                "4H TKx Score",
                "1D TKx Score",
                "1W TKx Score",
                "1M TKx Score",
                "TKx Score Sum",
            ],
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
