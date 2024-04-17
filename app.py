# Import packages
from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px  
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import no_update
from dash.dcc import RadioItems

# DataFrame for topic figure labeled by BertTopic
df_topic = pd.read_csv('Final_Topic_Mbert.csv')

#Data Frame for sentiments labeled by MBert
df_manila_mbert = pd.read_csv('final_mbert_manila.csv')
df_covidnews_mbert = pd.read_csv('final_mbert_covidnews.csv')
df_restrictions_mbert = pd.read_csv('final_mbert_movement.csv')
df_support_mbert = pd.read_csv('final_mbert_support.csv')
df_symptoms_mbert = pd.read_csv('final_mbert_symptoms.csv')

# DataFrame for summary of IATF policies
df_policy2020 = pd.read_csv('covid_policy2020.csv')


# Define colors for each sentiment
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
                        dbc.Col(dbc.NavbarBrand("Geospatial Infodemiology Using Sentiment Analysis and Topic Modeling", className="ms-2")),
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
                        # dbc.NavItem(dbc.NavLink("Home", href="/")),
                        # dbc.NavItem(dbc.NavLink("About Us", href="/about-us")),
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
    html.Div(id='page-content',className='body-content'),
    html.Div(id='hover-info', className='hover-info', style={
        'position' : 'absolute',
        'bottom' : '20px',
        'right' : '20px',
        'max-width' : '300px',
        'background' : 'white',
        'padding' : '10px',
        'border-radius' : '5px',
        'border' : '1px solid #ccc',
        'display' : 'none'
    })
])

# Callback to update page content based on navbar clicks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/model':
        return dmc.Container([
            dmc.Title('Sentiment Analysis Over Topics', color="blue", size="h3"),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(id='stacked-bar-chart-topics', style={'height': '700px'})  
                ], span=12),
            ]),
            html.Div(id='topic-clicked-content')
        ], fluid=True)
    elif pathname == '/about-us':
        return html.Div([
            html.H3('About Us')
        ])
    elif pathname == '/research-paper':
        return html.Div([
            html.H3('Research Paper')
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
    Input('stacked-bar-chart-topics', 'clickData')
)
def display_sentiment_analysis(clickData):
    if clickData is not None:
        selected_topic = clickData['points'][0]['x']

        match selected_topic:
            case "Manila":
                selected_topic_data = df_manila_mbert
            
            case "Covid-19 News/Updates":
                selected_topic_data = df_covidnews_mbert

            case "Online Community Support":
                selected_topic_data = df_support_mbert
            
            case "Movement Restrictions":
                selected_topic_data = df_restrictions_mbert
            
            case "COVID-19 Symptoms":
                selected_topic_data = df_symptoms_mbert

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
                hoverinfo='text', #added this
                hovertemplate='%{y}: ' + sentiment + '<extra></extra>', # added this
                connectgaps=True, # Connects the gap between points if any
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

@app.callback(
        Output('hover-info','children'),
        Output('hover-info', 'style'),
        Input('stacked-bar-chart-sentiment', 'hoverData'),
)
def display_hover_info(hoverData):
    month_descriptions = df_policy2020.set_index('Month')['Description'].to_dict()

    if hoverData:
        hover_month = hoverData['points'][0]['x']
        description = month_descriptions.get(hover_month, "No description")
        return description, {
            'display': 'block',
            'position': 'absolute',
            'top': '130%',
            'right': '100px',
            'width': '200px',
            'min-height': '100px',
            'background': 'rgba(255, 255, 255, 0.9)',
            'padding': '10px',
            'border-radius': '10px',
            'border': '1px solid #ddd',
            'box-shadow': '0px 4px 6px rgba(0,0,0,0.1)',
        }
    else:
        return "", {'display': 'none'}  # Hide the div


# Callback to update the topic figure
@app.callback(
    Output('stacked-bar-chart-topics', 'figure'),
    Input('stacked-bar-chart-topics', 'hoverData')
)
def update_topic_graph(hoverData):
    fig = go.Figure()
    topics = df_topic['topic']  
    sentiments = df_topic.columns[1:]  
    for i, (topic, data) in enumerate(df_topic.iterrows()):
        total_responses = sum(data[1:])
        cumulative_responses = [0] + list(data[1:].cumsum())
        for sentiment, count, cumulative_count in zip(sentiments, data.values[1:], cumulative_responses):
            percentage = count / total_responses * 100
            trace = go.Bar(
                x=[topics[i]],
                y=[count],               
                name=sentiment,
                marker=dict(color=sentiment_colors[sentiment]),
                legendgroup=sentiment,
                hovertemplate=f'{sentiment}: {percentage:.2f}%<extra></extra>'
            )
            if i == 0:
                trace['showlegend'] = True
            else:
                trace['showlegend'] = False
            fig.add_trace(trace)
            fig.add_annotation(
                x=topic,
                y=cumulative_count + count / 2,
                text=f'{percentage:.1f}%',
                showarrow=False,
                font=dict(color='white'),
                align='center',
                yanchor='middle'
            )

    fig.update_layout(
        title='Sentiment Analysis Over Topics',
        barmode='stack',
        xaxis_title='Topic',
        yaxis_title='Responses',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(l=50, r=50, t=50, b=50),
        bargap=0.1,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
