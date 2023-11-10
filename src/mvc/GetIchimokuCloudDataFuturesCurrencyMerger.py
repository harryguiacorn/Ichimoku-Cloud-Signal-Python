from src.mvc.DataCloudSignalMultiTimeframeMerge import Control, Model, View


def main():
    _model = Model(
        [
            "output/FuturesCurrency-cloud-D.csv",
            "output/FuturesCurrency-cloud-W.csv",
            "output/FuturesCurrency-cloud-M.csv",
        ],
        "output/FuturesCurrency-cloud-merged.csv",
    )
    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
