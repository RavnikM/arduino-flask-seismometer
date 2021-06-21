### **Arduino nano seismometer**

Simple application for collecting data from arduino nano seismometer to SQLite database and visualisation with Flask nad Plotly chart.

install requirements with `pip install -r requirements.txt`

download plotly https://cdn.plot.ly/plotly-2.0.0.min.js to `/static/` folder

download SQLite3 dll from https://www.sqlite.org/download.html to `/sqlite3/` folder

run Flask server `python server.py`

To plot daily data of senzor route to
`[host:port]/csv_data/[YYYY-MM-DD]`

[Marko Ravnik](markoravnik@gmail.com)