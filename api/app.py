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


with open("car_rf_random.pkl", 'rb') as file:
    car_model = pickle.load(file)


dep = {
    'CJJ': 0,
    'ICN': 1,
    'KWJ': 2,
    'PUS': 3,
    'TAE': 4,}

arr =  {   'CTS': 0, #훗카이도,
    'FUK': 1,#후쿠오카
    'KIX': 2,#오사카
    'NRT': 3,#도쿄
    'OKA': 4,#오키나와
    'OSA': 5,#오사카
    'SPK':6#삿포로
}

ticket_arr =  {   'CTS': 0,
    'FUK': 1,
    'KIX': 2,
    'NRT': 3,
    'OKA': 4,
    'OSA': 5,
    'SPK':6
}

rent_arr =  {   'CTS': 4, #훗카이도,
    'FUK': 1,#후쿠오카
    'KIX': 2,#오사카
    'NRT': 0,#도쿄
    'OKA': 3,#오키나와
    'OSA': 2,#오사카
    'SPK':1#삿포로
}



rent_arr_air =  {   'CTS': 1,
    'FUK': 4,
    'KIX': 2,
    'NRT': 0,
    'OKA': 3,
    'OSA': 2,
    'SPK':1
}


rentercar_name = {
    '86 ': 0,
    'C-HR ': 1,
    'eK 왜건 ': 2,
    '노트 5도어 ': 3,
    '노트 E-파워 ': 4,
    '데미오 ': 5,
    '델리카 8인승 ': 6,
    '라이즈 ': 7,
    '랜드 크루저 프라도 ': 8,
    '레보그 ': 9,
    '루미 ': 10,
    '무브 콘테 ': 11,
    '벨파이어 8인승 ': 12,
    '복시 ': 13,
    '비츠 ': 14,
    '스마일 ': 15,
    '스텝왜건 ': 16,
    '스텝왜건 8인승 ': 17,
    '시엔타 ': 18,
    '시엔타 6인승 ': 19,
    '아쿠아 ': 20,
    '알파드 ': 21,
    '알파드 8인승 ': 22,
    '야리스 ': 23,
    '엔박스 ': 24,
    '왜건 R ': 25,
    '이클립스 크로스 ': 26,
    '임프레자 ': 27,
    '캠리 ': 28,
    '코롤라 ': 29,
    '코롤라 필더 ': 30,
    '큐브 ': 31,
    '크라운 ': 32,
    '태프트 ': 33,
    '프리우스 ': 34,
    '피트 ': 35,
    '하이에이스 그랜드 캐빈 ': 36,
    '허슬러 ': 37
}

size = ['RV' 'SUV' '경형' '대형' '소형' '왜건' '준중형' '중형']

size_dict = {size[i]: i for i in range(len(size))}

insurance = ['면책커버보험 포함' '스탠다드플랜 포함' '프리미엄플랜 포함']
insurance_dict = {insurance[i]: i for i in range(len(insurance))}
brand = ['닛산' '다이하쓰' '도요타' '마쯔다' '미쓰비시' '스바루' '스즈키' '혼다']

brand_dict = {brand[i]:i for i in range(len(brand))}

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
    ticket_predict_request = np.array([[dep_name, arr_name, dep_time, arr_time, via,total_time, arr_month, arr_weekend, business, economy, premium]])
    ticket_predict_request = scaler.transform(ticket_predict_request)
    ticket_prediction = model.predict(ticket_predict_request)
    #############렌트카######################
    arr_name = rent_arr[request.args.get('arr')]
    arr_name_air = rent_arr_air[request.args.get('arr')]
    rentename = rentercar_name[request.args.get('rentcar_name')]
    size = size_dict[request.args.get('size')]
    insurance = insurance_dict[request.args.get('insurance')]
    brand = brand_dict[request.args.get('brand')]
    rent_request = np.array([arr_name,arr_name_air,rentename,size,insurance,brand])
    rent_prediction = car_model.predict(rent_request)
    print(ticket_prediction)
    print(rent_prediction)
    # Return the prediction as a JSON response
    return jsonify({'ticket_prediction': ticket_prediction.tolist(),'rend_prediction':rent_prediction.tolist()})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")