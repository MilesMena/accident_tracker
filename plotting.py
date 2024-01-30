import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def accidents_percent_dash(df):
    def update_plot(perc_var):
        county_counts = df.groupby(['County', perc_var]).size().unstack(fill_value=0)
        county_perc = (county_counts.div(county_counts.sum(axis=1), axis=0) * 100).reset_index()
        melted_df = pd.melt(county_perc, id_vars=['County'], var_name=perc_var, value_name='Percentage')
        
        fig = px.bar(melted_df, x='County', y='Percentage', color=perc_var)
        fig.update_layout(
            title=f'Percent of Accidents per County 2023 (by {perc_var})',
            xaxis=dict(title='County'),
            yaxis=dict(title='Accidents'),
            height=600,
            width=1200
        )
        
        return fig

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.A('Link to Plotly Dash App', href='http://127.0.0.1:8050'),  # Embed a link to the Dash app
        
        dcc.Dropdown(
            id='dropdown-perc-var',
            options=[{'label': perc_var, 'value': perc_var} for perc_var in df.columns],
            value='Lighting Conditions',
            clearable=False
        ),
        dcc.Graph(id='accidents-percent-plot')
    ])

    @app.callback(
        Output('accidents-percent-plot', 'figure'),
        [Input('dropdown-perc-var', 'value')]
    )
    def update_graph(selected_perc_var):
        return update_plot(selected_perc_var)

    app.run_server(debug=True)

#county_counts.dtypes
def accidents_percent(df, perc_var, drop_na = True):
    county_counts = df.groupby(['County', perc_var]).size().unstack(fill_value=0)
    county_perc= (county_counts.div(county_counts.sum(axis=1), axis=0) * 100).reset_index()
    county_order = df['County'].value_counts().index
    melted_df = pd.melt(county_perc, id_vars=['County'], var_name=perc_var, value_name='Percentage')
    fig = px.bar(melted_df, x = 'County', y = 'Percentage', color = perc_var)
    
    
    # Customize the layout
    fig.update_layout(height = 600, width = 1200,
        title='Percent of Accidents per County 2023',
        xaxis=dict(title='County'),
        yaxis=dict(title='Accidents')
    )
    
    fig.show()

    return melted_df