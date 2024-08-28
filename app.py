import plotly.express as px
import pandas as pd
import requests
from flask import Flask, render_template_string, jsonify

# Define your Mapbox token (make sure it's valid)
maps_api_token = "pk.eyJ1IjoiZGVianlvdGljIiwiYSI6ImNsYmFpY3p6OTAwb3IzcW1vMmRkcW15aTMifQ.STVwLHWK7VjBcXA4hvdi6A"

# Define the API endpoint
url = "https://consentiuminc.online/api/board/getdata/recent"
params = {
    "receivekey": "d46549f155ec2f887066c0ace65b86f2",
    "boardkey": "ae62e652d84128de"
}

# Initialize Flask app
app = Flask(__name__)


def get_latest_data():
    # Make the API request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract Latitude, Longitude, Velocity
        latitude = float(data['sensors'][0]['sensorData'][2]['data'])
        longitude = float(data['sensors'][0]['sensorData'][3]['data'])
        velocity = float(data['sensors'][0]['sensorData'][4]['data'])

        return {
            'latitude': latitude,
            'longitude': longitude,
            'velocity': velocity
        }
    else:
        return None


@app.route('/data')
def get_data():
    data = get_latest_data()
    return jsonify(data)


@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Road Quality Map</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                }
                #map {
                    width: 100%;
                    height: 100%;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>

            <script type="text/javascript">
                // Your Mapbox token
                const mapboxToken = "{{ mapbox_token }}";

                function initializeMap(latitude, longitude, velocity) {
                    const data = [{
                        type: 'scattermapbox',
                        lat: [latitude],
                        lon: [longitude],
                        mode: 'markers+text',
                        marker: {
                            size: 14,
                            color: 'red',
                            opacity: 0.8,
                        },
                        text: [velocity.toFixed(2)],
                        textposition: 'top center',
                        textfont: {
                            size: 16,
                            color: 'white'
                        }
                    }];

                    const layout = {
                        title: 'Road Quality',
                        autosize: true,
                        mapbox: {
                            style: 'mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw',
                            accesstoken: mapboxToken,
                            center: {lat: latitude, lon: longitude},
                            zoom: 11.5,
                        },
                        margin: { t: 0, r: 0, b: 0, l: 0 }  // Remove margins to make it full screen
                    };

                    Plotly.newPlot('map', data, layout);
                }

                function updateMap(latitude, longitude, velocity) {
                    const update = {
                        lat: [[latitude]],
                        lon: [[longitude]],
                        text: [velocity.toFixed(2)],
                        marker: { color: 'red' },
                    };
                    Plotly.restyle('map', update);
                }

                function fetchDataAndUpdateMap() {
                    $.getJSON("/data", function(data) {
                        if (data) {
                            const latitude = data.latitude;
                            const longitude = data.longitude;
                            const velocity = data.velocity;
                            updateMap(latitude, longitude, velocity);
                        }
                    });
                }

                $(document).ready(function() {
                    // Fetch initial data and initialize the map
                    $.getJSON("/data", function(data) {
                        if (data) {
                            const latitude = data.latitude;
                            const longitude = data.longitude;
                            const velocity = data.velocity;
                            initializeMap(latitude, longitude, velocity);
                        }
                    });

                    // Refresh map every 10 seconds
                    setInterval(fetchDataAndUpdateMap, 10000);
                });
            </script>
        </body>
    </html>
    """, mapbox_token=maps_api_token)


# Run the app
if __name__ == '__main__':
    app.run()
