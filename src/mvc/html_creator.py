import pandas as pd

# from IPython.display import HTML
from src.mvc import Util
from datetime import datetime
from pytz import timezone
import logging

logger = logging.getLogger(__name__)


class TableGenerator:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def generate_html_table(self, str_title: str = "Cloud Scan") -> str:
        logger.info("------------- Generating Html table -------------")
        if Util.file_exists(self.csv_file_path) is False:
            return

        # Read the CSV file
        df = pd.read_csv(self.csv_file_path)
        logger.debug("HTML title: %s", str_title)
        # added !important in css to overwrite cell colours
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

        # Convert the CSV file to an HTML table
        html_table += df.to_html(index=False)

        # Add the DataTables plugin to the HTML table
        html_table = html_table.replace(
            "<table",
            '<table class="table table-striped table-bordered" id="dataTable_1"',
        )
        html_table += """
        <script>
        $(document).ready(function() {
          // Calculate the last column index
          let lastColumnIndex = $('#dataTable_1 thead th').length - 1; 

          // Initialize the DataTable with the order option set to sort by the last column in descending order
          $('#dataTable_1').DataTable({ order: [[lastColumnIndex, 'desc']] });

          // Get all table rows
          var rows = $('#dataTable_1').DataTable().rows().nodes();

          // Iterate over all table rows and add classes
          for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var cells = row.querySelectorAll('td');

            for (var j = 0; j < cells.length; j++) {
              var cell = cells[j];
              var value = parseFloat(cell.textContent);

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
        });     
        </script>
        </table>
        """
        # calculate time elapsed
        london_tz_finish = timezone("Europe/London")
        time_finish = datetime.now(london_tz_finish)
        time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"Table generated at {time_finish_formatted}")
        html_table += f"""
        <footer>
          <p>Table Generated At {time_finish_formatted} [UK]<br></p>
        </footer>
        </body>

        </html>
        """
        # logger.debug(html_table)
        logger.info("HTML table generated.")
        return html_table

    def save_html_table(self, html_table: str, filename: str):
        if html_table is None:
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_table)
        logger.info(f"HTML data table saved at {filename}")

    def display_html_table_jupyter(
        self, filename: str = "/content/Cloud-Signal-Python/table.html"
    ):
        if Util.file_exists(filename) is False:
            return

        # Open the HTML file and read its contents
        with open(filename, "r") as f:
            html_content = f.read()

        # Commented out because of deployment error in Koyeb and Render
        # # Display the HTML content in the Colab notebook
        # HTML(html_content)


if __name__ == "__main__":
    table_generator = TableGenerator(
        "output/sum/Oanda-sum-cloud-tkx-merged.csv"
    )
    html_table = table_generator.generate_html_table()
    table_generator.save_html_table(html_table, "table.html")
    table_generator.display_html_table_jupyter("table.html")
