from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_mapper")
'''
false positive is troublesome: paradise, $HOME, NWP
record this: use ambiguous threshold to disambiguation
'''
# this threshold determines the ambiguity. Sometimes there are duplicates in names
ambiguous_threshold = 2


def map_location_to_country(location):
    # Normalize and clean the location string
    location = location.lower().strip()
    # This will return all possible locations
    list_location_geo_info = geolocator.geocode(location, exactly_one=False, language='en')
    # If there are no results
    if list_location_geo_info is None:
        return "NOT_AN_ADDRESS"
    # Check ambiguity
    possible_countries = set()
    for location_geo_info in list_location_geo_info:
        country_name = location_geo_info.address.split(',')[-1].strip()
        possible_countries.add(country_name)
    if len(possible_countries) > ambiguous_threshold:
        # it is ambiguous
        return "AMBIGUOUS"
    # if it exists and not ambiguous
    return list_location_geo_info[0].address.split(',')[-1].strip()
