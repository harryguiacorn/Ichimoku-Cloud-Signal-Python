from src.mvc.DataTKxSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/DowJones30-tkx-D.csv",
                "output/DowJones30-tkx-W.csv",
                "output/DowJones30-tkx-M.csv",
            ],
            "output/DowJones30-tkx-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
