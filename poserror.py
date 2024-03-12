import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Function to remove brackets and convert string to float
def clean_convert(value):
    return float(value.strip('[]'))

# Directories
original_data_dir = 'D:\\Vodafone\\Kalman\\Git\\Prepared data'
predicted_data_dir = 'D:\\Vodafone\\Kalman\\Git\\reprocessed_data'

# Get all CSV files from both directories
original_files = glob.glob(os.path.join(original_data_dir, '*.csv'))
predicted_files = glob.glob(os.path.join(predicted_data_dir, '*_future_predictions.csv'))

# Sort the files to ensure matching pairs
original_files.sort()
predicted_files.sort()

# Initialize a list to hold all position errors
all_position_errors = []

# Process each file
for original_file, predicted_file in zip(original_files, predicted_files):
    # Load the original and predicted data
    original_data = pd.read_csv(original_file)
    predicted_data = pd.read_csv(predicted_file)

    # Clean the predicted data by removing brackets and converting to float
    for col in predicted_data.columns:
        predicted_data[col] = predicted_data[col].apply(clean_convert)

    # Calculate position errors for each file and add to the list
    position_errors = np.sqrt((original_data['PosX'] - predicted_data['Future_PosX'])**2 +
                              (original_data['PosY'] - predicted_data['Future_PosY'])**2 +
                              (original_data['PosZ'] - predicted_data['Future_PosZ'])**2)
    all_position_errors.append(position_errors)

# Plotting the position errors as box plots
plt.figure(figsize=(14, 7))

# Box plot for position errors
plt.subplot(2, 1, 1)
plt.boxplot(all_position_errors, showfliers=False)
plt.yscale('log')
plt.ylabel('meters')
plt.title('Position Errors for All Traces')

# Adjustments to make the plot more readable
plt.xticks(range(1, len(original_files) + 1), [os.path.basename(f).replace('.csv', '') for f in original_files], rotation=45, ha='right')
plt.tight_layout()

plt.show()
