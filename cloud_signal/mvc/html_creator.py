import html
import json
import logging
import re
from datetime import datetime

import pandas as pd
from pytz import timezone

# from IPython.display import HTML
from cloud_signal.mvc import Util

logger = logging.getLogger(__name__)


def _wrap_header_label(label: str, column_index: int, is_chikou: bool) -> str:
    cleaned = str(label).strip()
    if not cleaned:
        return cleaned
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
                return f"{parts[0]}\n{' '.join(parts[1:])}"
            if parts[0].lower() in {
                "cloud",
                "chikou",
                "tkx",
                "score",
                "signal",
                "count",
                "state",
                "direction",
            }:
                return f"{parts[0]}\n{' '.join(parts[1:])}"
            if parts[0].isdigit() and len(parts) > 1:
                return f"{parts[0]}\n{' '.join(parts[1:])}"
    return cleaned


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

        is_chikou_page = any("Chikou" in str(column) for column in df.columns)
        df = df.copy()
        df.columns = [
            _wrap_header_label(column, idx, is_chikou_page)
            for idx, column in enumerate(df.columns)
        ]

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
        <h1>{str_title}</h1>
      """
        html_table = html_table_head
        html_table += df.to_html(index=False, escape=False)
        html_table = html_table.replace(
            "<table",
            '<table class="table table-striped table-bordered" id="dataTable_1"',
        )
        html_table += """
        <script>
        const wrapHeaderLabel = (label, columnIndex, isChikou) => {
          const cleaned = String(label).trim();
          if (!cleaned) return cleaned;

          const firstWrapIndex = isChikou ? 1 : 2;
          if (columnIndex >= firstWrapIndex) {
            const parts = cleaned.split(/\s+/);
            if (parts.length >= 2 && !['Symbol', 'Name', 'Close', 'Date'].includes(parts[0])) {
              if (/^(1H|4H|1D|1W|1M|3M|6M|1Y)/.test(parts[0])) {
                return `${parts[0]}\n${parts.slice(1).join(' ')}`;
              }
              if (['Cloud', 'Chikou', 'TKx', 'Score', 'Signal', 'Count', 'State', 'Direction'].includes(parts[0])) {
                return `${parts[0]}\n${parts.slice(1).join(' ')}`;
              }
            }
          }
          return cleaned;
        };

        $(document).ready(function() {
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
            initComplete: function() {
              const rows = table.rows().nodes();
              for (let i = 0; i < rows.length; i++) {
                const cells = rows[i].querySelectorAll('td');
                for (let j = 0; j < cells.length; j++) {
                  const cell = cells[j];
                  const text = cell.textContent.trim();
                  const normalized = text.toLowerCase();

                  if (normalized.startsWith('above')) {
                    cell.classList.add('highlight-positive');
                  } else if (normalized.startsWith('below')) {
                    cell.classList.add('highlight-negative');
                  } else {
                    const value = parseFloat(text);
                    if (!isNaN(value)) {
                      if (value > 0) {
                        cell.classList.add('highlight-positive');
                      } else if (value < 0) {
                        cell.classList.add('highlight-negative');
                      } else {
                        cell.classList.add('highlight-neutral');
                      }
                    }
                  }
                }
              }
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

        columns = []
        for column in df.columns:
            title = str(column).strip()
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
    .tabulator {{ border: 2px solid #344955; background: #ffffff; box-shadow: 0 8px 20px rgba(23, 33, 43, .14); }}
    .tabulator .tabulator-header, .tabulator .tabulator-header .tabulator-col {{ background: #17212b; color: #ffffff; }}
    .tabulator .tabulator-header .tabulator-col {{ border-right: 1px solid #657782; }}
    .tabulator .tabulator-header-filter input {{ background: #ffffff; color: #17212b; border: 2px solid #8ba3af; border-radius: 3px; }}
    .tabulator-row {{ border-bottom: 1px solid #c4d0d6; }}
    .tabulator-row:nth-child(even) {{ background: #e8f0f2; }}
    .tabulator-row:hover {{ background: #b9dfe0 !important; }}
    .tabulator .tabulator-cell {{ border-right: 1px solid #d0dbe0; white-space: normal !important; word-break: break-word; line-height: 1.4; }}
    .tabulator .tabulator-col-title {{ white-space: normal !important; word-break: break-word; line-height: 1.4; }}
    .highlight-positive {{ background-color: #d1f2d1 !important; color: #0b6e3d !important; font-weight: 600; }}
    .highlight-negative {{ background-color: #f8d7da !important; color: #8b1e2d !important; font-weight: 600; }}
    .highlight-neutral {{ background-color: #e6e7e8 !important; color: #4a4a4a !important; }}
  </style>
</head>
<body>
  <main class="tabulator-page">
    <h1>{safe_title}</h1>
    <div id="dataTableTabulator"></div>
    <footer><p>Last updated: {time_finish_formatted} [UK]</p></footer>
  </main>
  <script src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
  <script>
    const tableData = {data_json};
    const tableColumns = {columns_json};
    const exactHeaderFilter = (headerValue, rowValue) =>
      String(rowValue ?? "").trim() === String(headerValue ?? "").trim();
    tableColumns.forEach(column => {{
      column.headerFilterFunc = exactHeaderFilter;
    }});
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
          if (normalized.startsWith('above')) {{
            element.classList.add('highlight-positive');
            return;
          }}
          if (normalized.startsWith('below')) {{
            element.classList.add('highlight-negative');
            return;
          }}

          const value = Number.parseFloat(rawValue);
          if (Number.isFinite(value)) {{
            if (value > 0) element.classList.add('highlight-positive');
            else if (value < 0) element.classList.add('highlight-negative');
            else element.classList.add('highlight-neutral');
          }}
        }});
      }});
    }};

    tabulatorTable.on("renderComplete", applyNumericHighlights);
    tabulatorTable.on("dataLoaded", applyNumericHighlights);
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
