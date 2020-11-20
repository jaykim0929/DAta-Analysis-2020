# conda install -c anaconda flask
from flask import Flask
import folium

app = Flask(__name__)

@app.route('/')
def index():
    start_coords = (37.240867, 127.177968)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)