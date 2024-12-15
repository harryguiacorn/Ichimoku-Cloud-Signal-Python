from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMergerWithList import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        # ----- Retrieve Dow Jones 30 symbols & data from Russell 1000 -----
        _model = Model(
            "asset_list/DowJones30.csv",
            "output/sum/Russell1000-sum-cloud-tkx-merged.csv",
            "output/sum/DowJones30-sum-cloud-tkx-merged_from_rs1000.csv",
            "Dow Jones 30",
        )
        _control = Control(_model, View())
        _control.main()



if __name__ == "__main__":
    main()
