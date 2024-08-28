import plotly.express as px
import pandas as pd
import requests

# Define your Mapbox token (make sure it's valid)
maps_api_token = "pk.eyJ1IjoiZGVianlvdGljIiwiYSI6ImNsYmFpY3p6OTAwb3IzcW1vMmRkcW15aTMifQ.STVwLHWK7VjBcXA4hvdi6A"

# Define the API endpoint
url = "https://consentiuminc.online/api/board/getdata/recent"
params = {
    "receivekey": "d46549f155ec2f887066c0ace65b86f2",
    "boardkey": "ae62e652d84128de"
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

# Extract Latitude, Longitude, Velocity, and Road Quality (add this if needed)
latitude = float(data['sensors'][0]['sensorData'][2]['data'])
longitude = float(data['sensors'][0]['sensorData'][3]['data'])
velocity = float(data['sensors'][0]['sensorData'][4]['data'])

# Simulating road_quality if it's not in the API response
road_quality = 1.0  # Default value, you can adjust this based on your logic

# Create a DataFrame with Latitude, Longitude, Velocity, and Road Quality
gps_df = pd.DataFrame([[latitude, longitude, velocity]],
                      columns=['latitude', 'longitude', 'velocity'])

print(gps_df)

# Create the scatter mapbox figure
fig = px.scatter_mapbox(gps_df, lat="latitude", lon="longitude", color='velocity',
                        color_continuous_scale=["black", "purple", "red"], size_max=30, zoom=11.5,
                        height=700, width=700, title='Road Quality')

# Update layout and mapbox style
fig.update_layout(font_size=16, title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5},
                  title_font_size=24, mapbox_accesstoken=maps_api_token,
                  mapbox_style="mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")

# Update marker size
fig.update_traces(marker=dict(size=6))


fig.show()
