# -*- coding: utf-8 -*-
import json
import flask
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from wordcloud import WordCloud, STOPWORDS
from dash_html_components import Div, Img, Button, H2, H1, P, Hr, A, Span, Label
from wordcloud_template import make_word_cloud
from data.states import state_names
from data.cities import city_names
import requests
from urllib.request import urlopen


EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]



#####################################
# MAP                               #
#####################################
# map need to have lat and long for location
# it works better for scatter location like city
# but for the sake of demo a state, we will use random city location in state
df = pd.read_csv('https://raw.githubusercontent.com/SonQBChau/JSON/main/map.csv')
mapbox_access_token = open("./mapbox_token").read()

map_fig = go.Figure()
for  row in df.itertuples():
    map_fig.add_trace(go.Scattermapbox(
        lon = [row.lon],
        lat = [row.lat],
        mode='markers',
        text = "{} <br> {}".format (row.name , row.count),
        marker=go.scattermapbox.Marker(
            size= int(row.count/20),
            opacity=0.7
        ),
    )
    )
 

map_fig.update_layout(
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='light'
    ),
)



#####################################
# BAR CHART                         #
#####################################
# mostly just need to provide 2 variables: x and y (and type)
# df = pd.DataFrame({
#     "Programming Language": [],
#     "Amount": [],
#     "Type": []
#     })

# calling from API endpoint
# url = 'http://sonchau.pythonanywhere.com/summarizer/api/v1.0/summarize' #replace with real endpoint
# myobj = {'job': 'job_val', 'state': 'state_val', 'city': 'city_val'}

# data = requests.post(url = url, json = myobj)
# jsondata = data.json()
# df = pd.DataFrame.from_dict(jsondata)


df = pd.read_csv('https://raw.githubusercontent.com/SonQBChau/JSON/main/bar_chart.json')
bar_fig = px.bar(df, x="name", y="count", color="type", barmode="group")

#####################################
# SCATTER PLOT                      #
#####################################
# mostly just need 3 variables: x and y and size (and color)
df = pd.read_csv('https://raw.githubusercontent.com/SonQBChau/JSON/main/scatter_plot.json')
scatter_fig = px.scatter(df, x="name", y="size", size='count',color="job",)
 


#####################################
# SUNBURST                          #
#####################################
# sunbrust is good for group and subgroup
# for example, we can have machine learning include all the language inside it
df = pd.read_csv('https://raw.githubusercontent.com/SonQBChau/JSON/main/sunburst.json')
sunburst_fig = px.sunburst(df, path=['job', 'name'], values='count')





#####################################
# WORDCLOUD                         #
#####################################
# just need to provide a text
def make_frequency_and_treemap(data_frame):
    text = urlopen("https://raw.githubusercontent.com/SonQBChau/JSON/main/wordcloud.txt").read().decode('utf-8')
    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=30, max_font_size=90,)
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
    
    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "550", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
  
    return  frequency_figure_data, treemap_figure

def make_wordcloud():
    text = urlopen("https://raw.githubusercontent.com/SonQBChau/JSON/main/wordcloud.txt").read().decode('utf-8')
    imagemaskurl = 'https://raw.githubusercontent.com/SonQBChau/JSON/main/linkedin_logo.png'
    nwords = 200
    customstopwords = ''
    customstopwords = customstopwords.split(',')
 
    children = make_word_cloud(imagemaskurl,  nwords, text,customstopwords)
    

    return children

wordcloud_fig = make_wordcloud()
frequency_fig, treemap_fig = make_frequency_and_treemap(df)



#####################################
# HTML COMPONENTS                   #
#####################################
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("LinkedIn Job Report", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)


#####################################
# MAP COMPONENT                     #
#####################################
MAP_COMPS = [
        dbc.CardHeader(html.H5("Map")),
        dbc.CardBody(
        [
            dcc.Loading(
                id="loading-map",
                children=[
                    # show error if not loaded
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-map",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="map-comps", figure=map_fig),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#####################################
# BAR CHART COMPONENT               #
#####################################
BAR_CHART = [
        dbc.CardHeader(html.H5("Bar Chart")),
        dbc.CardBody(
        [
            dcc.Loading(
                id="loading",
                children=[
                    # show error if not loaded
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-bar",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="table-comps", figure=bar_fig),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#####################################
# SCATTER PLOT COMPONENT            #
#####################################
SCATTER_PLOT = [
    dbc.CardHeader(html.H5("Scatter Plot")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-scatter",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams",
                        color="warning",
                        style={"display": "none"},
                    ),
        
                    dcc.Graph(id="scatter-plot", figure=scatter_fig),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#####################################
# SUNBURST COMPONENT                #
#####################################
SUNBURST = [
    dbc.CardHeader(html.H5("Sunburst Plot")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-sunbrust",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-sunbrust",
                        color="warning",
                        style={"display": "none"},
                    ),
        
                    dcc.Graph(id="sunbrust-plot", figure=sunburst_fig),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#####################################
# WORDCLOUD COMPONENT               #
#####################################
WORDCLOUD = [
    dbc.CardHeader(html.H5("World Cloud")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-frequencies",
                            children=[dcc.Graph(id="frequency_figure", figure=frequency_fig)],
                            type="default",
                        )
                    ),
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[dcc.Graph(id="bank-treemap", figure=treemap_fig)],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud",
                                                children = wordcloud_fig,
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]




#####################################
# BODY CONTAINER                    #
#####################################
BODY = dbc.Container(
    [
        
        dbc.Row([dbc.Col(dbc.Card(MAP_COMPS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(BAR_CHART)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(SCATTER_PLOT)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(SUNBURST)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(WORDCLOUD)),], style={"marginTop": 30}),
     
    ],
    className="mt-12",
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Heroku deployment

app.layout = html.Div(children=[NAVBAR, BODY])



if __name__ == "__main__":
    app.run_server(debug=True)
