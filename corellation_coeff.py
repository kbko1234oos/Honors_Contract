import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

# Read the stores and provinces CSV files
stores_data_2017 = pd.read_csv('Starbucks_2017_city_province_v2.csv')
stores_data_2023 = pd.read_csv('Starbucks_2023_city_province_v3.csv')

population_data = pd.read_csv('China_pop_province_2017_2023.csv')

# Aggregate the number of stores per province for both 2017 and 2023
stores_count_2017 = stores_data_2017.groupby('province').size().reset_index(name='number_of_stores_2017')
stores_count_2023 = stores_data_2023.groupby('province').size().reset_index(name='number_of_stores_2023')

# Merge the two dataframes on the province column
merged_data = pd.merge(stores_count_2017, stores_count_2023, on='province')

# Merge the population data
population_data.columns = ['province', '2022', '2017']
merged_data = pd.merge(merged_data, population_data, on='province')

# Read the grp data for 2017 and 2023
grp_data_2017 = pd.read_csv('China_province_GRP_2017.csv')
grp_data_2023 = pd.read_csv('China_province_GRP_2023.csv')

# Calculate the difference in grp and population between 2017 and 2022
grp_data_2017['grp_2023'] = grp_data_2023['grp'] - grp_data_2017['grp']
population_data['pop_diff'] = population_data['2022'] - population_data['2017']

# Merge the grp and population differences with the merged_data DataFrame
merged_data = pd.merge(merged_data, grp_data_2017[['province', 'grp_2023']], on='province')
merged_data = pd.merge(merged_data, population_data[['province', 'pop_diff']], on='province')

# Calculate store_increase using number_of_stores_2017 and number_of_stores_2023
merged_data['store_increase'] = merged_data['number_of_stores_2023'] - merged_data['number_of_stores_2017']

# Convert the columns to numeric
merged_data['store_increase'] = pd.to_numeric(merged_data['store_increase'], errors='coerce')
merged_data['grp_2023'] = pd.to_numeric(merged_data['grp_2023'], errors='coerce')
merged_data['pop_diff'] = pd.to_numeric(merged_data['pop_diff'], errors='coerce')

# Normalize the data
scaler = MinMaxScaler()
columns_to_normalize = ['grp_2023', 'pop_diff', 'store_increase']
merged_data[columns_to_normalize] = scaler.fit_transform(merged_data[columns_to_normalize])

# Perform linear regression (grp_2023 and pop_diff vs. store_increase)
X = merged_data[['grp_2023', 'pop_diff']].values
y = merged_data['store_increase'].values

# Create and fit the linear regression model
regression_model = LinearRegression()
regression_model.fit(X, y)

# Retrieve the coefficients and intercept
slope = regression_model.coef_
intercept = regression_model.intercept_

# Get the R-squared value
r_squared = regression_model.score(X, y)

# Reshape X[:, 0]
x_values = X[:, 0].reshape(-1, 1)

# Create a scatter plot (grp_2023 vs. store_increase)
plt.scatter(x_values[:, 0], y, label='Data Points')

# Plot the line of best fit
plt.plot(x_values[:, 0], slope[0] * x_values[:, 0] + slope[0] * x_values[:, 0] + intercept, color='red', label='Line of Best Fit')


# Add labels to each point on the graph
for i, province in enumerate(merged_data['province']):
    plt.annotate(province, (x_values[i], y[i]))

# Add labels and title
plt.xlabel('grp_2023')
plt.ylabel('store_increase')
plt.title('Correlation between Store Increase and GRP 2023')

plt.legend()
plt.show()


# Print the results
print("Slope:", slope)
print("Intercept:", intercept)
print("R-squared:", r_squared)

merged_data.to_csv('merged_data.csv', index=False)
