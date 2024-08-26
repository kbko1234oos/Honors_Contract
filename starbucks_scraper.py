import requests
import re
import pandas as pd

# Define the latitude and longitude ranges
latitude_range = range(16, 56)
longitude_range = range(39, 138)

# Set the zoom value
zoom = 12

# Define the processResponse function
def processResponse(r):
	# Parse out each store's info
	stores = re.findall(r'\"storeNumber\":.*?\"slug\"', r)
	storeInfo = []
	for store in stores:
		# Parse out info about each store
		info = re.findall(r'\"storeNumber\":\"(.*?)\".*?\"name\":\"(.*?)\".*?\"latitude\":(.*?),.*?\"longitude\":(.*?),.*?\"city\":\"(.*?)\".*?\"countrySubdivisionCode\":\"(.*?)\".*?\"postalCode\":\"(.*?)\"', store)
		if info:
			storeInfo.append(list(info[0]))
	return storeInfo

# Initialize the list to store store information
allStores = []

# Make requests with varying latitude and longitude values
for lat in latitude_range:
	for lon in longitude_range:
		# Calculate the latitude and longitude values with increments
		latitude = lat + 0.3
		longitude = lon + 0.35

		# Construct the URL with the latitude, longitude, and zoom values
		url = f'https://www.starbucks.com/store-locator?map={latitude},{longitude},{zoom}z'
		print(f"Processing latitude/longitude: {latitude} {longitude}")

		# Make the request
		r = requests.get(url)

		# Check if the request was successful
		if r.status_code == 200:
			# Process the response to extract store information
			storeInfoList = processResponse(r.text)

			# Append the store information to the list
			allStores += storeInfoList

# Create a DataFrame from the store information
dfSbux = pd.DataFrame(allStores, columns=['id', 'strLocation', 'latitude', 'longitude', 'city', 'state', 'zip'])

# Convert latitude and longitude columns to numeric types
dfSbux['latitude'] = pd.to_numeric(dfSbux['latitude'])
dfSbux['longitude'] = pd.to_numeric(dfSbux['longitude'])

# Save the DataFrame to a CSV file
dfSbux.to_csv('starbucks_stores.csv', index=False)

# Print the total number of Starbucks stores retrieved
print("Total number of Starbucks stores retrieved:", len(dfSbux))
print("Data saved to starbucks_stores.csv")
