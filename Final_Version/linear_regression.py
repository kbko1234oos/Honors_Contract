import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

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

# Perform linear regression (grp_2023 and pop_diff vs. store_increase)
X = merged_df[['grp_diff_norm', 'pop_diff_norm']].values
y = merged_df['store_inc_norm'].values

X_scaled = np.round((X - X.min()) / (X.max() - X.min()) * (10000 - 1) + 1).astype(int)
y_scaled = np.round((y - y.min()) / (y.max() - y.min()) * (10000 - 1) + 1).astype(int)

# Create a 3D scatter plot
fig = plt.figure(figsize=(14,14))
ax = fig.add_subplot(111, projection='3d')

# Plot the data points with labels
for i, (grp_diff, pop_diff, store_inc, province) in enumerate(zip(X_scaled[:, 0], X_scaled[:, 1], y_scaled, merged_df['province'])):
    ax.scatter(grp_diff, pop_diff, store_inc, c='blue', label=f'Data Point {i+1}')
    ax.text(grp_diff, pop_diff, store_inc, f'{province}', color='black')

# Create and fit the linear regression model
regression_model = LinearRegression()
regression_model.fit(X_scaled, y_scaled)

# Retrieve the coefficients and intercept
coefficients = regression_model.coef_
intercept = regression_model.intercept_

# Create a meshgrid of values
x_grid, y_grid = np.meshgrid(np.linspace(X_scaled[:, 0].min(), X_scaled[:, 0].max(), 100),
                             np.linspace(X_scaled[:, 1].min(), X_scaled[:, 1].max(), 100))
X_grid = np.column_stack((x_grid.flatten(), y_grid.flatten()))

# Predict the values using the linear regression model
y_pred = regression_model.predict(X_grid)

# Reshape the predicted values to match the grid shape
z_grid = y_pred.reshape(x_grid.shape)

# Plot the linear regression plane
ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.5, color='red', label='Linear Regression Plane')

# Set labels for the axes
ax.set_xlabel('GRP Increase Z-Score')
ax.set_ylabel('Popupation Increase Z-Score')
ax.set_zlabel('Num Stores Increase Z-Score')

# Create a separate legend outside the loop
handles, labels = ax.get_legend_handles_labels()
#ax.legend(handles, labels)

# Add the equation of the plane
equation = f"z = {coefficients[0]:.2f} * x + {coefficients[1]:.2f} * y + {intercept:.2f}"
ax.text(X_scaled[:, 0].mean(), X_scaled[:, 1].mean(), y_scaled.mean(), equation, color='black')


# Show the plot
plt.show()

merged_df.to_csv('merged_df.csv', index=False)