import streamlit as st
import pandas as pd
import streamlit_survey as ss
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page





st.set_page_config(
    page_title="Survey",
    page_icon="✅",
    initial_sidebar_state = "collapsed"
)



# 사이트 헤드라인
st.title('🛫 일본 여행 비용 예측 🗾')
# 이모티콘
# https://kr.piliapp.com/emoji/list/

st.markdown("""
 * AI를 통해 항공권, 숙박, 렌트카의 비용을 예측해드립니다.
 * 아래의 질문에 답해주세요!
""")


#Airport
######################################
# Load the saved model
# air_model = joblib.load("air_test.pkl")

# Read the car data from CSV
air = pd.read_csv("data2/air_original_k2j.csv",encoding='CP949')


#매핑 데이터
city_to_airport_code_kr = {
    '인천': 'ICN',
    '청주': 'CJJ',
    '대구': 'TAE',
    '광주': 'KWJ',
    '부산': 'PUS'
}

city_to_airport_code_jp = {
    '삿포로': 'CTS',
    '후쿠오카': 'FUK',
    '도쿄(하네다)': 'HND',
    '오사카(간사이)': 'KIX',
    '도쿄(나리타)': 'NRT',
    '오키나와': 'OKA'
}



korea_air = {'CJJ':0, 'ICN':1, 'KWJ':2, 'PUS':3, 'TAE':4}
japan_air = {'CTS':0, 'FUK':1, 'HND':2, 'KIX':3, 'NRT':4, 'OKA':5}

seat_class_mapping = {
    'economy': 0,
    'premium': 1,
    'business': 2,
    'first': 3

}
flight_mapping = {'직항': 0, '1회경유': 1, '그외': 2}


#Hotel
######################################
hotel = pd.read_csv("data2/hotel_total_final.csv")
# 지역명을 숫자로 매핑하는 딕셔너리
category_mapping = {'게스트하우스,캡슐호텔,호스텔':0, '리조트,펜션,료칸':1, '호텔':2}
hotel_grade_mapping ={'1성급':1,'2성급':2,'3성급':3,'4성급':4,'5성급':5,}

#입실	퇴실	지역	숙박유형	별점	등급	가장 가까운 공항까지 시간



#Rent Car
######################################

# Read the car data from CSV
car = pd.read_csv("data2/car_total.csv")

# 지역명을 숫자로 매핑하는 딕셔너리를 생성합니다
region_mapping = {
    '도쿄': 0,'삿포로': 1,'오사카': 2,'오키나와': 3,'후쿠오카': 4}
# 지역명을 숫자로 매핑하는 딕셔너리
air_mapping = {'CTS': 0,'FUK': 1,'HND': 2,'KIX': 3,'KKJ': 4,'NRT': 5,'OKA': 6}

# 자동차명을 숫자로 매핑하는 딕셔너리
car_mapping = {
   '86': 0,'C-HR': 1,'eK 왜건': 2,'노트 5도어': 3,'노트 E-파워': 4,'데미오': 5,'델리카 8인승': 6,'라이즈': 7,'랜드 크루저 프라도': 8,'레보그': 9,
   '루미': 10,'무브 콘테': 11,'벨파이어 8인승': 12,'복시': 13,'비츠': 14,'스마일': 15,'스텝왜건': 16,'스텝왜건 8인승': 17,'시엔타': 18,'시엔타 6인승': 19,
   '아쿠아': 20,'알파드': 21,'알파드 8인승': 22,'야리스': 23,'엔박스': 24,'왜건 R': 25,'이클립스 크로스': 26,'임프레자': 27,'캠리': 28,'코롤라': 29,
   '코롤라 필더': 30,'큐브': 31,'크라운': 32,'태프트': 33,    '프리우스': 34,'피트': 35,'하이에이스 그랜드 캐빈': 36,'허슬러': 37
}
# 차량 크기를 숫자로 매핑하는 딕셔너리
car_size_mapping = {'RV': 0,'SUV': 1,'경형': 2,'대형': 3,'소형': 4,'왜건': 5,'준중형': 6,'중형': 7}

# 보험을 숫자로 매핑하는 딕셔너리
insurance_mapping = {'면책커버보험 포함': 0,'스탠다드플랜 포함': 1,'프리미엄플랜 포함': 2}

# 브랜드명을 숫자로 매핑하는 딕셔너리
brand_mapping = {'닛산': 0,'다이하쓰': 1,'도요타': 2,'마쯔다': 3,'미쓰비시': 4,'스바루': 5,'스즈키': 6,'혼다': 7}








with st.expander(" ", expanded=True):
    survey = ss.StreamlitSurvey("Survey Example")
    pages = survey.pages(15, on_submit=lambda: switch_page("분석페이지") )
    with pages:

      
# 1. 몇 명이서 여행을 가시나요? 
        if pages.current == 0:
            st.markdown(f"#### 1. 몇 명이서 여행을 가시나요? ")
            user_count = survey.number_input( '동행 인원 수', min_value=1, max_value=10)
            st.session_state['user_count'] = user_count
            


# 2. 누구와 함께 가시나요?(객관식)
# ⇒ 1) 가족 2) 연인 3) 친구 등
            if user_count >= 2:
                st.markdown(f"#### 2. 누구와 함께 가시나요? ")
                user_with =survey.radio(
                   'user_with',  options=["가족", "연인", "친구"], index=0, label_visibility="collapsed", horizontal=True
                )
                st.session_state['user_with'] = user_with
                

                

    
# 3. 여행 기간은 어떻게 되시나요?(~9월까지 제공)
# ⇒ 달력으로 표시(직접 선택) == 출발, 도착일 정해짐 + 일수계산 필요
        if pages.current == 1:
                st.markdown(f"#### 3. 여행 기간은 어떻게 되시나요? ")
                air_st = survey.dateinput('출국날짜')
                air_end = survey.dateinput('입국날짜')

                air_days = None  # Initialize air_days to None

                if air_st == air_end:
                    st.markdown(f"##### 날짜를 선택해주세요 ")
                else:
                    air_st_date = datetime.strptime(str(air_st)[0:10], '%Y-%m-%d').date()
                    air_end_date = datetime.strptime(str(air_end)[0:10], '%Y-%m-%d').date()
                    
                    if air_st_date < air_end_date:
                        air_days = (air_end_date - air_st_date).days

                if air_days is not None:
                    st.markdown("##### 여행 기간 : {}일".format(str(air_days)))


                st.session_state['air_st'] = air_st
                st.session_state['air_end'] = air_end
                st.session_state['air_days'] = air_days
                


                
    

# - 항공권 질문
# 4. 일본 어디로 가시나요?
# ⇒ 1) 도쿄 2) 오사카 3) 삿포로 4) 오키나와 5) 후쿠오카
        if pages.current == 2:
            st.markdown(f"#### 4. 일본 어디로 가시나요? ")
            det =survey.radio(
              'det',   options=list(city_to_airport_code_jp.keys()), index=0, label_visibility="collapsed"
            )
            det_i=city_to_airport_code_jp[det]
            st.session_state['det'] = det
            st.session_state['det_i'] = det_i
            



# 6. 어디에서 출발하시나요?
#  1) 인천공항 2) 청주공항 3) 광주공항 4) 대구공항 5)김해공항
        if pages.current == 3:
            st.markdown(f"#### 5. 어디 공항에서 출발하시나요? ")
            arr =survey.radio(
              'arr',    options=list(city_to_airport_code_kr.keys()), index=0, label_visibility="collapsed", horizontal=True
            )
            arr_i=city_to_airport_code_kr[arr]
            st.session_state['arr'] = arr
            st.session_state['arr_i'] = arr_i


# 7. 항공편에 선호하는 좌석 등급이 있나요?(상관없음을 빼고 복수선택 가능을 해도 괜찮을 듯)
# ⇒ 1) 상관 없음 2) 이코노미 3)프리미엄 이코노미 4) 비즈니스 5)퍼스트
        if pages.current == 4:
            st.markdown(f"#### 6. 항공편에 선호하는 좌석 등급이 있나요? ")
            filtered_air = air[(air['Arr'] == str(st.session_state.get('arr_i'))) & (air['Det'] == str(st.session_state.get('det_i')))]
            air_cls =survey.radio(
              'air_cls',  options=filtered_air['grade'].drop_duplicates().tolist(), index=0, label_visibility="collapsed", horizontal=True
            )
            st.session_state['air_cls'] = air_cls



# 8. 경유를 해도 괜찮나요?
        if pages.current == 5:
            st.markdown(f"#### 7. 경유를 해도 괜찮나요? ")
            filtered_air = air[(air['Arr'] == str(st.session_state.get('arr_i'))) & (air['Det'] == str(st.session_state.get('det_i'))) & 
                             (air['grade'] == str(st.session_state.get('air_cls'))) ]
            if len(filtered_air)==0:
              st.markdown('조건에 맞는 항공권이 없습니다, 다른 옵션으로 바꿔 주세요')
            
            else :
              air_around =survey.radio(
                'air_around', options=filtered_air['time_taken'].drop_duplicates().tolist(), index=0, label_visibility="collapsed", horizontal=True
              )
              st.session_state['air_around'] = air_around
            
            if not st.session_state.get('air_around') :
              st.write('직항, 경유 조건이 선택되지 않으면 정확한 예측이 어렵습니다. 이전 질문으로 돌아가주세요')


        if pages.current == 6:
          st.markdown(f"#### 8. 항공권 시간을 선택해주세요 ")
          col2, col3, col4, col5 = st.columns([0.4,0.2,0.2,0.2])
          with col2:
            st.write('일본행 항공권 시간을 선택해주세요')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write('한국행 항공권 시간을 선택해주세요')
          with col3:
            arrival_hour = st.number_input("일본행 (시)", min_value=0, max_value=23, value=0)
            depart_hour = st.number_input("한국행 (시)", min_value=0, max_value=23, value=0)
          with col4:
            arrival_minute = st.number_input("일본행 (분)", min_value=0, max_value=59, value=0)
            depart_minute = st.number_input("한국행 (분)", min_value=0, max_value=59, value=0)
          st.session_state['depart_hour'] = depart_hour
          st.session_state['arrival_hour'] = arrival_hour
          st.session_state['depart_minute'] = depart_minute
          st.session_state['arrival_minute'] = arrival_minute
            

 
# #호텔명	입실	퇴실	지역	숙박유형	별점	등급	가격	가장 가까운 공항	가장 가까운 공항과의 거리	가장 가까운 공항까지 시간
# #입실 == 출발날이랑 같다고 가정
# #지역 == 도착지랑 같다고 가정


        if pages.current == 7:
           st.write('#### 다음은 숙박에 대한 질문 입니다.')
          
        if pages.current == 8:
            st.markdown(f"#### 9. 어떤 숙박 유형을 찾을까요? ")
            hot_category=survey.radio('hot_category',
                        options=list(category_mapping.keys()), index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['hot_category'] = hot_category
        
        if pages.current == 9:
            st.markdown(f"#### 10. 숙소의 평점을 선택해주세요 ")
            st.markdown(f"##### 8점 이상을 추천드립니다.")
            hotel_score = survey.slider("평점 0.0 ~ 10.0", min_value=1, max_value=10, value=8)
            st.session_state['hotel_score'] = hotel_score

        if pages.current == 10:
            st.markdown(f"#### 11. 숙소의 등급(성급)을 선택해주세요 ")
            hotel_grade = survey.radio('등급', options=sorted(hotel['등급'].drop_duplicates().tolist()), index=2, label_visibility="collapsed", horizontal=True)
            st.session_state['hotel_grade'] = hotel_grade
          
        if pages.current == 11:
            st.markdown(f"#### 12. 공항에서 호텔과의 거리를 선택해주세요 ")
            hotel_far=survey.number_input("숙소까지의 시간(분단위) 0 ~ 60", min_value=1, max_value=60, value=20,step=1)
            st.session_state['hotel_far'] = hotel_far
            


# # # 렌트카 :: 지역	공항	이름	대여일	반납일	크기	제한인원수	보험	가격	브랜드
        if pages.current == 12:
           st.write('#### 다음의 질문은 렌트카에 대한 질문입니다.')
           
           
        if pages.current == 13:
                st.markdown(f"#### 13. 렌탈 기간은 어떻게 되시나요?  ")
                car_st = survey.dateinput('픽업날짜')
                car_end = survey.dateinput('반납날짜')


                car_days = None  # Initialize car_days to None

                if car_st == car_end:
                    st.markdown(f"##### 날짜를 선택해주세요  ")
                else:
                    car_st_date = datetime.strptime(str(car_st)[0:10], '%Y-%m-%d').date()
                    car_end_date = datetime.strptime(str(car_end)[0:10], '%Y-%m-%d').date()
                    
                    if car_st_date < car_end_date:
                        car_days = (car_end_date - car_st_date).days

                if car_days is not None:
                    st.markdown("##### 렌탈 기간 : {}일".format(str(car_days)))

                st.session_state['car_st'] = car_st
                st.session_state['car_end'] = car_end
                st.session_state['car_days'] = car_days
                
                
        if pages.current == 14:
            st.write(f'#### 14. 원하는 차종을 선택해주세요  ')
            car_capacity = survey.radio('차종', options=car['크기'].drop_duplicates().tolist(), index=0,label_visibility="collapsed", horizontal=True)
            st.session_state['car_capacity'] = car_capacity
            
          
            if car_capacity:
                # Convert '제한인원수' column to integers and filter the cars with a maximum passenger capacity
                filtered_cars = car[car['크기'] == car_capacity]
                car_size_list = filtered_cars['브랜드'].drop_duplicates().tolist()
                st.write(f'#### 15. 원하는 브랜드를 선택해주세요  ')
                car_brand = survey.radio('자동차 브랜드', options=car_size_list, label_visibility="collapsed", horizontal=True)
                st.session_state['car_brand'] = car_brand
                
                # Further filter the DataFrame based on the selected brand
                filtered_cars_by_brand = filtered_cars[filtered_cars['브랜드'] == car_brand]
                car_name_list = filtered_cars_by_brand['이름'].drop_duplicates().tolist()
                st.session_state['car_name_list'] = car_name_list
                
                
                st.markdown(f"#### 16. 보험은 어떤 걸로 할까요?  ")
                insurance=survey.radio('보험 종류',
                            options=car['보험'].drop_duplicates().tolist(), index=0, label_visibility="collapsed", horizontal=True
                        )
                st.session_state['insurance'] = insurance
