from flask import Flask, request, render_template
app = Flask(__name__)

from urllib import urlencode
from urllib2 import urlopen
import json

import sunlight

app.debug = True # never use in production

def build_google_geocoding_query(address, region="us", sensor="false"):
    '''
    Returns a url suitable for performing a lookup with the Google geocoding
    API
    '''
    return "http://maps.googleapis.com/maps/api/geocode/json?" + urlencode( locals() )

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

def lookup_reps( gc ):
    '''
    Return a list of representatives based on address
    Use the Sunlight Congress API - we can lookup by zip code or lat/lng
    '''
    # assuming first returned result is correct
    result = gc["results"][0]
    lat = result["geometry"]["location"]["lat"]
    lng = result["geometry"]["location"]["lng"]

    # lookup reps for this lat/lng with Sunlight Congress API
    representatives = sunlight.congress.legislators_for_lat_lon(lat, lng)
    return str(representatives)

@app.route('/lookup')
def lookup():
    # Make sure we got input for the address
    try:
        address = request.args['address']
    except KeyError:
        return "You don't live nowhere!"

    # Geocode the address
    gc = geocode_address( address )
    if valid_address_lookup( gc ):
        return lookup_reps( gc )
    else:
        return "We couldn't resolve that address!"

@app.route('/')
def address_form():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
