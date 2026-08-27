from cloud_signal.mvc.core.DataChikouSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        model = Model(
            [
                "output/chikou/DowJones30-chikou-1H.csv",
                "output/chikou/DowJones30-chikou-D.csv",
                "output/chikou/DowJones30-chikou-W.csv",
                "output/chikou/DowJones30-chikou-M.csv",
            ],
            "output/chikou/DowJones30-chikou-merged.csv",
            [
                ["1H Chikou Direction", "1H Chikou Count"],
                ["1D Chikou Direction", "1D Chikou Count"],
                ["1W Chikou Direction", "1W Chikou Count"],
                ["1M Chikou Direction", "1M Chikou Count"],
            ],
            ["Chikou Score Sum"],
        )
        Control(model, View()).main()
