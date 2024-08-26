import json

# Load the GeoJSON file
with open('ne_50m_admin_0_countries.geojson') as f:
    data = json.load(f)

# Filter the features to extract China
china_features = [feature for feature in data['features'] if feature['properties']['ADMIN'] == 'China']

# Create a new GeoJSON object with only China's data
china_geojson = {
    'type': 'FeatureCollection',
    'features': china_features
}

# Save the extracted GeoJSON for China
with open('china_extracted.geojson', 'w') as f:
    json.dump(china_geojson, f)
