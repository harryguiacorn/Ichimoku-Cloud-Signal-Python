from src.mvc.DataCloudSignalMultiTimeframeMerge import Control, Model, View


def main():
    _model = Model(
        [
            "output/Futures-cloud-D.csv",
            "output/Futures-cloud-W.csv",
            "output/Futures-cloud-M.csv",
        ],
        "output/Futures-cloud-merged.csv",
    )
    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
