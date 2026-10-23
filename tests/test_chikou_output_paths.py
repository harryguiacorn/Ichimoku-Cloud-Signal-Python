import importlib

import pandas as pd


def test_generic_chikou_merger_targets_sum_directory(monkeypatch):
    merger = importlib.import_module(
        "cloud_signal.mvc.controllers.GetIchimokuChikouDataMultiTFMerger"
    )
    captured = {}

    class FakeModel:
        def __init__(
            self,
            input_paths,
            output_path,
            direction_count_names,
            score_names,
            title,
        ):
            captured["output_path"] = output_path

    class FakeControl:
        def __init__(self, model, view):
            pass

        def main(self):
            pass

    monkeypatch.setattr(merger, "Model", FakeModel)
    monkeypatch.setattr(merger, "Control", FakeControl)

    merger.main(
        "SPX500",
        [(True, "data/spx500/d/", False, "SPX500-chikou-D", "1D")],
    )

    assert captured["output_path"] == "output/sum/SPX500-chikou-merged.csv"


def test_dow_jones_chikou_merger_targets_sum_directory(monkeypatch):
    merger = importlib.import_module(
        "cloud_signal.mvc.controllers.GetIchimokuChikouDataDJ30MultiTFMerger"
    )
    captured = {}

    class FakeModel:
        def __init__(
            self,
            input_paths,
            output_path,
            direction_count_names,
            score_names,
        ):
            captured["output_path"] = output_path

    class FakeControl:
        def __init__(self, model, view):
            pass

        def main(self):
            pass

    monkeypatch.setattr(merger, "Model", FakeModel)
    monkeypatch.setattr(merger, "Control", FakeControl)

    merger.main()

    assert (
        captured["output_path"]
        == "output/sum/DowJones30-chikou-merged.csv"
    )


def test_spdr_sector_chikou_pages_read_and_write_sum_directory(
    tmp_path, monkeypatch
):
    scanner = importlib.import_module(
        "cloud_signal.mvc.controllers.GetIchimokuChikouDataMatchSPX500_SPDR_ETFs"
    )
    monkeypatch.chdir(tmp_path)
    holdings_dir = tmp_path / "asset_list" / "SPDR_ETF"
    sum_dir = tmp_path / "output" / "sum"
    holdings_dir.mkdir(parents=True)
    sum_dir.mkdir(parents=True)
    (holdings_dir / "index-holdings-xlc.csv").write_text(
        "Sector holdings\nSymbol\nTEST\n",
        encoding="utf-8",
    )
    pd.DataFrame(
        {
            "Symbol": ["TEST", "OTHER"],
            "Name": ["Test Co", "Other Co"],
            "1D Chikou Count": [4, 2],
        }
    ).to_csv(sum_dir / "SPX500-chikou-merged.csv", index=False)

    scanner.main()

    sector_output = sum_dir / "SPDR_ETF-XLC-chikou-merged.csv"
    assert sector_output.exists()
    assert pd.read_csv(sector_output)["Symbol"].tolist() == ["TEST"]
    assert (sum_dir / f"{sector_output.name}.html").exists()
