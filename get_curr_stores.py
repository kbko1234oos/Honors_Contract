import csv
import json

# Read the JSON data from a file
with open('china_stores.json', 'r') as file:
    json_data = file.read()

# Assuming the JSON data is stored in a variable called 'json_data'
data = json.loads(json_data)

# Check if the data is within an array or a single object
if isinstance(data["data"], list):
    entries = data["data"]
else:
    entries = [data["data"]]


# Write latitudes and longitudes to a CSV file
filename = "china_stores_v4.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["StoreName", "CityName", "StreetAddress1", "StreetAddress2", "StreetAddress3", "latitude", "longitude"])  # Write header

    for entry in entries:
        coordinates = entry["coordinates"]
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        name = entry["name"]
        address = entry["address"]
        cityname = address["city"]
        StreetAddress1 = address["streetAddressLine1"]
        StreetAddress2 = address["streetAddressLine2"]
        StreetAddress3 = address["streetAddressLine3"]
        writer.writerow([name, cityname, StreetAddress1, StreetAddress2, StreetAddress3, latitude, longitude])

print(f"Data written to {filename} successfully.")
