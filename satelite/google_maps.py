import requests
from PIL import Image

class GoogleMaps:
    
    def __init__(self, key):
        self.key = key
        
    def image(self, lat, long, zoom=15, width=1024, height=768):
        url  = 'https://maps.googleapis.com/maps/api/staticmap?'
        url += 'center={latitude},{longitude}&size={width}x{height}&zoom={zoom}'
        #url += '&maptype=satellite'
        url += '&style=road|visibility:on'        
        url += '&style=element:labels|visibility:off'
        url += '&style=feature:poi|visibility:off'
        url += '&style=feature:water|visibility:off'
        url += '&style=feature:landscape.man_made|visibility:off'
        url += '&key={api}'

        url = url.format(**{
            'api': self.key,
            'latitude': lat,
            'longitude': long,
            'zoom': zoom,
            'width': width,
            'height': height
        })
        
        response = requests.get(url, stream=True)
        return Image.open(response.raw)
