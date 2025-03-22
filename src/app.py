'''
 # @ Create Time: 2025-03-21 20:33:20.092521
'''

import pathlib
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="Capstone")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))
# Load patient data
df = load_data("patients_data.csv")  # Replace with your dataset name

# Generate a list of unique patient IDs for the dropdown
patient_ids = df['patient_id'].unique()

app.layout = html.Div([
    html.H4('Spider Map for Patient Metrics'),
    dcc.Dropdown(
        id='patient-dropdown',
        options=[{'label': f'Patient {pid}', 'value': pid} for pid in patient_ids],
        value=patient_ids[0],  # Default selection
        placeholder="Select a Patient ID",
    ),
    dcc.Graph(id="spider-map")
])

@app.callback(
    Output("spider-map", "figure"),
    Input("patient-dropdown", "value")
)
def update_spider_map(patient_id):
    # Filter data for the selected patient
    patient_data = df[df['patient_id'] == patient_id].iloc[0]

    # Define radar/spider map categories and values
    categories = ['Metric 1', 'Metric 2', 'Metric 3', 'Metric 4', 'Metric 5']
    values = [patient_data[metric] for metric in categories]
    values += values[:1]  # Close the circle

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],  # Add first category to close circle
        fill='toself',
        name=f'Patient {patient_id}'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]  # Adjust range as needed
            )
        ),
        showlegend=True
    )

    return fig
if __name__ == '__main__':
    app.run(debug=True)
