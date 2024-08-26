import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_store_graph(provinces_file1, stores_file1, provinces_file2, stores_file2):
	# Read the first set of provinces and stores data
	provinces_data1 = pd.read_csv(provinces_file1, encoding='latin-1')
	stores_data1 = pd.read_csv(stores_file1, encoding='latin-1')

	# Merge provinces and stores data based on province name
	merged_data1 = pd.merge(provinces_data1, stores_data1, left_on='province', right_on='province', how='outer')
	merged_data1.rename(columns={'ï»¿StoreName': 'StoreName'}, inplace=True)

	# Group by province and count the number of stores in the first dataset
	store_counts1 = merged_data1.groupby('province')['StoreName'].count()

	# Sort provinces in decreasing order based on store counts
	store_counts1 = store_counts1.sort_values(ascending=False)

	# Read the second set of provinces and stores data
	provinces_data2 = pd.read_csv(provinces_file2, encoding='latin-1')
	stores_data2 = pd.read_csv(stores_file2, encoding='latin-1')

	# Merge provinces and stores data based on province name
	merged_data2 = pd.merge(provinces_data2, stores_data2, left_on='province', right_on='province', how='outer')
	merged_data2.rename(columns={'ï»¿StoreName': 'StoreName'}, inplace=True)

	# Group by province and count the number of stores in the second dataset
	store_counts2 = merged_data2.groupby('province')['StoreName'].count()

	# Sort provinces in decreasing order based on store counts
	store_counts2 = store_counts2.sort_values(ascending=False)

	# Get the unique provinces
	provinces = np.union1d(store_counts1.index, store_counts2.index)

	# Set the width of each bar
	bar_width = 0.35

	# Set the positions of the bars on the x-axis
	r1 = np.arange(len(provinces))
	r2 = [x + bar_width for x in r1]

	# Create a figure and axis objects
	fig, ax = plt.subplots(figsize=(12, 6))

	# Plot the number of stores in the first dataset
	if not 'Inner Mongolia' in store_counts1.index or not 'InnerMongolia' in store_counts1.index:
		ax.bar(r1, store_counts1[provinces], color='skyblue', width=bar_width, label='2017')

	# Plot the number of stores in the second dataset
	if not 'Inner Mongolia' in store_counts2.index or not 'InnerMongolia' in store_counts2.index:
		ax.bar(r2, store_counts2[provinces], color='red', width=bar_width, label='2023')

	# Set the x-axis tick positions and labels
	ax.set_xticks(np.arange(len(provinces)))
	ax.set_xticklabels(provinces, rotation=90)

	# Set the axis labels and title
	ax.set_xlabel('Province')
	ax.set_ylabel('Number of Stores')
	ax.set_title('Number of Stores in Each Province')

	# Add a legend
	ax.legend()

	plt.tight_layout()
	plt.show()

# Example usage
provinces_file1 = 'China_province_GRP_2017.csv'
stores_file1 = 'Starbucks_2017_city_province_v2.csv'
provinces_file2 = 'China_province_GRP_2023.csv'
stores_file2 = 'Starbucks_2023_city_province_v3.csv'

create_store_graph(provinces_file1, stores_file1, provinces_file2, stores_file2)
