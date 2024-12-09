import us

# Example major cities for each state
major_cities_by_state = {
    "AL": ["Birmingham", "Montgomery", "Mobile"],
    "AK": ["Anchorage", "Juneau", "Fairbanks"],
    "AZ": ["Phoenix", "Tucson", "Mesa"],
    "AR": ["Little Rock", "Fayetteville", "Fort Smith"],
    "CA": ["Los Angeles", "San Francisco", "San Diego"],
    "CO": ["Denver", "Colorado Springs", "Aurora"],
    "CT": ["Hartford", "New Haven", "Stamford"],
    "DE": ["Wilmington", "Dover"],
    "FL": ["Miami", "Orlando", "Tampa"],
    "GA": ["Atlanta", "Augusta", "Savannah"],
    "HI": ["Honolulu", "Hilo"],
    "ID": ["Boise", "Idaho Falls", "Nampa"],
    "IL": ["Chicago", "Springfield", "Naperville"],
    "IN": ["Indianapolis", "Fort Wayne", "Evansville"],
    "IA": ["Des Moines", "Cedar Rapids", "Davenport"],
    "KS": ["Wichita", "Overland Park", "Kansas City"],
    "KY": ["Louisville", "Lexington", "Bowling Green"],
    "LA": ["New Orleans", "Baton Rouge", "Shreveport"],
    "ME": ["Portland", "Augusta", "Bangor"],
    "MD": ["Baltimore", "Annapolis", "Frederick"],
    "MA": ["Boston", "Worcester", "Springfield"],
    "MI": ["Detroit", "Grand Rapids", "Ann Arbor"],
    "MN": ["Minneapolis", "Saint Paul", "Rochester"],
    "MS": ["Jackson", "Gulfport", "Southaven"],
    "MO": ["Kansas City", "Saint Louis", "Springfield"],
    "MT": ["Billings", "Missoula", "Great Falls"],
    "NE": ["Omaha", "Lincoln", "Bellevue"],
    "NV": ["Las Vegas", "Reno", "Henderson"],
    "NH": ["Manchester", "Nashua", "Concord"],
    "NJ": ["Newark", "Jersey City", "Paterson"],
    "NM": ["Albuquerque", "Santa Fe", "Las Cruces"],
    "NY": ["New York", "Buffalo", "Rochester"],
    "NC": ["Charlotte", "Raleigh", "Greensboro"],
    "ND": ["Fargo", "Bismarck", "Grand Forks"],
    "OH": ["Columbus", "Cleveland", "Cincinnati"],
    "OK": ["Oklahoma City", "Tulsa", "Norman"],
    "OR": ["Portland", "Eugene", "Salem"],
    "PA": ["Philadelphia", "Pittsburgh", "Allentown"],
    "RI": ["Providence", "Newport", "Cranston"],
    "SC": ["Charleston", "Columbia", "Greenville"],
    "SD": ["Sioux Falls", "Rapid City", "Aberdeen"],
    "TN": ["Nashville", "Memphis", "Knoxville"],
    "TX": ["Houston", "Austin", "Dallas"],
    "UT": ["Salt Lake City", "Provo", "Ogden"],
    "VT": ["Burlington", "Montpelier", "Rutland"],
    "VA": ["Richmond", "Virginia Beach", "Norfolk"],
    "WA": ["Seattle", "Spokane", "Tacoma"],
    "WV": ["Charleston", "Huntington", "Morgantown"],
    "WI": ["Milwaukee", "Madison", "Green Bay"],
    "WY": ["Cheyenne", "Casper", "Laramie"],
}

# Generate a list of "City, State Abbreviation" for all major cities
locations = []
for state in us.states.STATES:
    abbreviation = state.abbr
    cities = major_cities_by_state.get(abbreviation, [])
    for city in cities:
        locations.append(f"{city}, {abbreviation}")

# Optionally save to a file
# with open("us_locations.txt", "w", encoding="utf-8") as file:
#     file.write("\n".join(locations))
