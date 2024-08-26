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

    # Calculate the absolute number increase in store counts
    number_increase = store_counts2 - store_counts1

    # Add the increase in store counts as a new column in the second stores data
    stores_data2['NumberIncrease'] = number_increase.reindex(store_counts2.index)

    # Save the modified stores data to the CSV file
    stores_data2.to_csv(stores_file2, index=False)

provinces_file1 = 'China_province_GRP_2017.csv'
stores_file1 = 'Starbucks_2017_city_province_v2.csv'
provinces_file2 = 'China_province_GRP_2023.csv'
stores_file2 = 'Starbucks_2023_city_province_v3.csv'

create_store_graph(provinces_file1, stores_file1, provinces_file2, stores_file2)