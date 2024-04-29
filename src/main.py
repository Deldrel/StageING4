from flask import Flask, render_template
import googlemaps
import os

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


@app.route('/')
def index():
    # Coordinates for Lyon, France
    lyon_center = (45.7640, 4.8357)

    # Fetch pathways in Lyon, France
    # Note: This is a placeholder, you need to adjust the query based on your needs
    directions_result = gmaps.directions(lyon_center,
                                         lyon_center,
                                         mode="walking",
                                         waypoints=["via:45.7700,4.8300", "via:45.7500,4.8500"])

    # Extract polyline data from directions result
    polyline = directions_result[0]['overview_polyline']['points']

    return render_template('map.html', api_key=GOOGLE_MAPS_API_KEY, polyline=polyline)


if __name__ == '__main__':
    app.run(debug=True)
