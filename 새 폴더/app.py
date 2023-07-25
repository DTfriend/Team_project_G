'''
  _____  ____     _____ ______ _______      ________ _____  
 |  __ \|  _ \   / ____|  ____|  __ \ \    / /  ____|  __ \ 
 | |  | | |_) | | (___ | |__  | |__) \ \  / /| |__  | |__) |
 | |  | |  _ <   \___ \|  __| |  _  / \ \/ / |  __| |  _  / 
 | |__| | |_) |  ____) | |____| | \ \  \  /  | |____| | \ \ 
 |_____/|____/  |_____/|______|_|  \_\  \/   |______|_|  \_\
                                                         '''

#이 코드는 주기적으로 DB를 업데이트 하는 코드입니다. DB 서버
#그리고 업데이트한 DB에 맞추어, 랜덤 포레스트 모델을 주기적으로(48시간 간격, 2일치 데이터 수집)으로 업데이트 하고, pickle로 만들어, 이를 STREAMLIT 서버에 전달하는 코드입니다
#전달하기 전에 STREAMLIT 서버에 업데이트 한다는 요청을 보냅니다.
#요청을 받으면 STREAMLIT 서버는 기존 모델을 임시 폴더에 이동시킵니다. (계속 작동)
#STREAMLIT 서버는 모델 업데이트가 끝났다는 요청을 받으면 기존 모델을 삭제하고, 새로운 모델을 로드합니다. ("이 과정에서 점검중입니다." 뜨면 되게 할 거 같습니다)
#STREAMLIT 서버에 여러가지 요청을 보내, 제대로 작동하는지 확인. 랜덤하게 10개의 요청을 보냄.
#STREAMLIT 서버가 정상적으로 구동이 확인되면, 정상적이라고 STREAMLIT 서버에 요청을 보내면 될 거 같습니다
#이 과정은 10분정도 걸릴 거 같으므로, 점검 시간이라고 공지를 하면 될 거 같습니다



#의사코드 설정


#크롤링 > (문제 생기면 공지) 및 n번 재시도>history_db 업데이트,Machine_DB 업데이트 (문제 생기면 공지 및 n번 재시도)> 랜덤 포레스트 모델 재학습 (문제 생기면 공지 및 n번 재시도)> STREAMLIT 서버 업데이트 요청 보냄 (문제 생기면 공지 및 n번 재시도)> 랜덤 포레스트 모델 전송(문제 생기면 공지,및 n번 재시도)



#추후 history_db에 충분한 데이터가 쌓이면 딥러닝 모델로 교체


#이 과정을 48시간 간격으로 Latency를 주어, 소모 자원 최소화



#DB 설계
#이 서버는 크롤링을 HEADLESS로 수행합니다. 또한 2일에 한번씩 업데이트하므로, 캡차 걱정없이 크롤링 할 수 있습니다.(과도하지 않게 크롤링)



#db 로드(두 달간의 데이터 저장)



#만약 문제가 발생했을 경우, 디스코드 봇을 사용하여 공지합니다.


#비행기 티켓 58일 후부터 60일까지 크롤링 한후, 기존 db업데이트 하는 코드


from crawling import FlightDataGatherer,HotelDataGatherer,CarRentalDataGatherer
import requests
import traceback
import pandas as pd
import sqlite3
import pandas as pd
from data_preprocessing import HotelAirportDistanceCalculator, Flight_DataPreprocessor
from training_machine import HotelPricePredictor,Flight_ModelTrainer
from sklearn.ensemble import RandomForestRegressor
API_KEYS = '' 



conn = sqlite3.connect('database.db')
flight_data_gatherer = FlightDataGatherer()
hotel_data_gatherer = HotelDataGatherer()
car_rent_gatherer = CarRentalDataGatherer()
calculator = HotelAirportDistanceCalculator(API_KEYS)
predictor = HotelPricePredictor(conn, 'hotel')
conn.close()

try:
    #비행기 데이터 추출중
    flight_data = flight_data_gatherer.gather_data()
    #이거 데이터프레임으로 제작
    conn = sqlite3.connect('database.db')
    flight_data.to_sql('flight', conn, if_exists='append', index=False)
    conn.close()
    preprocessor = Flight_DataPreprocessor('database.db', 'SELECT * FROM flight')
    data = preprocessor.preprocess_data()
    X = data.drop(columns=['가격'])
    y = data['가격']
    trainer = Flight_ModelTrainer(X, y)
    trainer.preprocess_data()
    trainer.train_model(RandomForestRegressor())
    trainer.save_model('/model')

except:
    print('항공기 코드 쪽에 문제 발생')


try:
    #호텔 데이터 추출중
    hotel_data = hotel_data_gatherer.gather_data()
    df = pd.DataFrame(hotel_data, columns=['호텔명', '입실', '퇴실', '지역', '숙박유형', '별점', '등급', '가격'])
    hotel_data = calculator.calculate_distance(df)
    #호텔데이터 DB 에 업로드
    conn = sqlite3.connect('database.db')
    hotel_data.to_sql('hotel', conn, if_exists='append', index=False)
    #맨앞의 2일은 삭제해야 합니다. 추후 추가
    conn.close()
    conn = sqlite3.connect('database.db')
    predictor.load_data()
    predictor.train_model()
    predictor.save_model('/model')
    conn.close()
    #호텔데이터 DB 에 업로드
    #DB에서 자료 추출하여 모델 학습을 진행해야 합니다. training_machine.py의 클래스를 사용합니다 

except:
    print('호텔 쪽 코드에 문제 발생')



try:
    car_rent_data = car_rent_gatherer.gather_data()
except:
    print('랜터카 쪽 코드에 문제 발생')





'''error = traceback.format_exc()

    discord_webhook_url = 'your_discord_webhook_url_here'
    data = {
        'content': f"An error has occurred: {error}"
    }
    requests.post(discord_webhook_url, data=data)'''
