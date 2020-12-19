from dash_html_components import Div, Img, Button, H2, H1, P, Hr, A, Span, Label, Details, Summary
from wordcloud import WordCloud, ImageColorGenerator
import io
import base64
from PIL import Image
import plotly.graph_objs as go
import re
import numpy as np
import requests
import dash_bootstrap_components as dbc


def make_word_cloud(imagemaskurl, nwords, text, customstopwords):
    if imagemaskurl is not None and imagemaskurl != '':
        try:
            r = requests.get(imagemaskurl)
            b = r.content
            image_bytes = io.BytesIO(b)
            im = Image.open(image_bytes).convert('RGBA')
            canvas = Image.new('RGBA', im.size, (255, 255, 255, 255))
            canvas.paste(im, mask=im)
            mask = np.array(canvas)
            width, height = im.size
        except:
            mask = None
            text = 'Invalid Image Mask!'
    else:
        mask = None
    from wordcloud import STOPWORDS
    STOPWORDS = list(STOPWORDS)

    for word in customstopwords:
        STOPWORDS.append(word)
        STOPWORDS.append(word + 's')
        STOPWORDS.append(word + "'s")
 
  
    cloud = WordCloud(width=width, height=height, mask=mask, background_color='white', ).generate(text)


    try:
        coloring = ImageColorGenerator(mask)
        cloud.recolor(color_func=coloring)
    except:
        pass
    image = cloud.to_image()

    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    data_uri = base64.b64encode(byte_io.getvalue()).decode('utf-8').replace('\n', '')
    src = 'data:image/png;base64,{0}'.format(data_uri)
    x = np.array(list(cloud.words_.keys()))
    y = np.array(list(cloud.words_.values()))
    order = np.argsort(y)[::-1]
    x = x[order]
    y = y[order]
    trace = go.Bar(x=x, y=y)
    layout = go.Layout(title='Relative frequency of words')
    fig = go.Figure(data=[trace], layout=layout)
    children = [
        Img(src=src, width=image.size[0], height=image.size[1],
            style={'maxWidth': '100%', 'height': 'auto',
                   'margin': '0 auto', 'display': 'block'}),
    ]

    return children
