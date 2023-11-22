from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/ -tkx-D.csv",
                "output/ -tkx-W.csv",
                "output/ -tkx-M.csv",
            ],
            "output/ -tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
