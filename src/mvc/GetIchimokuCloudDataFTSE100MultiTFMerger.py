from src.mvc.DataCloudSignalMultiTimeframeMerger import Control, Model, View


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/FTSE100-cloud-D.csv",
                "output/FTSE100-cloud-W.csv",
                "output/FTSE100-cloud-M.csv",
            ],
            "output/FTSE100-cloud-merged.csv",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
