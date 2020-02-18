import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

@st.cache
def load_data():

    breeds_coords = pd.read_csv('data/breeds_coords.csv')
    attribs_coords = pd.read_csv('data/attribs_coords.csv')

    returns = (attribs_coords, breeds_coords)
    return returns

attribs_coords, breeds_coords = load_data()

st.subheader("Attribute Score by City")

attrib_selection = st.selectbox(" ", attribs_coords.Attribute.unique())

token = 'pk.eyJ1IjoibWljYWVsYW1jY2FsbCIsImEiOiJjazRrNHFkaGsyMm94M21xZHozazd5ODg3In0.aRQ114nE0WKa7AnPMGiRzQ'

@st.cache
def plot_attributemap():
    data = attribs_coords[attribs_coords.Attribute == attrib_selection]
    attributemap = go.Figure([go.Scattermapbox(
        lat = data.lat, 
        lon = data.lon,
        hoverinfo= "text", 
        text = ['{} Score: {}'.format(*i) for i in zip(data['City'], data['Average'].astype('float'))],
        mode = 'markers', 
        marker = dict(
            size = 8,
            opacity = 0.8,
            symbol = 'circle',
            color = data['Average'],
            colorscale = 'viridis',
            colorbar_title="Score"))])

    attributemap.update_layout(
        autosize=False,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=35,
                lon=-98
            ),
            pitch=0,
            zoom=2,
            style='light'
        ),
    )

    return attributemap


attributemap = plot_attributemap()


st.plotly_chart(attributemap)

st.subheader("Breed Counts by City")


breed_selection = st.selectbox(" ", breeds_coords.Breed.unique())


@st.cache
def plot_breedmap():
    data = breeds_coords[breeds_coords.Breed == breed_selection]
    breedmap = go.Figure(go.Scattermapbox(
        lat = data.lat, 
        lon = data.lon,
        hoverinfo = 'text',
        text = ['{}: {} dogs'.format(*i) for i in zip(data['City'], data['Reg Count'].astype('int'))], 
        mode = 'markers', 
        marker = dict(
            size = 8,
            opacity = 0.8,
            symbol = 'circle',
            color = data['Reg Count'],
            colorscale = 'viridis',
            colorbar_title = "Count")))

    breedmap.update_layout(
        autosize=False,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=35,
                lon=-98
            ),
            pitch=0,
            zoom=2,
            style='light'
        ),
    )

    return breedmap


breedmap = plot_breedmap()

st.plotly_chart(breedmap)


# city_selection = st.radio('City', ['NYC', 'Seattle', 'Edmonton', 'Adelaide'])


# st.markdown(city_selection + ' top 5 breeds')

# st.table(combined_breeds_coords[(combined_breeds_coords.City == city_selection)][['Breed','Count']].nlargest(6, ['Count']).set_index('Breed'))

# st.markdown(city_selection + ' attribute score')

# st.table(combined_attrib_coords[(combined_attrib_coords.City == city_selection)][['Attribute', 'Average']].set_index('Attribute'))