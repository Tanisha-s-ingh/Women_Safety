import geocoder

def get_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng
    else:
        return None
