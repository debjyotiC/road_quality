import requests
from flask import Flask, render_template, jsonify

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
        update_at = data['sensors'][0]['sensorData'][2]['updatedAt']

        return {
            'latitude': latitude,
            'longitude': longitude,
            'velocity': velocity,
            'date':update_at
        }
    else:
        return None


@app.route('/data')
def get_data():
    data = get_latest_data()
    print(data)
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html', mapbox_token=maps_api_token)


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
