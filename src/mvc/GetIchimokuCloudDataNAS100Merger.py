from src.mvc.DataCloudSignalMultiTimeframeMerge import Control, Model, View


def main():
    _model = Model(
        [
            "output/Nasdaq100-cloud-D.csv",
            "output/Nasdaq100-cloud-W.csv",
            "output/Nasdaq100-cloud-M.csv",
        ],
        "output/Nasdaq100-cloud-merged.csv",
    )
    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
