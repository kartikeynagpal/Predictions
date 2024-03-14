
# Predictions

## Description

This project focuses on implementing a Kalman filter to make predictions based on given datasets. The primary objective is to provide an efficient and accurate method for data prediction and error analysis. 

## Installation Instructions

To set up the "Predictions" environment, follow these steps. Ensure you have Python installed on your system before proceeding.

1. **Create a new virtual environment**:

   ```shell
   python -m venv predenv
   ```

2. **Activate the virtual environment**:
   
   On Windows:
   ```shell
   .\predenv\Scripts\activate
   ```



3. **Install required packages**:

   Ensure you have a `requirements.txt` file in your project directory. Run the following command to install the necessary packages:
   
   ```shell
   pip install -r .\requirements.txt
   ```

## Usage Instructions

Once the installation is complete, you are ready to run the Kalman filter and analyze the error in predictions.

- **Run the Kalman filter**:

  ```shell
  python .\eval.py
  ```

- **Generate the error plot**:

  ```shell
  python .\Errorcalc.py
  ```

These commands will execute the Kalman filter on your dataset and produce an error plot based on the predictions, helping you understand the accuracy and efficiency of the predictions.

