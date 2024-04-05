# Import packages
import json
# from sre_parse import State
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import os
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
from dash import callback_context


# print("Current Working Director: ",os.getcwd())
# Read Data (csvs)
df_topic = pd.read_csv('sample_topic.csv') 
df_sentiment = pd.read_csv('sample_sentiment.csv') 
df_duterte = pd.read_csv('s_duterte.csv')
df_government = pd.read_csv('s_government.csv')
df_pandemic = pd.read_csv('s_pandemic.csv')
df_sinovac = pd.read_csv('s_sinovac.csv')
df_vaccination = pd.read_csv('s_vaccination.csv')

#monthly topicsa
df_topic_jan = pd.read_csv('sample_topic_01.csv') 
df_topic_feb = pd.read_csv('sample_topic_02.csv') 
df_topic_mar = pd.read_csv('sample_topic_03.csv') 
df_topic_apr = pd.read_csv('sample_topic_04.csv') 
df_topic_may = pd.read_csv('sample_topic_05.csv') 
df_topic_jun = pd.read_csv('sample_topic_06.csv') 
df_topic_jul = pd.read_csv('sample_topic_07.csv')
df_topic_aug = pd.read_csv('sample_topic_08.csv') 
df_topic_sep = pd.read_csv('sample_topic_09.csv') 
df_topic_oct = pd.read_csv('sample_topic_10.csv') 
df_topic_nov = pd.read_csv('sample_topic_11.csv') 
df_topic_dec = pd.read_csv('sample_topic_12.csv') 

# define colors for the sentiments
sentiment_colors = {
    'positive': 'rgb(0, 255, 0)',   # Green
    'negative': 'rgb(255, 0, 0)',   # Red
    'neutral': 'rgb(0, 0, 255)',    # Blue
    'unclear': 'rgb(128, 128, 128)',# Gray
}

# Initialize the app with Bootstrap CSS for styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# Navbar setup using Dash Bootstrap Components
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/SCL_logo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Geospatial Infodemiology Using Sentiment Analysis and Topic Modelling", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("About Us", href="/about-us")),
                        dbc.NavItem(dbc.NavLink("Model", href="/model")),
                        dbc.NavItem(dbc.NavLink("Research Paper", href="/research-paper")),
                    ], className="ms-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    # color="primary",
    className="custom-navbar-color",
    dark=True,
)


# Layout setup with Navbar and page content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content',className='body-content')
])

# Callback to update page content based on navbar clicks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/model':
        months = ["Jan", "Feb", "Mar", "Apr", "May", "June",
                  "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Button layout
        month_buttons = html.Div(
            [html.Button(month, id={'type': 'month-button', 'index': month}, 
                            className="mb-1", n_clicks=0, style={"width": "100%", "marginBottom": 10, "marginTop": 10}) 
                for month in months],
            style={"display": "flex", "flexDirection": "column"}
        )

        return dmc.Container([
            dmc.Title('Sentiment Analysis Over Topics', color="primary", size="h3"),
            dmc.Grid([
                dmc.Col(month_buttons, span=1),  # Adjust 'span' for the buttons column width
                dmc.Col([
                    dcc.Graph(id='monthly-topic-chart', style={'height': '700px'})  
                ], span=11),
            ]),
            html.Div(id='topic-clicked-content')
        ], fluid=True)
        
    elif pathname == '/about-us':
        return html.Div([
            html.H3('About Us')
            # Include components or content for the 'About Us' section
        ])
    elif pathname == '/research-paper':
        return html.Div([
            html.H3('Research Paper')
            # Include components or content for the 'Research Paper' section
        ])
    else:
        return html.Div([
            html.H3('Home'),
            html.P('Welcome to the Sentiment Analysis Dashboard')
            # Home page content
        ])


# Callback to update sentiment analysis when a topic is clicked
@app.callback(
    Output('topic-clicked-content', 'children'),
    Input('monthly-topic-chart', 'clickData')
)
def display_sentiment_analysis(clickData):
    if clickData is not None:
        selected_topic = clickData['points'][0]['x']

        print(selected_topic)
        match selected_topic:
            case "vaccination":
                selected_topic_data = df_vaccination
            
            case "sinovac":
                selected_topic_data = df_sinovac

            case "government":
                selected_topic_data = df_government
            
            case "duterte":
                selected_topic_data = df_duterte
            
            case "pandemic":
                selected_topic_data = df_pandemic

        # selected_topic_data = df_sentiment[df_sentiment['month'] == selected_topic]  # Use 'month' column for filtering
        # selected_topic_data = df_sentiment  # Use 'month' column for filtering
        return [
            dmc.Title(f'Sentiment Analysis Over Time for {selected_topic}', color="blue", size="h3"),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(
                        id='stacked-bar-chart-sentiment',
                        style={'height': '800px'},
                        figure=create_sentiment_figure(selected_topic_data)
                    )  
                ], span=12),
            ])
        ]
    else:
        return []

# Function to create sentiment figure
def create_sentiment_figure(selected_topic_data):
    # Bar Chart Implementation
    # if 'month' in selected_topic_data.columns:  # Check if 'month' column exists
    #     fig = go.Figure()
    #     sentiments = selected_topic_data.columns[1:] 
    #     months = selected_topic_data['month']  
    #     for i, (month, data) in enumerate(selected_topic_data.iterrows()):
    #         total_responses = sum(data[1:])
    #         cumulative_responses = [0] + list(data[1:].cumsum())
    #         for sentiment, count, cumulative_count in zip(sentiments, data.values[1:], cumulative_responses):
    #             percentage = count / total_responses * 100
    #             trace = go.Bar(
    #                 x=[months[i]],
    #                 y=[count],              
    #                 name=sentiment,
    #                 marker=dict(color=sentiment_colors[sentiment]),
    #                 legendgroup=sentiment,
    #                 hovertemplate=f'{sentiment}: {percentage:.2f}%<extra></extra>'
    #             )
    #             if i == 0:
    #                 trace['showlegend'] = True
    #             else:
    #                 trace['showlegend'] = False
    #             fig.add_trace(trace)
    #             fig.add_annotation(
    #                 x=month,
    #                 y=cumulative_count + count / 2,
    #                 text=f'{percentage:.1f}%',
    #                 showarrow=False,
    #                 font=dict(color='white'),
    #                 align='center',
    #                 yanchor='middle'
    #             )

    #     fig.update_layout(
    #         title='Sentiment Analysis Over Time',
    #         barmode='stack',
    #         xaxis_title='Month',
    #         yaxis_title='Responses',
    #         uniformtext_minsize=8,
    #         uniformtext_mode='hide',
    #         margin=dict(l=50, r=50, t=50, b=50),
    #         bargap=0.1,
    #         showlegend=True,
    #         legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    #     )

    #     return fig
    # else:
    #     return go.Figure()  # Return an empty figure if 'month' column is not found


    #Line Chart Implementation
    fig = go.Figure()

    # Define colors for sentiments
    sentiment_colors = {
        'positive': 'rgb(0, 255, 0)',   # Green
        'negative': 'rgb(255, 0, 0)',   # Red
        'neutral': 'rgb(0, 0, 255)',    # Blue
        'unclear': 'rgb(128, 128, 128)' # Gray
    }

    # Adding a line for each sentiment
    for sentiment in ['positive', 'negative', 'neutral', 'unclear']:
        if sentiment in selected_topic_data.columns:
            fig.add_trace(go.Scatter(
                x=selected_topic_data['month'], 
                y=selected_topic_data[sentiment], 
                mode='lines+markers',
                name=sentiment,
                line=dict(color=sentiment_colors[sentiment]),
                connectgaps=True  # Connects the gap between points if any
            ))

    fig.update_layout(
        title='Sentiment Analysis Over Time',
        xaxis_title='Month',
        yaxis_title='Responses',
        legend_title='Sentiment',
        plot_bgcolor='white',  # Setting background color to white for better readability
        xaxis=dict(showgrid=False),  # Hide the x-axis grid lines for a cleaner look
        yaxis=dict(showgrid=True, gridcolor='lightgray')  # Light gray y-axis grid lines for readability
    )

    return fig

# CALL BACk TO OLD TOPIC FIGURE
# # # Callback to update the topic figure
# @app.callback(
#     Output('stacked-bar-chart-topics', 'figure'),
#     Input('stacked-bar-chart-topics', 'hoverData')
# )
# def update_topic_graph(hoverData):
#     fig = go.Figure()
#     topics = df_topic['topic']  
#     sentiments = df_topic.columns[1:]  
#     for i, (topic, data) in enumerate(df_topic.iterrows()):
#         total_responses = sum(data[1:])
#         cumulative_responses = [0] + list(data[1:].cumsum())
#         for sentiment, count, cumulative_count in zip(sentiments, data.values[1:], cumulative_responses):
#             percentage = count / total_responses * 100
#             trace = go.Bar(
#                 x=[topics[i]],
#                 y=[count],               
#                 name=sentiment,
#                 marker=dict(color=sentiment_colors[sentiment]),
#                 legendgroup=sentiment,
#                 hovertemplate=f'{sentiment}: {percentage:.2f}%<extra></extra>'
#             )
#             if i == 0:
#                 trace['showlegend'] = True
#             else:
#                 trace['showlegend'] = False
#             fig.add_trace(trace)
#             fig.add_annotation(
#                 x=topic,
#                 y=cumulative_count + count / 2,
#                 text=f'{percentage:.1f}%',
#                 showarrow=False,
#                 font=dict(color='white'),
#                 align='center',
#                 yanchor='middle'
#             )

#     fig.update_layout(
#         title='Sentiment Analysis Over Topics',
#         barmode='stack',
#         xaxis_title='Topic',
#         yaxis_title='Responses',
#         uniformtext_minsize=8,
#         uniformtext_mode='hide',
#         margin=dict(l=50, r=50, t=50, b=50),
#         bargap=0.1,
#         showlegend=True,
#         legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
#     )

#     return fig



@app.callback(
    Output('monthly-topic-chart', 'figure'),
    [Input({'type': 'month-button', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True  # Prevents the callback from firing on app load
)
def update_monthly_chart(n_clicks):
    # ctx = dash.callback_context

    if not callback_context.triggered:
        return go.Figure()  # Return an empty figure or some initial setup
        #pass
        #raise PreventUpdate

    button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    month_index = json.loads(button_id)['index']

    # Dictionary mapping month names to their respective dataframes
    df_map = {
        "Jan": df_topic_jan,
        "Feb":df_topic_feb,
        "Mar":df_topic_mar,
        "Apr":df_topic_apr,
        "May":df_topic_may, 
        "June":df_topic_jun,
        "July":df_topic_jul, 
        "Aug":df_topic_aug, 
        "Sep":df_topic_sep, 
        "Oct":df_topic_oct, 
        "Nov":df_topic_nov,  
        "Dec":df_topic_dec, 
    }

        
    selected_df = df_map.get(month_index, df_topic_jan)  # Default to January if not found

    # Now create your figure based on 'selected_df'
    # This assumes you have a function 'create_sentiment_figure' that generates the figure
    figure = create_topic_figure(selected_df)
    return figure

def create_topic_figure(df):
    fig = go.Figure()
    # Assuming 'topic' and sentiment columns exist in your df
    for sentiment in ['positive', 'negative', 'neutral', 'unclear']:
        fig.add_trace(go.Bar(
            x=df['topic'], 
            y=df[sentiment], 
            name=sentiment,
            marker_color=sentiment_colors[sentiment]
        ))

    fig.update_layout(
        barmode='stack',
        title='Monthly Sentiment Analysis Over Top 5 Topics',
        xaxis_title='Topic',
        yaxis_title='Count',
        legend_title='Sentiment'
    )
    return fig


# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
