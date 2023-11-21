from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/SPX500-tkx-D.csv",
                "output/SPX500-tkx-W.csv",
                "output/SPX500-tkx-M.csv",
            ],
            "output/SPX500-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
