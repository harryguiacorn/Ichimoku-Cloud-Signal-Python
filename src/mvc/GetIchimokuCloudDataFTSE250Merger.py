from src.mvc.DataCloudSignalMultiTimeframeMerge import Control, Model, View


def main():
    _model = Model(
        [
            "output/FTSE250-cloud-D.csv",
            "output/FTSE250-cloud-W.csv",
            "output/FTSE250-cloud-M.csv",
        ],
        "output/FTSE250-cloud-merged.csv",
    )
    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
