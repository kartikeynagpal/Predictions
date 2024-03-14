import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter
import os
import glob

class KalmanCSVProcessor:
    def __init__(self, pred_window=1, dt=0.1, output_dir='reprocessed_data'):
        self.kf = None
        self.pred_window = pred_window
        self.dt = dt
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure the output directory exists

    def setup_kalman_filter(self, dim_x, dim_z):
        self.kf = KalmanFilter(dim_x=dim_x, dim_z=dim_z)
        self.kf.F = np.eye(dim_x)
        for i in range(dim_x // 2):
            self.kf.F[i, i + dim_x // 2] = self.dt
        self.kf.H = np.eye(dim_z, dim_x)  # Measurement function
        self.kf.P *= 1000.
        self.kf.R = np.eye(dim_z) * 5  # Measurement uncertainty
        self.kf.Q = np.eye(dim_x) * 0.1  # Process uncertainty

    def process_file(self, filepath):
        data = pd.read_csv(filepath)
        dim_x = 14
        dim_z = 7

        self.setup_kalman_filter(dim_x, dim_z)

        predictions = []
        for _, row in data.iterrows():
            z = np.array([row['PosX'], row['PosY'], row['PosZ'], row['QuatW'], row['QuatX'], row['QuatY'], row['QuatZ']])
            self.kf.predict()
            self.kf.update(z)
            predictions.append(self.kf.x[:dim_z].tolist())  # Save only the immediate next state

        # Save predictions as future predictions
        future_pred_path = os.path.join(self.output_dir, os.path.splitext(os.path.basename(filepath))[0] + '_future_predictions.csv')
        future_result_df = pd.DataFrame(predictions, columns=['Future_PosX', 'Future_PosY', 'Future_PosZ', 'Future_QuatW', 'Future_QuatX', 'Future_QuatY', 'Future_QuatZ'])
        future_result_df.to_csv(future_pred_path, index=False)
        print(f"Future predictions saved to: {future_pred_path}")

def main():
    processor = KalmanCSVProcessor(pred_window=1, dt=0.1)
    directory_path = 'Prepared data'  # Adjusted for clarity

    for filepath in glob.glob(os.path.join(directory_path, '*.csv')):
        processor.process_file(filepath)

if __name__ == "__main__":
    main()
