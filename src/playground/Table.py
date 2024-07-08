import pandas as pd
from jinja2 import Template

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("SPX500-tkx-D.csv")

# Define the Jinja2 template for the HTML table
template_str = """
<table class="sortable">
  <thead>
    {% for col in cols %}
      <th class="header {{ col|lower }}">{{ col }}</th>
    {% endfor %}
  </thead>
  <tbody>
    {% for row in rows %}
      <tr>
        {% for col in cols %}
          <td>{{ row[col] }}</td>
        {% endfor %}
      </tr>
    {% endfor %}
  </tbody>
</table>

<!-- Include the jQuery and tablesorter.js libraries -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script>

<!-- Initialize the tablesorter plugin on the table -->
<script>
  $(document).ready(function() {
    $('table.sortable').tablesorter({
      headers: {
        {% for col in cols %}
          {{ loop.index0 }}: { sorter: '{{ col|lower }}' },
        {% endfor %}
      }
    });
  });
</script>
"""

# Create a Jinja2 template object from the template string
template = Template(template_str)

# Render the Jinja2 template using the DataFrame
html = template.render(cols=df.columns, rows=df.to_dict("records"))

# Write the HTML output to a file
with open("output.html", "w") as f:
    f.write(html)
