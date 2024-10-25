from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMergerWithList import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        # ----- XLC - Communication Services -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlc.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLC-sum-cloud-tkx-merged.csv",
            "XLC - Communication Services",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLY - Consumer Discretionary -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xly.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLY-sum-cloud-tkx-merged.csv",
            "XLY - Consumer Discretionary",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLP - Consumer Staples -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlp.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLP-sum-cloud-tkx-merged.csv",
            "XLP - Consumer Staples",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLE - Energy -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xle.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLE-sum-cloud-tkx-merged.csv",
            "XLE - Energy",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLF - Financials -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlf.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLF-sum-cloud-tkx-merged.csv",
            "XLF - Financials",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLV - Health Care -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlv.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLV-sum-cloud-tkx-merged.csv",
            "XLV - Health Care",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLI - Industrials -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xli.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLI-sum-cloud-tkx-merged.csv",
            "XLI - Industrials",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLB - Materials -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlb.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLB-sum-cloud-tkx-merged.csv",
            "XLB - Materials",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLRE - Real Estate -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlre.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLRE-sum-cloud-tkx-merged.csv",
            "XLRE - Energy",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLK - Technology -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlk.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLK-sum-cloud-tkx-merged.csv",
            "XLK - Energy",
        )
        _control = Control(_model, View())
        _control.main()

        # ----- XLU - Utilities -----
        _model = Model(
            "asset_list/SPDR_ETF/index-holdings-xlu.csv",
            "output/sum/SPX500-sum-cloud-tkx-merged.csv",
            "output/sum/SPDR_ETF-XLU-sum-cloud-tkx-merged.csv",
            "XLU - Energy",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
