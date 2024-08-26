import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import scipy.stats

# Read the 2023 dataset
df_2023 = pd.read_csv('Starbucks_2023_city_province_v3.csv')

# Read the 2017 dataset
df_2017 = pd.read_csv('Starbucks_2017_city_province_v2.csv')

# Read the GRP datasets
df_grp_2017 = pd.read_csv('China_province_GRP_2017.csv')
df_grp_2023 = pd.read_csv('China_province_GRP_2023.csv')

# Read the population dataset
df_population = pd.read_csv('China_pop_province_2017_2023.csv')

# Calculate the number of stores in each year by province
num_stores_2023 = df_2023.groupby('province').size().reset_index(name='num_stores_2023')
num_stores_2017 = df_2017.groupby('province').size().reset_index(name='num_stores_2017')

# Merge the datasets based on the province column
merged_df = pd.merge(num_stores_2023, num_stores_2017, on='province')

# Merge GRP data
grp_merge = pd.merge(df_grp_2023, df_grp_2017, on='province')
grp_merge['grp_diff'] = grp_merge['grp_x'] - grp_merge['grp_y']

merged_df = pd.merge(merged_df, grp_merge[['province', 'grp_diff']], on='province')

# Merge pop data
df_population['pop_diff'] = df_population['2022'] - df_population['2017']

merged_df = pd.merge(merged_df, df_population[['province', 'pop_diff']], on='province')

# Merge store data
store_merge = pd.merge(num_stores_2023, num_stores_2017, on='province')
store_merge['store_inc'] = store_merge['num_stores_2023'] - store_merge['num_stores_2017']
merged_df = pd.merge(merged_df, store_merge[['province', 'store_inc']], on='province')

print(merged_df)

# Normalize using z-scores
merged_df['grp_diff_norm'] = scipy.stats.zscore(merged_df['grp_diff'])
merged_df['pop_diff_norm'] = scipy.stats.zscore(merged_df['pop_diff'])
merged_df['store_inc_norm'] = scipy.stats.zscore(merged_df['store_inc'])

print(merged_df)

# Create input variables (X) and target variable (y)
X = merged_df[['grp_diff_norm','pop_diff_norm']]
y = merged_df['store_inc_norm']

# Split the data into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=32)

# Create a decision tree regressor
regressor = DecisionTreeRegressor()

# Fit the model on the training data
regressor.fit(X_train, y_train)

# Make predictions on the test data
y_pred = regressor.predict(X_test)

# Calculate mean squared error on the test data
mse = mean_squared_error(y_test, y_pred)

# Print the mean squared error
print('Mean Squared Error:', mse)

# Add the predicted store increase to the merged dataset
merged_df['predicted_store_inc'] = regressor.predict(X)

# Save the merged dataset with predictions to a CSV file
merged_df.to_csv('merged_dataset_with_predictions.csv', index=False)
