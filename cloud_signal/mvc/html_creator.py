import html
import json
import logging
import math
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from pytz import timezone

# from IPython.display import HTML
from cloud_signal.mvc import Util

logger = logging.getLogger(__name__)

SPDR_SECTOR_SYMBOLS = {
  "XLB",
  "XLC",
  "XLE",
  "XLF",
  "XLI",
  "XLK",
  "XLP",
  "XLRE",
  "XLU",
  "XLV",
  "XLY",
}


def _spdr_sector_scan_suffix(csv_file_path: str):
  return {
    "SPDR_ETFS-sum-cloud-tkx-merged.csv": "sum-cloud-tkx-merged",
    "SPDR_ETFs-chikou-merged.csv": "chikou-merged",
  }.get(Path(csv_file_path).name)


def _spdr_sector_page_href(symbol, suffix: str, tabulator: bool = False):
  symbol = str(symbol).strip()
  if symbol not in SPDR_SECTOR_SYMBOLS:
    return None

  page_extension = ".tabulator.html" if tabulator else ".html"
  return f"SPDR_ETF-{symbol}-{suffix}.csv{page_extension}"


def _spdr_sector_symbol_html(symbol, suffix: str) -> str:
  symbol_text = html.escape(str(symbol))
  href = _spdr_sector_page_href(symbol, suffix)
  if href is None:
    return symbol_text
  return f'<a href="{html.escape(href, quote=True)}">{symbol_text}</a>'


def _move_close_after_name(df: pd.DataFrame) -> pd.DataFrame:
    if "Name" not in df.columns or "Close" not in df.columns:
        return df

    columns = list(df.columns)
    columns.remove("Close")
    columns.insert(columns.index("Name") + 1, "Close")
    return df[columns]


def _format_close_value(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value

    if math.isfinite(number) and number != round(number, 2):
        return f"{number:.2f}"
    return value


def _wrap_header_label(label: str, column_index: int, is_chikou: bool) -> str:
    cleaned = str(label).strip()
    if is_chikou:
        cleaned = re.sub(r"\bChikou\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return f"{cleaned}<br>&nbsp;"
    if (is_chikou and column_index >= 1) or (
        (not is_chikou) and column_index >= 2
    ):
        parts = cleaned.split()
        if len(parts) >= 2 and parts[0].lower() not in {
            "symbol",
            "name",
            "close",
            "date",
        }:
            if parts[0].startswith(
                ("1H", "4H", "1D", "1W", "1M", "3M", "6M", "1Y")
            ):
                return f"{parts[0]}<br>{' '.join(parts[1:])}"
            if parts[0].lower() in {
                "cloud",
                "chikou",
                "tkx",
                "total",
                "score",
                "signal",
                "count",
                "state",
                "direction",
            }:
                return f"{parts[0]}<br>{' '.join(parts[1:])}"
            if parts[0].isdigit() and len(parts) > 1:
                return f"{parts[0]}<br>{' '.join(parts[1:])}"
    return f"{cleaned}<br>&nbsp;"


class TableGenerator:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self._hidden_columns = None
        self._title = "Cloud Scan"

    def generate_html_table(
        self, str_title: str = "Cloud Scan", hidden_columns=None
    ) -> str:
        logger.info("------------- Generating Html table -------------")
        if Util.file_exists(self.csv_file_path) is False:
            return

        df = pd.read_csv(self.csv_file_path)
        self._hidden_columns = hidden_columns
        self._title = str_title
        if hidden_columns:
            df = df.drop(columns=hidden_columns, errors="ignore")
        spdr_sector_suffix = _spdr_sector_scan_suffix(self.csv_file_path)
        if spdr_sector_suffix and "Symbol" in df.columns:
          df["Symbol"] = df["Symbol"].map(
            lambda symbol: _spdr_sector_symbol_html(
              symbol, spdr_sector_suffix
            )
          )
        df = _move_close_after_name(df)

        is_chikou_page = any("Chikou" in str(column) for column in df.columns)
        close_column_index = (
            df.columns.get_loc("Close") if "Close" in df.columns else None
        )
        df = df.copy()
        df.columns = [
            _wrap_header_label(column, idx, is_chikou_page)
            for idx, column in enumerate(df.columns)
        ]
        if close_column_index is not None:
            close_column_label = df.columns[close_column_index]
            df[close_column_label] = df[close_column_label].map(
                _format_close_value
            )

        logger.debug("HTML title: %s", str_title)
        html_table_head = f"""
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="../../css/html_creator.css">
          <title>{str_title}</title>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/css/bootstrap.min.css">
          <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css">
          <link rel="icon" type="image/x-icon" href="../../favicon/favicon.ico">
          <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
          <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
          <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
      </head>
      <body>
        <nav class="scan-navigation" aria-label="Page navigation">
          <a href="../../index.html">Home</a>
          <button type="button" class="search-help-button" data-search-help-open>Filter guide</button>
        </nav>
        <h1>{str_title}</h1>
        <dialog class="search-help-dialog" data-search-help-dialog aria-labelledby="search-help-title">
          <h2 id="search-help-title">Filter guide</h2>
          <p>For numeric columns:</p>
          <ul>
            <li><code>1</code> matches exactly 1</li>
            <li><code>&gt;1</code> or <code>1+</code> matches values greater than 1</li>
            <li><code>0+</code> matches positive values; <code>0-</code> matches negative values</li>
            <li><code>0-3</code> matches values from 0 through 3, inclusive</li>
          </ul>
          <p>Comparisons such as <code>&gt;=1</code>, <code>&lt;1</code>, and <code>&lt;=1</code> are also supported. Text searches match partial values, ignoring case.</p>
          <form method="dialog"><button type="submit">Close</button></form>
        </dialog>
      """
        html_table = html_table_head
        html_table += df.to_html(index=False, escape=False)
        html_table = html_table.replace(
            "<table",
            '<table class="table table-striped table-bordered" id="dataTable_1"',
        )
        html_table += """
        <script>
        const classifyCell = (cell, isStateColumn, isCloseColumn) => {
          cell.classList.remove('highlight-positive', 'highlight-negative', 'highlight-neutral');
          const text = cell.textContent.trim();
          const normalized = text.toLowerCase();

          if (isCloseColumn) return;

          if (isStateColumn) {
            if (normalized.startsWith('above')) {
              cell.classList.add('highlight-positive');
            } else if (normalized.startsWith('below')) {
              cell.classList.add('highlight-negative');
            }
            return;
          }

          const numericText = text.replace(/,/g, '');
          if (/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(numericText)) {
            const value = Number(numericText);
            if (value > 0) {
              cell.classList.add('highlight-positive');
            } else if (value < 0) {
              cell.classList.add('highlight-negative');
            } else {
              cell.classList.add('highlight-neutral');
            }
          }
        };

        const wrapHeaderLabel = (label, columnIndex, isChikou) => {
          const cleaned = String(label).trim();
          if (!cleaned) return cleaned;

          const firstWrapIndex = isChikou ? 1 : 2;
          if (columnIndex >= firstWrapIndex) {
            const parts = cleaned.split(/\s+/);
            if (parts.length >= 2 && !['Symbol', 'Name', 'Close', 'Date'].includes(parts[0])) {
              if (/^(1H|4H|1D|1W|1M|3M|6M|1Y)/.test(parts[0])) {
                return `${parts[0]}<br>${parts.slice(1).join(' ')}`;
              }
              if (['Cloud', 'Chikou', 'TKx', 'Total', 'Score', 'Signal', 'Count', 'State', 'Direction'].includes(parts[0])) {
                return `${parts[0]}<br>${parts.slice(1).join(' ')}`;
              }
            }
          }
          return cleaned;
        };

        $(document).ready(function() {
          const searchHelpDialog = document.querySelector('[data-search-help-dialog]');
          document.querySelector('[data-search-help-open]').addEventListener('click', () => searchHelpDialog.showModal());
          searchHelpDialog.addEventListener('click', (event) => {
            if (event.target !== searchHelpDialog) return;
            const bounds = searchHelpDialog.getBoundingClientRect();
            if (
              event.clientX < bounds.left || event.clientX > bounds.right ||
              event.clientY < bounds.top || event.clientY > bounds.bottom
            ) {
              searchHelpDialog.close();
            }
          });

          const isChikou = $('#dataTable_1 thead th').toArray().some((th) => th.textContent.includes('Chikou'));
          $('#dataTable_1 thead th').each(function(index) {
            const raw = $(this).text().trim();
            const wrapped = wrapHeaderLabel(raw, index, isChikou);
            if (wrapped !== raw) {
              $(this).html(wrapped);
            }
          });

          const table = $('#dataTable_1').DataTable({
            order: [[$('#dataTable_1 thead th').length - 1, 'desc']],
            drawCallback: function() {
              const stateColumnIndexes = $('#dataTable_1 thead th')
                .toArray()
                .map((th, index) => th.textContent.toLowerCase().includes('state') ? index : null)
                .filter(index => index !== null);
              const closeColumnIndexes = $('#dataTable_1 thead th')
                .toArray()
                .map((th, index) => th.textContent.toLowerCase().includes('close') ? index : null)
                .filter(index => index !== null);

              $('#dataTable_1 tbody tr').each(function() {
                $(this).find('td').each(function(index) {
                  classifyCell(
                    this,
                    stateColumnIndexes.includes(index),
                    closeColumnIndexes.includes(index)
                  );
                });
              });
            },
            initComplete: function() {
              this.api().draw(false);
            }
          });
        });
        </script>
        </table>
        """

        london_tz_finish = timezone("Europe/London")
        time_finish = datetime.now(london_tz_finish)
        time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
        logger.info("Last updated: %s", time_finish_formatted)

        html_table += f"""
        <footer>
          <p>Last updated: {time_finish_formatted} [UK]<br></p>
        </footer>
        </body>
        </html>
        """
        logger.info("HTML Last updated: .")
        return html_table

    def generate_tabulator_html_table(
        self, str_title: str = "Cloud Scan", hidden_columns=None
    ) -> str:
        """Generate a sortable, filterable Tabulator page for the CSV data."""
        logger.info("------------- Generating Tabulator table -------------")
        if Util.file_exists(self.csv_file_path) is False:
            return

        df = pd.read_csv(self.csv_file_path)
        if hidden_columns:
            df = df.drop(columns=hidden_columns, errors="ignore")
        df = _move_close_after_name(df)

        columns = []
        is_chikou_page = any("Chikou" in str(column) for column in df.columns)
        for index, column in enumerate(df.columns):
            title = _wrap_header_label(column, index, is_chikou_page)
            definition = {
                "title": title,
                "field": str(column),
                "headerFilter": "input",
            }
            if pd.api.types.is_numeric_dtype(df[column]):
                definition["sorter"] = "number"
                definition["hozAlign"] = "right"
            columns.append(definition)

        data_json = df.to_json(orient="records", date_format="iso")
        data_json = data_json.replace("<", "\\u003c")
        columns_json = json.dumps(columns)
        spdr_sector_suffix = _spdr_sector_scan_suffix(self.csv_file_path)
        spdr_sector_symbols_json = json.dumps(sorted(SPDR_SECTOR_SYMBOLS))
        safe_title = html.escape(str_title, quote=True)
        london_tz_finish = timezone("Europe/London")
        time_finish = datetime.now(london_tz_finish)
        time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="../../css/html_creator.css">
  <link rel="stylesheet" href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css">
  <link rel="icon" type="image/x-icon" href="../../favicon/favicon.ico">
  <style>
    body {{ background: #eef2f4; color: #17212b; }}
    .tabulator-page {{ max-width: 100%; margin: 0 auto; padding: 24px; }}
    .search-help-dialog {{ max-width: 440px; border: 2px solid #344955; padding: 20px; color: #17212b; }}
    .search-help-dialog::backdrop {{ background: rgba(23, 33, 43, .45); }}
    .search-help-dialog h2 {{ margin-top: 0; font-size: 1.25rem; }}
    .tabulator {{ border: 2px solid #344955; background: #ffffff; box-shadow: 0 8px 20px rgba(23, 33, 43, .14); }}
    .tabulator .tabulator-header, .tabulator .tabulator-header .tabulator-col {{ background: #17212b; color: #ffffff; }}
    .tabulator .tabulator-header .tabulator-col {{ border-right: 1px solid #657782; }}
    .tabulator .tabulator-header-filter input {{ background: #ffffff; color: #17212b; border: 2px solid #8ba3af; border-radius: 3px; }}
    .tabulator-row {{ border-bottom: 1px solid #c4d0d6; }}
    .tabulator-row:nth-child(even) {{ background: #e8f0f2; }}
    .tabulator-row:hover {{ background: #b9dfe0 !important; }}
    .tabulator .tabulator-cell {{ border-right: 1px solid #d0dbe0; white-space: normal !important; word-break: break-word; line-height: 1.4; }}
    .tabulator .tabulator-header .tabulator-col {{ height: 80px !important; min-height: 80px !important; box-sizing: border-box; line-height: 1.25 !important; text-align: center !important; }}
    .tabulator .tabulator-col-title {{ display: flex; align-items: center; justify-content: center; min-height: 28px; white-space: normal !important; word-break: break-word; line-height: 1.4; text-align: center; }}
    .highlight-positive {{ background-color: #d1f2d1 !important; color: #0b6e3d !important; font-weight: 600; }}
    .highlight-negative {{ background-color: #f8d7da !important; color: #8b1e2d !important; font-weight: 600; }}
    .highlight-neutral {{ background-color: #e6e7e8 !important; color: #4a4a4a !important; }}
  </style>
</head>
<body>
  <main class="tabulator-page">
    <nav class="scan-navigation" aria-label="Page navigation">
      <a href="../../index.html">Home</a>
      <button type="button" class="search-help-button" data-search-help-open>Filter guide</button>
    </nav>
    <h1>{safe_title}</h1>
    <dialog class="search-help-dialog" data-search-help-dialog aria-labelledby="search-help-title">
      <h2 id="search-help-title">Filter guide</h2>
      <p>For numeric columns:</p>
      <ul>
        <li><code>1</code> matches exactly 1</li>
        <li><code>&gt;1</code> or <code>1+</code> matches values greater than 1</li>
        <li><code>0+</code> matches positive values; <code>0-</code> matches negative values</li>
        <li><code>0-3</code> matches values from 0 through 3, inclusive</li>
      </ul>
      <p>Comparisons such as <code>&gt;=1</code>, <code>&lt;1</code>, and <code>&lt;=1</code> are also supported. Text searches match partial values, ignoring case.</p>
      <form method="dialog"><button type="submit">Close</button></form>
    </dialog>
    <div id="dataTableTabulator"></div>
    <footer><p>Last updated: {time_finish_formatted} [UK]</p></footer>
  </main>
  <script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
  <script>
    const tableData = {data_json};
    const tableColumns = {columns_json};
    const spdrSectorPageSuffix = {json.dumps(spdr_sector_suffix)};
    const spdrSectorSymbols = new Set({spdr_sector_symbols_json});
    const searchHelpDialog = document.querySelector('[data-search-help-dialog]');
    document.querySelector('[data-search-help-open]').addEventListener('click', () => searchHelpDialog.showModal());
    searchHelpDialog.addEventListener('click', (event) => {{
      if (event.target !== searchHelpDialog) return;
      const bounds = searchHelpDialog.getBoundingClientRect();
      if (
        event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom
      ) {{
        searchHelpDialog.close();
      }}
    }});
    const textHeaderFilter = (headerValue, rowValue) =>
      String(rowValue ?? "").toLowerCase().includes(String(headerValue ?? "").trim().toLowerCase());
    const numericHeaderFilter = (headerValue, rowValue) => {{
      const query = String(headerValue ?? "").trim();
      const value = Number(String(rowValue ?? "").replace(/,/g, ""));
      if (!query) return true;
      if (!Number.isFinite(value)) return false;

      const rangeMatch = query.match(/^([+-]?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)) *- *([+-]?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+))$/);
      if (rangeMatch) {{
        const lowerBound = Number(rangeMatch[1].replace(/,/g, ""));
        const upperBound = Number(rangeMatch[2].replace(/,/g, ""));
        return Number.isFinite(lowerBound) && Number.isFinite(upperBound)
          && value >= lowerBound && value <= upperBound;
      }}

      const match = query.match(/^(>=|<=|>|<|=)? *([+-]?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)) *([+-]?)$/);
      if (!match) return false;

      const [, operator, thresholdText, suffix] = match;
      const threshold = Number(thresholdText.replace(/,/g, ""));
      if (!Number.isFinite(threshold)) return false;
      if (suffix) {{
        if (operator) return false;
        return suffix === "+" ? value > threshold : value < threshold;
      }}

      switch (operator || "=") {{
        case ">": return value > threshold;
        case ">=": return value >= threshold;
        case "<": return value < threshold;
        case "<=": return value <= threshold;
        default: return value === threshold;
      }}
    }};
    tableColumns.forEach(column => {{
      column.headerFilterFunc = column.sorter === "number"
        ? numericHeaderFilter
        : textHeaderFilter;
    }});
    const closeColumn = tableColumns.find(column => column.field === "Close");
    if (closeColumn) {{
      closeColumn.formatter = cell => {{
        const value = cell.getValue();
        if (typeof value !== "number" || !Number.isFinite(value)) return value;
        const roundedValue = Number(value.toFixed(2));
        return roundedValue === value ? value : value.toFixed(2);
      }};
    }}
    const symbolColumn = tableColumns.find(column => column.field === "Symbol");
    if (symbolColumn && spdrSectorPageSuffix) {{
      symbolColumn.formatter = cell => {{
        const symbol = String(cell.getValue() ?? "").trim();
        if (!spdrSectorSymbols.has(symbol)) return cell.getValue();
        const link = document.createElement("a");
        link.href = `SPDR_ETF-${{symbol}}-${{spdrSectorPageSuffix}}.csv.tabulator.html`;
        link.textContent = symbol;
        return link;
      }};
    }}
    const tabulatorTable = new Tabulator("#dataTableTabulator", {{
      data: tableData,
      columns: tableColumns,
      layout: "fitDataTable",
      responsiveLayout: false,
      pagination: true,
      paginationSize: 50,
      paginationSizeSelector: [25, 50, 100, true],
      initialSort: [{{column: tableColumns[tableColumns.length - 1].field, dir: "desc"}}],
      placeholder: "No matching rows"
    }});

    const applyNumericHighlights = () => {{
      const rows = tabulatorTable.getRows();
      rows.forEach(row => {{
        row.getCells().forEach(cell => {{
          const rawValue = String(cell.getValue() ?? '').trim();
          const element = cell.getElement();
          element.classList.remove('highlight-positive', 'highlight-negative', 'highlight-neutral');

          const normalized = rawValue.toLowerCase();
          const field = String(cell.getColumn().getField() ?? '').toLowerCase();
          if (field.includes('close')) return;
          if (field.includes('state')) {{
            if (normalized.startsWith('above')) element.classList.add('highlight-positive');
            else if (normalized.startsWith('below')) element.classList.add('highlight-negative');
            return;
          }}

          const numericText = rawValue.replace(/,/g, '');
          if (/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(numericText)) {{
            const value = Number(numericText);
            if (value > 0) element.classList.add('highlight-positive');
            else if (value < 0) element.classList.add('highlight-negative');
            else element.classList.add('highlight-neutral');
          }}
        }});
      }});
    }};

    tabulatorTable.on("renderComplete", applyNumericHighlights);
    tabulatorTable.on("dataLoaded", applyNumericHighlights);
  tabulatorTable.on("pageLoaded", applyNumericHighlights);
  </script>
</body>
</html>
"""

    def save_html_table(self, html_table: str, filename: str):
        if html_table is None:
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)
        logger.info("HTML data table saved at %s", filename)

        title_match = re.search(r"<title>(.*?)</title>", html_table, re.S)
        if title_match:
            self._title = html.unescape(title_match.group(1).strip())

        tabulator_html = self.generate_tabulator_html_table(
            self._title, hidden_columns=self._hidden_columns
        )
        if tabulator_html is not None:
            tabulator_filename = (
                filename.removesuffix(".html") + ".tabulator.html"
            )
            with open(tabulator_filename, "w", encoding="utf-8") as f:
                f.write(tabulator_html)
            logger.info("Tabulator data table saved at %s", tabulator_filename)

    def display_html_table_jupyter(
        self, filename: str = "/content/Cloud-Signal-Python/table.html"
    ):
        if Util.file_exists(filename) is False:
            return

        with open(filename, "r", encoding="utf-8") as f:
            _ = f.read()


if __name__ == "__main__":
    table_generator = TableGenerator(
        "output/sum/Oanda-sum-cloud-tkx-merged.csv"
    )
    html_table = table_generator.generate_html_table()
    table_generator.save_html_table(html_table, "table.html")
    table_generator.display_html_table_jupyter("table.html")
