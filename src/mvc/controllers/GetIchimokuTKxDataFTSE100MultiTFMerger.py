from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FTSE100-tkx-D.csv",
                "output/FTSE100-tkx-W.csv",
                "output/FTSE100-tkx-M.csv",
            ],
            "output/FTSE100-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
