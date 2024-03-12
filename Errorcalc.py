import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy.spatial.transform import Rotation as R

def clean_convert(value):
    return float(value.strip('[]'))

def calculate_angular_error(q_actual, q_predicted):
    # Convert quaternions to scipy Rotation objects
    rotation_actual = R.from_quat(q_actual)
    rotation_predicted = R.from_quat(q_predicted)
    # Calculate relative rotation
    relative_rotation = rotation_predicted * rotation_actual.inv()
    # Convert to Euler angles and calculate the magnitude in degrees
    euler_angles = relative_rotation.as_euler('xyz', degrees=True)
    angular_error = np.linalg.norm(euler_angles)
    return angular_error

original_data_dir = 'D:\\Vodafone\\Kalman\\Git\\Prepared data'
predicted_data_dir = 'D:\\Vodafone\\Kalman\\Git\\reprocessed_data'

original_files = glob.glob(os.path.join(original_data_dir, '*.csv'))
predicted_files = glob.glob(os.path.join(predicted_data_dir, '*_future_predictions.csv'))

original_files.sort()
predicted_files.sort()

all_position_errors = []
all_angular_errors = []

for original_file, predicted_file in zip(original_files, predicted_files):
    original_data = pd.read_csv(original_file)
    predicted_data = pd.read_csv(predicted_file)

    for col in predicted_data.columns:
        predicted_data[col] = predicted_data[col].apply(clean_convert)
    
    position_errors = np.sqrt((original_data['PosX'] - predicted_data['Future_PosX'])**2 +
                              (original_data['PosY'] - predicted_data['Future_PosY'])**2 +
                              (original_data['PosZ'] - predicted_data['Future_PosZ'])**2)
    all_position_errors.append(position_errors)
    
    angular_errors = []
    for i in range(len(original_data)):
        q_actual = original_data.loc[i, ['QuatW', 'QuatX', 'QuatY', 'QuatZ']].values
        q_predicted = predicted_data.loc[i, ['Future_QuatW', 'Future_QuatX', 'Future_QuatY', 'Future_QuatZ']].values
        error = calculate_angular_error(q_actual, q_predicted)
        angular_errors.append(error)
    all_angular_errors.append(angular_errors)

plt.figure(figsize=(14, 7))

# Position Error plot
plt.subplot(2, 1, 1)
plt.boxplot(all_position_errors, showfliers=False)
plt.yscale('log')
plt.ylabel('Position Error (meters)')
plt.title('Position Errors for All Traces')

# Angular Error plot
plt.subplot(2, 1, 2)
plt.boxplot(all_angular_errors, showfliers=False)
plt.yscale('log')
plt.ylabel('Angular Error (degrees)')
plt.title('Angular Errors for All Traces')

plt.xticks(range(1, len(original_files) + 1), [os.path.basename(f).replace('.csv', '') for f in original_files], rotation=45, ha='right')
plt.tight_layout()

plt.show()
