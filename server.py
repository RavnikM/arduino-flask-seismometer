# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask
from seismometer import arduino_nano_seizometer
import threading
import sqlite3
import plotly
import plotly.graph_objs as go
import pandas as pd

# Flask constructor takes the name of
# current module (__name__) as argument. 
app = Flask(__name__)


#Create "arduino_nano_seizometer" object and run reading and inserting value in thread loop
ans = arduino_nano_seizometer('COM8')
thread = threading.Thread(target=ans.archive_values)
thread.start()


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call  
# the associated function. 
@app.route('/')
# ‘/’ URL is bound with hello_world() function. 
def hello_world():
    return 'arduino nano seizometer server'

#<date> is in format 'YYYY-MM-DD'
@app.route('/csv_data/<date>')
def csv_data(date):
    with sqlite3.connect('sqlite3/seizmometer.db',check_same_thread=False) as con:
        df = pd.read_sql_query("SELECT * FROM seizmograph WHERE timestamp BETWEEN date(?) AND date(?,'+1 days')",con=con , params = (date,date))

        #fig = go.Figure([go.Scatter(x=df['timestamp'], y=df['axis_x'])])
        fig = go.Figure()

        fig.add_trace(go.Scatter( x=df['timestamp'], y=df['axis_x'], name="axis X data"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['axis_y'], name="axis Y data",yaxis="y2"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['axis_z'], name="axis Z data",yaxis="y3"))

        # Create axis objects
        fig.update_layout(
            xaxis=dict(
                domain=[0.3, 0.7]
            ),
            yaxis=dict(
                title="axis X",
                titlefont=dict(
                    color="#1f77b4"
                ),
                tickfont=dict(
                    color="#1f77b4"
                )
            ),
            yaxis2=dict(
                title="axis2 Y",
                titlefont=dict(
                    color="#ff7f0e"
                ),
                tickfont=dict(
                    color="#ff7f0e"
                ),
                anchor="free",
                overlaying="y",
                side="left",
                position=0.15
            ),
            yaxis3=dict(
                title="axis Z",
                titlefont=dict(
                    color="#d62728"
                ),
                tickfont=dict(
                    color="#d62728"
                ),
                anchor="free",
                overlaying="y",
                side="left"
            )
        )


        fig.update_layout(
            title_text="arduino nano seizometer server data",
        )

        div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True)
        return div


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server. 
    app.run() 