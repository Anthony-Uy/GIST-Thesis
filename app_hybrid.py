# Import packages
from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px  
import dash_mantine_components as dmc

# Read data
df_topic = pd.read_csv('sample_topic.csv') 
df_sentiment = pd.read_csv('sample_sentiment.csv') 
df_duterte = pd.read_csv('s_duterte.csv')
df_government = pd.read_csv('s_government.csv')
df_pandemic = pd.read_csv('s_pandemic.csv')
df_sinovac = pd.read_csv('s_sinovac.csv')
df_vaccination = pd.read_csv('s_vaccination.csv')


# Define colors for each sentiment
sentiment_colors = {
    'positive': 'rgb(0, 255, 0)',   # Green
    'negative': 'rgb(255, 0, 0)',   # Red
    'neutral': 'rgb(0, 0, 255)',    # Blue
    'unclear': 'rgb(128, 128, 128)',# Gray
}

# Initialize the app 
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dmc.Container([
    dmc.Title('Sentiment Analysis Over Topics', color="blue", size="h3"),
    dmc.Grid([
        dmc.Col([
            dcc.Graph(id='stacked-bar-chart-topics', style={'height': '700px'})  
        ], span=12),
    ]),
    html.Div(id='topic-clicked-content')
], fluid=True)

# Callback to update sentiment analysis when a topic is clicked
@app.callback(
    Output('topic-clicked-content', 'children'),
    Input('stacked-bar-chart-topics', 'clickData')
)
def display_sentiment_analysis(clickData):
    if clickData is not None:
        selected_topic = clickData['points'][0]['x']

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
    if 'month' in selected_topic_data.columns:  # Check if 'month' column exists
        fig = go.Figure()
        sentiments = selected_topic_data.columns[1:] 
        months = selected_topic_data['month']  
        for i, (month, data) in enumerate(selected_topic_data.iterrows()):
            total_responses = sum(data[1:])
            cumulative_responses = [0] + list(data[1:].cumsum())
            for sentiment, count, cumulative_count in zip(sentiments, data.values[1:], cumulative_responses):
                percentage = count / total_responses * 100
                trace = go.Bar(
                    x=[months[i]],
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
                    x=month,
                    y=cumulative_count + count / 2,
                    text=f'{percentage:.1f}%',
                    showarrow=False,
                    font=dict(color='white'),
                    align='center',
                    yanchor='middle'
                )

        fig.update_layout(
            title='Sentiment Analysis Over Time',
            barmode='stack',
            xaxis_title='Month',
            yaxis_title='Responses',
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            margin=dict(l=50, r=50, t=50, b=50),
            bargap=0.1,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )

        return fig
    else:
        return go.Figure()  # Return an empty figure if 'month' column is not found



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
