import plotly.express as px
import pandas as pd
import requests
import numpy as np

maps_api_token = "pk.eyJ1IjoiZGVianlvdGljIiwiYSI6ImNsYmFpY3p6OTAwb3IzcW1vMmRkcW15aTMifQ.STVwLHWK7VjBcXA4hvdi6A"
cloud_api = "C4EUQWKMRDFBT1ZX1S14PG"

pod_url = f"http://consentiuminc.online/feeds?receive_key={cloud_api}&all=false"
data = requests.get(pod_url).json()['feeds'][0]

sensor_data = data['sensor_data']
sensor_info = data['sensor_info']
updated_at = data['updated_at']

latitude = np.array([i[0] for i in sensor_data])
longitude = np.array([i[1] for i in sensor_data])
velocity = np.array([i[2] for i in sensor_data])
road_quality = np.array([i[3] for i in sensor_data])

lat = latitude[latitude != 0]
lon = longitude[latitude != 0]
velo = velocity[latitude != 0]
r_q = road_quality[latitude != 0]

# print("Lat: ", latitude[latitude != 0])
# print("Long: ", longitude[latitude != 0])
# print("Velocity: ", velocity[latitude != 0])
# print("Quality: ", road_quality[latitude != 0])

gps_df = pd.DataFrame(list(zip(lat, lon, velo, r_q)),
                      columns=['latitude', 'longitude', 'velocity', 'road_quality'])

fig = px.scatter_mapbox(gps_df, lat="latitude", lon="longitude", color='velocity',
                        color_continuous_scale=["black", "purple", "red"], size_max=30, zoom=11.5,
                        height=700, width=700, title='Road Quality')

fig.update_layout(font_size=16, title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5, },
                  title_font_size=24, mapbox_accesstoken=maps_api_token,
                  mapbox_style="mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")

fig.update_traces(marker=dict(size=6))

fig.write_image('images/gps.png')
fig.show()
