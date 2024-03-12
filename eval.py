import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter
import os
import glob

class KalmanCSVProcessor:
    def __init__(self, pred_window=1, dt=0.1, output_dir='processed_data'):  
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

    def predict_future_states(self, steps):
        future_states = []
        for _ in range(steps):
            self.kf.predict()
            future_states.append(self.kf.x.copy())
        return future_states

    def process_file(self, filepath):
        data = pd.read_csv(filepath)
        dim_x = 14
        dim_z = 7

        self.setup_kalman_filter(dim_x, dim_z)

        predictions, future_predictions = [], []
        for _, row in data.iterrows():
            z = np.array([row['PosX'], row['PosY'], row['PosZ'], row['QuatW'], row['QuatX'], row['QuatY'], row['QuatZ']])
            self.kf.predict()
            self.kf.update(z)
            predictions.append(self.kf.x[:dim_z].tolist())

            steps = int(self.pred_window / self.dt)
            future_states = self.predict_future_states(steps)
            future_predictions.append([fs[:dim_z].tolist() for fs in future_states])

        result_df = pd.DataFrame(predictions, columns=['PosX', 'PosY', 'PosZ', 'QuatW', 'QuatX', 'QuatY', 'QuatZ'])
        future_pred_path = os.path.join(self.output_dir, os.path.splitext(os.path.basename(filepath))[0] + '_future_predictions.csv')
        flat_future_predictions = [item for sublist in future_predictions for item in sublist]
        future_result_df = pd.DataFrame(flat_future_predictions, columns=['Future_PosX', 'Future_PosY', 'Future_PosZ', 'Future_QuatW', 'Future_QuatX', 'Future_QuatY', 'Future_QuatZ'])
        result_path = os.path.join(self.output_dir, os.path.splitext(os.path.basename(filepath))[0] + '_filtered.csv')
        result_df.to_csv(result_path, index=False)
        future_result_df.to_csv(future_pred_path, index=False)
        print(f"Processed and saved to: {result_path}")
        print(f"Future predictions saved to: {future_pred_path}")

def main():
    processor = KalmanCSVProcessor(pred_window=1, dt=0.1)
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Prepared data')

    for filepath in glob.glob(os.path.join(directory_path, '*.csv')):
        processor.process_file(filepath)

if __name__ == "__main__":
    main()
