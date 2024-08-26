import pandas as pd
import matplotlib.pyplot as plt

def create_store_graph(provinces_file, stores_file):
	# Read provinces and GDP CSV file
	provinces_data = pd.read_csv(provinces_file, encoding='latin-1')
	stores_data = pd.read_csv(stores_file, encoding='latin-1')

	# Convert 'province' column in stores_data to lowercase for case-insensitive matching
	#stores_data['province'] = stores_data['province'].str.lower()
	# Merge provinces and stores data based on province name
	merged_data = pd.merge(provinces_data, stores_data, left_on='province', right_on='province', how='outer')

	# Group by province and count the number of stores
	store_counts = merged_data.groupby('province')['StoreName'].count()

	# Sort provinces in decreasing order based on store counts
	store_counts = store_counts.sort_values(ascending=False)

	# Plotting the graph
	plt.figure(figsize=(10, 6))
	plt.bar(store_counts.index, store_counts.values)
	plt.xlabel('Province')
	plt.ylabel('Number of Stores')
	plt.title('Number of Stores in Each Province')
	plt.xticks(rotation=90)
	plt.tight_layout()
	plt.show()

# Example usage
provinces_file = 'China_province_GDPs.csv'
stores_file = 'Starbucks_2023_city_province.csv'
create_store_graph(provinces_file, stores_file)
