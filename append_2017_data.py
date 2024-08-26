import pandas as pd

def add_english_names(city_csv_file, data_csv_file):
    # Read the city mapping CSV file into a pandas DataFrame
    city_mapping_df = pd.read_csv(city_csv_file)

    # Read the data CSV file into a pandas DataFrame
    df = pd.read_csv(data_csv_file)

    # Merge the data DataFrame with the city mapping DataFrame
    merged_df = pd.merge(df, city_mapping_df, on='CityName', how='left')

    # Rename the columns in the merged DataFrame
    merged_df.rename(columns={'English_Province': 'English_Province',
                              'English_City': 'English_City'}, inplace=True)

    # Save the modified DataFrame back to the data CSV file
    merged_df.to_csv(data_csv_file, index=False)

# Usage example
add_english_names('China_provinces_cities.csv', 'Starbucks_2017_city_province_v2.csv')
