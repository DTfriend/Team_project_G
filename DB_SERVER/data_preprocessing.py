##이 코드는 데이터를 리스트 형태로 받아 랜덤포레스트 모델에 맞게 전처리하는 코드입니다. 그런 다음, DB에 업로드 합니다.


'''
  ______ _ _       _     _     _____        _                                            _             
 |  ____| (_)     | |   | |   |  __ \      | |                                          (_)            
 | |__  | |_  __ _| |__ | |_  | |  | | __ _| |_ __ _   _ __  _ __ ___   ___ ___  ___ ___ _ _ __   __ _ 
 |  __| | | |/ _` | '_ \| __| | |  | |/ _` | __/ _` | | '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ \ / _` |
 | |    | | | (_| | | | | |_  | |__| | (_| | || (_| | | |_) | | | (_) | (_|  __/\__ \__ \ | | | | (_| |
 |_|    |_|_|\__, |_| |_|\__| |_____/ \__,_|\__\__,_| | .__/|_|  \___/ \___\___||___/___/_|_| |_|\__, |
              __/ |                                   | |                                         __/ |
             |___/                                    |_|                                        |___/ 
'''


import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import sqlite3
import googlemaps
from datetime import datetime
from haversine import haversine
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import *

class Flight_DataPreprocessor:
    def __init__(self, db_path, query):
        self.db_path = db_path
        self.query = query

    def price_to_int(self, price_str):
        return int(price_str.replace('편도', '').replace(',', '').replace('원~', '').strip())

    def time_to_min(self, time_str):
        hours, minutes = map(int, time_str.replace('시간', '').replace('분', '').split())
        return hours * 60 + minutes

    def dir_to_int(self, dir_str):
        if dir_str =='직항':
            return 0
        elif dir_str =='경유 1':
            return 1
        else:
            return 2

    def preprocess_data(self):
        conn = sqlite3.connect(self.db_path)
        
        df = pd.read_sql_query(self.query, conn)
        conn.close()

        df['가격'] = df['가격'].apply(self.price_to_int)
        df['총 소요 시간'] = df['총 소요 시간'].apply(self.time_to_min)
        df['항공편'] = df['항공편'].apply(self.dir_to_int)

        encoder = OrdinalEncoder()
        encoded_data = encoder.fit_transform(df[['출발지','도착지']])
        df[['출발지','도착지']] = encoded_data

        df['날짜'] = pd.to_datetime(df['날짜'])
        df['Monthly'] = df['날짜'].dt.month
        df['Weekend'] = (5 - df['날짜'].dt.dayofweek) % 7
        df['출발시간'] = df['출발시간'].str.split(':').str[0].astype(int)
        df['도착시간'] = df['도착시간'].str.split(':').str[0].astype(int)

        grouped = df.groupby('좌석등급')
        economy_df = grouped.get_group('economy')
        premium_df = grouped.get_group('premium')
        business_df = grouped.get_group('business')

        data = pd.concat([economy_df, premium_df, business_df])
        data = data.drop('날짜',axis=1)
        data = pd.get_dummies(data, columns=['좌석등급'])

        return data

'''
 __                    __                __              __              __                                          __                            __ 
/  |                  /  |              /  |            /  |            /  |                                        /  |                          /  |
$$ |____    ______   _$$ |_     ______  $$ |        ____$$ |  ______   _$$ |_     ______         __    __   ______  $$ |  ______    ______    ____$$ |
$$      \  /      \ / $$   |   /      \ $$ |       /    $$ | /      \ / $$   |   /      \       /  |  /  | /      \ $$ | /      \  /      \  /    $$ |
$$$$$$$  |/$$$$$$  |$$$$$$/   /$$$$$$  |$$ |      /$$$$$$$ | $$$$$$  |$$$$$$/    $$$$$$  |      $$ |  $$ |/$$$$$$  |$$ |/$$$$$$  | $$$$$$  |/$$$$$$$ |
$$ |  $$ |$$ |  $$ |  $$ | __ $$    $$ |$$ |      $$ |  $$ | /    $$ |  $$ | __  /    $$ |      $$ |  $$ |$$ |  $$ |$$ |$$ |  $$ | /    $$ |$$ |  $$ |
$$ |  $$ |$$ \__$$ |  $$ |/  |$$$$$$$$/ $$ |      $$ \__$$ |/$$$$$$$ |  $$ |/  |/$$$$$$$ |      $$ \__$$ |$$ |__$$ |$$ |$$ \__$$ |/$$$$$$$ |$$ \__$$ |
$$ |  $$ |$$    $$/   $$  $$/ $$       |$$ |______$$    $$ |$$    $$ |  $$  $$/ $$    $$ |______$$    $$/ $$    $$/ $$ |$$    $$/ $$    $$ |$$    $$ |
$$/   $$/  $$$$$$/     $$$$/   $$$$$$$/ $$//      |$$$$$$$/  $$$$$$$/    $$$$/   $$$$$$$//      |$$$$$$/  $$$$$$$/  $$/  $$$$$$/   $$$$$$$/  $$$$$$$/ 
                                           $$$$$$/                                       $$$$$$/          $$ |                                        
                                                                                                          $$ |                                        
                                                                                                          $$/                                         

'''


class HotelAirportDistanceCalculator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=self.api_key)

    def get_place_location(self, place_name):
        geocode_result = self.gmaps.geocode(place_name, region='jp')
        return geocode_result[0]['geometry']['location']

    def get_nearest_airport(self, location):
        places_result = self.gmaps.places_nearby(location=location, radius=1000000, type='airport')
        airport_name = places_result['results'][0]['name']
        airport_location = places_result['results'][0]['geometry']['location']
        return airport_name, airport_location

    def get_distance_and_time(self, origin, destination):
        now = datetime.now()
        directions_result = self.gmaps.directions(origin, destination, departure_time=now)
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']
        return distance, duration

    def calculate_distance(self, hotel_data):
        hotel_dict = {i: ['',0,0] for i in list(set(hotel_data["호텔명"]))}
        airport_list = ['Narita International Airport','Kansai International Airport','New Chitose Airport','Naha Airport','Fukuoka Airport','Tokyo International Airport']
        airport_dict = {i:self.get_place_location(i) for i in airport_list}


        for name in hotel_dict:
            try:
                hotel_location = self.get_place_location(name)
                min_distance = float('inf')
                nearest_airport = ''
                for airport_name, airport_location in airport_dict.items():
                    distance = haversine((hotel_location['lat'], hotel_location['lng']), (airport_location['lat'], airport_location['lng']))
                    if distance < min_distance:
                        min_distance = distance
                        nearest_airport = airport_name
                time = self.get_distance_and_time(hotel_location, airport_dict[nearest_airport])
                hotel_dict[name][0] = nearest_airport
                hotel_dict[name][1] = min_distance
                hotel_dict[name][2] = time
                print(name, hotel_dict[name])
            except IndexError:
                print('재검색이 필요합니다')
                continue

        hotel_data['가장가까운공항'] = ''
        hotel_data['가장가까운공항과의거리'] = 0
        hotel_data['가장가까운공항까지시간'] = 0

        for i in range(len(hotel_data['호텔명'])):
            hotel_data['가장가까운공항'].iloc[i] =  hotel_dict[hotel_data['호텔명'].iloc[i]][0]
            if hotel_dict[hotel_data['호텔명'].iloc[i]][0] == '':
                continue
            else:
                hotel_data['가장가까운공항과의거리'].iloc[i] =  hotel_dict[hotel_data['호텔명'].iloc[i]][2][0]
                hotel_data['가장가까운공항까지시간'].iloc[i] =  hotel_dict[hotel_data['호텔명'].iloc[i]][2][1]

        s = 0
        for i in range(len(hotel_data['호텔명'])):
            if hotel_data['가장가까운공항'].iloc[i] == '':
                print(hotel_data['호텔명'].iloc[i])
                s +=1

        hotel_data = hotel_data[hotel_data['가장가까운공항'] != '']

        return hotel_data





class CarPreprocessor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.encoder = OrdinalEncoder()
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        self.car = pd.read_sql_query("SELECT * from car", conn)
        conn.close()

    def preprocess(self):
        self.car.loc[self.car['오일'].isna(), '오일'] = '휘발유'
        mapping = {
            'FUKUOKA': '후쿠오카',
            'OKINAWA': '오키나와',
            'TOKYO': '도쿄',
            'OSAKA': '오사카',
            'SAPPORO': '삿포로'
        }
        self.car['지역'] = self.car['지역'].map(mapping)
        self.car['공항'] = self.car['공항'].str.extract(r'\((.*?)\)')
        self.car[['브랜드', '이름']] = self.car['이름'].str.split(' ', 1, expand=True)
        self.car['이름'] = self.car['이름'].str.replace('또는 동급차종', '')
        self.car['가격'] = self.car['가격'].str.replace(',', '').str.extract(r'(\d+)').astype(int)
        self.car = self.car.drop(['회사', '오일', '기어'], axis=1)
        self.car['제한인원수'] = self.car['제한인원수'].str.extract(r'(\d+)').astype(int)
        self.car['대여일'] = self.car['대여일'].str.replace('-','').astype(int)
        self.car['반납일'] = self.car['반납일'].str.replace('-','').astype(int)
        ordinal_cols = ['지역',	'공항',	'이름',	'크기',	'보험',	'브랜드']
        self.car[ordinal_cols] = self.encoder.fit_transform(self.car[ordinal_cols])

    def get_preprocessed_data(self):
        return self.car