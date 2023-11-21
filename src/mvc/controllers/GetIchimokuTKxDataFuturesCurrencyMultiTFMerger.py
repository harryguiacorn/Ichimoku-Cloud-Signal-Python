from src.mvc.core.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FuturesCurrency-tkx-D.csv",
                "output/FuturesCurrency-tkx-W.csv",
                "output/FuturesCurrency-tkx-M.csv",
            ],
            "output/FuturesCurrency-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
