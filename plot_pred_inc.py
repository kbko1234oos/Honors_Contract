import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('merged_dataset_with_predictions.csv')

# Set the province as the index
df.set_index('province', inplace=True)

# Sort the DataFrame by store_increase in ascending order
df.sort_values('store_inc_norm', inplace=True)

# Get the necessary columns
provinces = df.index
store_increase = df['store_inc_norm']
predicted_store_increase = df['predicted_store_inc']

# Set the figure size
plt.figure(figsize=(10, 6))

# Plot the store_increase
plt.bar(provinces, store_increase, label='Actual Store Increase')

# Plot the predicted_store_increase
plt.plot(provinces, predicted_store_increase, marker='o', linestyle='-', color='red', label='Predicted Store Increase')

# Add labels to the points
for i in range(len(provinces)):
    plt.text(provinces[i], store_increase[i], str(int(store_increase[i])), ha='center', va='bottom')

# Set the title and labels
plt.title('Store Increase by Province')
plt.xlabel('Province')
plt.ylabel('Number of Stores')

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45)

# Add a legend
plt.legend()

# Display the plot
plt.show()
