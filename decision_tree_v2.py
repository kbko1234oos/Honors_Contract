import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Read the data
stores_data_2017 = pd.read_csv('Starbucks_2017_city_province_v2.csv')
stores_data_2023 = pd.read_csv('Starbucks_2023_city_province_v3.csv')
population_data = pd.read_csv('China_pop_province_2017_2023.csv')
grp_data_2017 = pd.read_csv('China_province_GRP_2017.csv')
grp_data_2023 = pd.read_csv('China_province_GRP_2023.csv')

# Merge the relevant data
merged_data = pd.merge(stores_data_2017, grp_data_2017, on='province')
merged_data = pd.merge(merged_data, population_data, on='province')

# Prepare the feature matrix X and target variable y
X = merged_data[['grp', '2022', '2017']]
y = merged_data['increase_in_stores']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a decision tree regressor model
model = DecisionTreeRegressor()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print("Mean Squared Error (MSE):", mse)
print("R-squared (R2):", r2)
