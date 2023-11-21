from src.mvc.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/Futures-tkx-D.csv",
                "output/Futures-tkx-W.csv",
                "output/Futures-tkx-M.csv",
            ],
            "output/Futures-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
