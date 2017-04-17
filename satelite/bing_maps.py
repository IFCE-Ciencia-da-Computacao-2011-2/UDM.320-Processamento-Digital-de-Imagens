import requests
from PIL import Image

class BingMaps:
    
    def __init__(self, key):
        self.key = key
        
    def image(self, lat, long, zoom=15, width=1024, height=768):
        url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{},{}/{}?mapSize={},{}&key={}'
        url = url.format(lat, long, zoom, width, height, self.key)
        
        response = requests.get(url, stream=True)
        return Image.open(response.raw)
