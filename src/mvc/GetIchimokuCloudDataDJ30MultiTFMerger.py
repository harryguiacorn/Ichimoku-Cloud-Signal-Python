from src.mvc.DataCloudSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/DowJones30-cloud-D.csv",
                "output/DowJones30-cloud-W.csv",
                "output/DowJones30-cloud-M.csv",
            ],
            "output/DowJones30-cloud-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
