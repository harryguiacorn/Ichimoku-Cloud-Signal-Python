from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/Nasdaq100-tkx-D.csv",
                "output/Nasdaq100-tkx-W.csv",
                "output/Nasdaq100-tkx-M.csv",
            ],
            "output/Nasdaq100-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
