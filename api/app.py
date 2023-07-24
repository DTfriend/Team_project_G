from flask import Flask, request, jsonify
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error,r2_score
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV



with open("rf_random.pkl", 'rb') as file:
    model = pickle.load(file)

with open("scaler.pkl", 'rb') as file:
    scaler = pickle.load(file)

dep = {
    'CJJ': 0,
    'ICN': 1,
    'KWJ': 2,
    'PUS': 3,
    'TAE': 4,}

arr =  {   'FUK': 0,
    'KIX': 1,
    'NRT': 2,
    'OKA': 3,
    'OSA': 4,
    'SPK': 5
}









#데이터 입력받을 때, 출발시간, 2023-07-24-13:56과 같이 입력 받음. 이를 parsing해야 함




seat_type = {'economy':[1,0,0],'premium':[0,1,1],'business':[0,0,1]}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/echo_call', methods=['GET','POST'])
def predict():
    print(request)
    # Read the parameters from the GET request
    dep_name = dep[request.args.get('dep')]
    print(dep_name)
    arr_name = arr[request.args.get('arr')]
    print(request)
    dep_time = request.args.get('dep_time')
    arr_time = request.args.get('arr_time')
    total_time = request.args.get('total_time')
    arr_month = request.args.get('arr_month')
    arr_weekend = request.args.get('arr_weekend')
    economy = seat_type[request.args.get('type')][0]
    premium = seat_type[request.args.get('type')][1]
    business = seat_type[request.args.get('type')][2]
    via =  request.args.get('via')
    
    # Process the data and make a prediction
    predict_request = np.array([[dep_name, arr_name, dep_time, arr_time, via,total_time, arr_month, arr_weekend, business, economy, premium]])
    predict_request = scaler.transform(predict_request)
    prediction = model.predict(predict_request)
    print(prediction)

    # Return the prediction as a JSON response
    return jsonify({'ticket_prediction': prediction.tolist()})







if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")