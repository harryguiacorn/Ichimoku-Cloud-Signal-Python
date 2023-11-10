from src.mvc.DataCloudSignalMultiTimeframeMerge import Control, Model, View


def main():
    _model = Model(
        [
            "output/NAS100-cloud-D.csv",
            "output/NAS100-cloud-W.csv",
            "output/NAS100-cloud-M.csv",
        ],
        "output/NAS100-cloud-merged.csv",
    )
    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
