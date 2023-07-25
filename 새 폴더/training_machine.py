import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error
import numpy as np
from sklearn.model_selection import GridSearchCV
# Define the class

class HotelPricePredictor:
    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name
        self.model = None


    def calculate_remaining_weekends(self, date):
        day_of_week = date.weekday()
        if day_of_week < 4:  # For Monday to Thursday
            return 2 - day_of_week
        elif day_of_week == 4:  # For Friday
            return 1
        else:  # For Saturday and Sunday
            return 0

    def convert_time_to_minutes(self, time_string):
        pattern = r'(?:(\d+) hours)? ?(?:(\d+) mins)?'
        match = re.match(pattern, time_string)
        hours = match.group(1)
        mins = match.group(2)
        hours_to_mins = int(hours) * 60 if hours else 0
        mins = int(mins) if mins else 0
        return hours_to_mins + mins


    def load_data(self):
        # Load data from the database into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)

        # Data preprocessing
        df['입실'] = pd.to_datetime(df['입실'])
        df['월'] = df['입실'].dt.month
        df['일'] = df['입실'].dt.day
        df['weekend'] = df['입실'].apply(self.calculate_remaining_weekends)
        df['가장 가까운 공항과의 거리'] = df['가장 가까운 공항과의 거리'].str.replace(' km', '').astype(float)
        df['가장 가까운 공항까지 시간'] = df['가장 가까운 공항까지 시간'].apply(self.convert_time_to_minutes)
        df = df.drop(columns=['입실', '퇴실'])
        # Remove outliers
        Q1 = df['가격'].quantile(0.15)
        Q3 = df['가격'].quantile(0.85)
        IQR = Q3 - Q1
        outliers = (df['가격'] < (Q1 - 1.5 * IQR)) | (df['가격'] > (Q3 + 1.5 * IQR))
        df_no_outliers = df[~outliers]

        # Encode categorical variables
        df_no_outliers = pd.get_dummies(df_no_outliers)

        # Split the dataset into features (X) and target (y)
        self.X = df_no_outliers.drop(columns=['가격'])
        self.y = df_no_outliers['가격']

    def train_model(self):
        # Split the dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        # Initialize the RandomForestRegressor
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)

        # Predict the target on the test set
        y_pred = self.model.predict(X_test)

        # Calculate the root mean square error (RMSE)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        # Calculate the R2 score
        r2 = r2_score(y_test, y_pred)

        return rmse, r2

    def save_model(self, path):
        with open(os.path.join(path, 'random_forest_model.pkl'), 'wb') as file:
            pickle.dump(self.model, file)



class Flight_ModelTrainer:
    def __init__(self, X, y, test_size=0.2, random_state=42):
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None

    def preprocess_data(self):
        # Split the dataset into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )

        # Scale the features
        scaler = RobustScaler()
        scaler.fit(self.X_train)
        self.X_train = scaler.transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def train_model(self, ml_model):
        # Train the model
        self.model = ml_model.fit(self.X_train, self.y_train)

        # Make predictions
        self.predictions = self.model.predict(self.X_test)

        # Calculate metrics
        r2score = r2_score(self.y_test, self.predictions)
        print("r2 score is: {}".format(r2score))
        print('MAE:{}'.format(mean_absolute_error(self.y_test, self.predictions)))
        print('MSE:{}'.format(mean_squared_error(self.y_test, self.predictions)))
        print('RMSE:{}'.format(np.sqrt(mean_squared_error(self.y_test, self.predictions))))

    def save_model(self, path):
        # Save the model as a pickle file
        with open(os.path.join(path, 'trained_model.pkl'), 'wb') as file:
            pickle.dump(self.model, file)
