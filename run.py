from flask import Flask, request, render_template
app = Flask(__name__)

from urllib import urlencode
from urllib2 import urlopen
import json

import sunlight

def build_google_geocoding_query(address, region="us", sensor="false"):
    '''
    Returns a url for a lookup with the Google geocoding API
    '''
    return "http://maps.googleapis.com/maps/api/geocode/json?" \
            + urlencode( locals() )

def geocode_address(address):
    '''
    Lookup the lat/lng of an address with the Google geocoding API
    '''
    return json.loads(
        urlopen(
            build_google_geocoding_query(address)
        ).read()
    )

def valid_address_lookup( json ):
    # note - also want to check validity in terms of number of results,
    # multiple results may be returned if address query is ambiguous
    # also might want to check location_type for quality of geocode
    if json['status'] == "OK":
        return True

@app.route('/lookup')
def lookup():
    # Make sure we got input for the address
    valid = True

    if 'lat' in request.args:
        lat = request.args["lat"]
        lng = request.args["lng"]
    elif 'address' in request.args:
        # Geocode the address
        geocode_output = geocode_address( request.args['address'] )
        valid = valid_address_lookup( geocode_output )
        # assuming first returned result is correct
        result = geocode_output["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
    else:
        # undefined query
        pass

    reps = sunlight.congress.legislators_for_lat_lon(lat, lng)
    district = sunlight.congress.districts_for_lat_lon(lat, lng)[0] # default

    return render_template("lookup.html", valid=valid, reps=reps,
            district=district)

@app.route('/')
def address_form():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
