import pandas as pd
import numpy as np
import plotly.express as px

# Define your Mapbox token (make sure it's valid)
maps_api_token = "pk.eyJ1IjoiZGVianlvdGljIiwiYSI6ImNsYmFpY3p6OTAwb3IzcW1vMmRkcW15aTMifQ.STVwLHWK7VjBcXA4hvdi6A"

# Load the CSV data
df = pd.read_csv("data/sensor-data.csv")

# Strip leading spaces from column names
df.columns = df.columns.str.strip()

# Remove leading/trailing spaces from 'updated_on' column
df['updated_on'] = df['updated_on'].str.strip()

# Convert 'updated_on' to datetime format
df['updated_on'] = pd.to_datetime(df['updated_on'], format='%I:%M:%S %p')

# Extract necessary columns
velocity = df['Velocity'].to_numpy()
longitude = df['Longitude'].to_numpy()
latitude = df['Latitude'].to_numpy()
updated_on = df['updated_on'].dt.time  # Extract the time portion for animation

# Create a mask to filter out zero values in both longitude and latitude
mask = (longitude != 0.0) & (latitude != 0.0)

# Apply the mask to filter all arrays consistently
longitude = longitude[mask]
latitude = latitude[mask]
velocity = velocity[mask]
updated_on = updated_on[mask]

# Create a DataFrame with Latitude, Longitude, Velocity, and Updated_On for animation
gps_df = pd.DataFrame({
    'latitude': latitude,
    'longitude': longitude,
    'velocity': velocity,
    'updated_on': updated_on  # Use this as the animation frame
})

# Create the scatter mapbox figure with animation using updated_on
fig = px.scatter_mapbox(gps_df, lat="latitude", lon="longitude", color='velocity',
                        animation_frame="updated_on",  # Animate based on Updated_On
                        color_continuous_scale=["black", "purple", "red"], size_max=30, zoom=11.5,
                        height=700, width=700, title='Road Quality Over Time')

# Update layout and mapbox style
fig.update_layout(font_size=16, title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5},
                  title_font_size=24, mapbox_accesstoken=maps_api_token,
                  mapbox_style="mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")

# Update marker size
fig.update_traces(marker=dict(size=6))

# Show the animated figure
fig.show()
