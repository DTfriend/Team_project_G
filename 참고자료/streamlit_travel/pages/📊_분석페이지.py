import streamlit as st
import datetime 
from datetime import datetime
import pandas as pd
import joblib
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space
import numpy as np



st.set_page_config(
    layout="wide",
    page_title="analysis",
    page_icon="📊",
)

# 사이트 헤드라인
st.title('비용 예측 및 분석 결과')

st.markdown("""
 * 답변을 바탕으로 비용 예측과 분석 결과를 볼 수 있습니다.            
 * 좌측 사이드바에서 선택한 옵션을 조정할 수 있습니다.
""")

add_vertical_space()
add_vertical_space()

air = pd.read_csv("data2/air_original_k2j.csv",encoding='CP949')
hotel = pd.read_csv("data2/hotel_total_final.csv")
car = pd.read_csv("data2/car_total.csv")


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

# 한국어 라벨로 변경
airport_to_name = {
'CTS': '삿포로',
'FUK': '후쿠오카',
'HND': '도쿄(하네다)',
'KIX': '오사카(간사이)',
'NRT': '도쿄(나리타)',
'OKA': '오키나와'
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
region_mapping = {
    '삿포로': 1,
    '후쿠오카': 4,
    '도쿄(하네다)': 0,
    '오사카(간사이)': 2,
    '도쿄(나리타)': 0,
    '오키나와': 3
}

## 호텔 데이터는 도쿄 HND, NRT 구분 안 하나?
airport_to_hotel_name =  {
'CTS': '삿포로',
'FUK': '후쿠오카',
'HND': '도쿄',
'KIX': '오사카(간사이)',
'NRT': '도쿄',
'OKA': '오키나와'
}

category_mapping = {'게스트하우스,캡슐호텔,호스텔':0, '리조트,펜션,료칸':1, '호텔':2}

hotel_grade_mapping ={'1성급':1,'2성급':2,'3성급':3,'4성급':4,'5성급':5,}




#Rent Car
######################################

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

airport_to_car_name =  {
'CTS': '삿포로',
'FUK': '후쿠오카',
'HND': '도쿄',
'KIX': '오사카',
'NRT': '도쿄',
'OKA': '오키나와'
}



    
# # # 사이드바 옵션
with st.sidebar:
    
    st.markdown('#### 내가 선택한 옵션')
#항공권
########################################################

    with st.expander("항공권"):
        with st.form("항공권"): 
            st.markdown("### 항공권")

    # # 1. 몇 명이서 여행을 가시나요? 
            st.markdown("#### 1. 몇 명이서 여행을 가시나요?")
            user_count = st.number_input( '인원 수', min_value=1, max_value=10, value=int(st.session_state.get('user_count')))
            


    # 2. 누구와 함께 가시나요?(객관식)
    # ⇒ 1) 가족 2) 연인 3) 친구 등
            if user_count >= 2:
                st.markdown("#### 2. 누구와 함께 가시나요?")
                user_with =st.radio(
                    'user_with',  options=["가족", "연인", "친구"], 
                    index={option: index for index, option in enumerate(["가족", "연인", "친구"])}.get(st.session_state.get('user_with'), -1), 
                    label_visibility="collapsed", horizontal=True
                )
            {option: index for index, option in enumerate(["가족", "연인", "친구"])}.get(st.session_state.get('user_with'), -1)
            
    # 3. 여행 기간은 어떻게 되시나요?(~9월까지 제공)
    # ⇒ 달력으로 표시(직접 선택) == 출발, 도착일 정해짐 + 일수계산 필요    


            st.markdown("#### 3. 여행 기간은 어떻게 되시나요?")
            air_st = st.date_input('출국날짜',value=datetime.strptime(str(st.session_state.get('air_st')[0:10]), '%Y-%m-%d').date())
            air_end = st.date_input('입국날짜',value=datetime.strptime(str(st.session_state.get('air_end')[0:10]), '%Y-%m-%d').date())
            
            air_st_date = datetime.strptime(str(air_st), '%Y-%m-%d').date()
            air_end_date = datetime.strptime(str(air_end), '%Y-%m-%d').date()
            
        
            if air_st_date < air_end_date:
                air_days = (air_end_date - air_st_date).days
                st.markdown("##### 여행 기간 : {}일".format(str(air_days)))
            else :
                st.write('입국 날짜가 출국 날짜와 같거나 먼저입니다')
                
            
    # # - 항공권 질문
    # # 4. 일본 어디로 가시나요?
    # # ⇒ 1) 도쿄 2) 오사카 3) 삿포로 4) 오키나와 5) 후쿠오카
            st.markdown("#### 4. 일본 어디로 가시나요?")
            det =st.radio(
                'det',   options=list(city_to_airport_code_jp.keys()), 
                index={option: index for index, option in enumerate(list(city_to_airport_code_jp.keys()))}.get(st.session_state.get('det'), -1), 
                label_visibility="collapsed"
            )
            det_i=city_to_airport_code_jp[det]
            det_city_name = region_mapping[det]
            
    # # 6. 어디에서 출발하시나요?
    # #  1) 인천공항 2) 청주공항 3) 광주공항 4) 대구공항 5)김해공항

            st.markdown("#### 5. 어디 공항에서 출발하시나요?")
            arr =st.radio(
                'arr',    options=list(city_to_airport_code_kr.keys()), 
                index={option: index for index, option in enumerate(list(city_to_airport_code_kr.keys()))}.get(st.session_state.get('arr'), -1), label_visibility="collapsed", 
                horizontal=True
            )
            arr_i=city_to_airport_code_kr[arr]
            
    # # 7. 항공편에 선호하는 좌석 등급이 있나요?(상관없음을 빼고 복수선택 가능을 해도 괜찮을 듯)
    # # ⇒ 1) 상관 없음 2) 이코노미 3)프리미엄 이코노미 4) 비즈니스 5)퍼스트
            
            st.markdown("#### 6. 항공편에 선호하는 좌석 등급이 있나요?")
            filtered_air = air[(air['Arr'] == str(st.session_state.get('arr_i'))) & (air['Det'] == str(st.session_state.get('det_i')))]
            air_cls =st.radio(
                'air_cls',  options=filtered_air['grade'].drop_duplicates().tolist(), 
                index={option: index for index, option in enumerate(filtered_air['grade'].drop_duplicates().tolist())}.get(st.session_state.get('air_cls'), -1), 
                label_visibility="collapsed", horizontal=True
            )
            air_cls_i=seat_class_mapping[air_cls]
            st.session_state['air_cls'] = air_cls

    # # 8. 경유를 해도 괜찮나요? 
            st.markdown("#### 7. 경유를 해도 괜찮나요?")
            filtered_air = air[(air['Arr'] == str(st.session_state.get('arr_i'))) & (air['Det'] == str(st.session_state.get('det_i'))) & 
                                (air['grade'] == str(st.session_state.get('air_cls'))) ]

            if st.session_state.get('air_around') :

                air_around =st.radio(
                    'air_around', options=filtered_air['time_taken'].drop_duplicates().tolist(), 
                    index={option: index for index, option in enumerate(filtered_air['time_taken'].drop_duplicates().tolist())}.get(st.session_state.get('air_around'), -1), 
                    label_visibility="collapsed", horizontal=True
                    )
                air_around_i=flight_mapping[air_around]
                
            else : 
                st.write('직항, 경유 조건이 선택되지 않으면 정확한 예측이 어렵습니다. 옵션을 조정해보세요')
                
                
            st.markdown(f"#### 8. 항공권 시간을 선택해주세요 ")      
            st.write('#### 일본행 항공권 시간을 선택해주세요')
            col1, col2 = st.columns([0.5,0.5])
            with col1:
                arrival_hour = st.number_input("(시)", min_value=0, max_value=23, value=int(st.session_state.get('arrival_hour')))
            with col2:
                arrival_minute = st.number_input("(분)", min_value=0, max_value=59, value=int(st.session_state.get('arrival_minute')))
                
            st.write('#### 한국행 항공권 시간을 선택해주세요')
            col3, col4 = st.columns([0.5,0.5])
            with col3:
                depart_hour = st.number_input("(시) ", min_value=0, max_value=23, value=int(st.session_state.get('depart_hour')))            
            with col4:
                depart_minute = st.number_input("(분) ", min_value=0, max_value=59, value=int(st.session_state.get('depart_minute')))
            
            # Every form must have a submit button.
            col5, col6, col7, col8, col9 = st.columns([0.2,0.2,0.2,0.2,0.2])
            with col9:
                st.write(' ')
                submitted_air = st.form_submit_button("적용")
# 호텔
# ######################################
           
    with st.expander("숙박"),st.form("숙박"):
            st.markdown("### 숙박")
            st.markdown("#### 9. 어떤 숙박 유형을 찾을까요?")
            hot_category=st.radio('hot_category',
                        options=list(category_mapping.keys()), 
                        index={option: index for index, option in enumerate(list(category_mapping.keys()))}.get(st.session_state.get('hot_category'), -1), 
                        label_visibility="collapsed", horizontal=True
                        )
            
            st.markdown("#### 10. 숙소의 평점을 선택해주세요")
            hotel_score = st.slider("평점 0.0 ~ 10.0", min_value=1, max_value=10, value = st.session_state.get('hotel_score') )
            
            
            st.markdown("#### 11. 숙소의 등급(성급)을 선택해주세요")
            hotel_grade = st.radio('등급', options=sorted(hotel['등급'].drop_duplicates().tolist()), 
                                   index={option: index for index, option in enumerate(sorted(hotel['등급'].drop_duplicates().tolist()))}.get(st.session_state.get('hotel_grade'), -1), 
                                   label_visibility="collapsed", horizontal=True)
            

            st.markdown("#### 12. 공항에서 호텔과의 거리를 선택해주세요")
            hotel_far=st.number_input("숙소까지 걸리는 시간(분)", min_value=1, max_value=60, value=st.session_state.get('hotel_far') ,step=1)
            # 차? 버스? 전철? 지하철? 어떤 기준임??
            
            col5, col6, col7, col8, col9 = st.columns([0.2,0.2,0.2,0.2,0.2])
            with col9:
                st.write(' ')
                submitted_hotel = st.form_submit_button("적용")
        
            
# # 렌트카 
# # 지역	공항	이름	대여일	반납일	크기	제한인원수	보험	가격	브랜드
# ###########################################
            
    with st.expander("렌트카"),st.form("렌트카"):
            st.markdown("### 렌트카")

            st.markdown("#### 13. 렌탈 기간은 어떻게 되시나요?")
            car_st = st.date_input('픽업날짜',value=datetime.strptime(str(st.session_state.get('car_st')[0:10]), '%Y-%m-%d').date())
            car_end = st.date_input('반납날짜',value=datetime.strptime(str(st.session_state.get('car_end')[0:10]), '%Y-%m-%d').date())
            
            car_st_date = datetime.strptime(str(car_st), '%Y-%m-%d').date()
            car_end_date = datetime.strptime(str(car_end), '%Y-%m-%d').date()
            
            if car_end_date > car_st_date :
                car_days = (car_end_date - car_st_date).days
                st.markdown("##### 렌탈 기간 {}일".format(str(car_days)))
            else :
                st.write('픽업 날짜가 반납 날짜와 같거나 먼저입니다')
                
            
            st.write('#### 14. 원하는 차종을 선택해주세요')
            car_capacity = st.radio('차종', options=car['크기'].drop_duplicates().tolist(), 
                                    index={option: index for index, option in enumerate(car['크기'].drop_duplicates().tolist())}.get(st.session_state.get('car_capacity'), -1),
                                    label_visibility="collapsed", horizontal=True)
            
            if not car_capacity:
                st.write('해당하는 렌트카가 없습니다. 옵션을 조정해주세요')
                
            else :
                # Convert '제한인원수' column to integers and filter the cars with a maximum passenger capacity
                filtered_cars = car[car['크기'] == car_capacity]
                car_size_list = filtered_cars['브랜드'].drop_duplicates().tolist()
                
                st.write('#### 15. 원하는 브랜드를 선택해주세요')
                car_brand = st.radio('자동차 브랜드', options=car_size_list,
                                     index={option: index for index, option in enumerate(car_size_list)}.get(st.session_state.get('car_brand'), -1) , 
                                     label_visibility="collapsed", horizontal=True)
                
                # Further filter the DataFrame based on the selected brand
                filtered_cars_by_brand = filtered_cars[filtered_cars['브랜드'] == car_brand]
                car_name_list = filtered_cars_by_brand['이름'].drop_duplicates().tolist()
                for name in car_name_list:
                    name_encoded = car_mapping[name]

                
                
                st.markdown("#### 16. 보험은 어떤 걸로 할까요?")
                insurance=st.radio('보험 종류',
                            options=car['보험'].drop_duplicates().tolist(), 
                            index={option: index for index, option in enumerate(car['보험'].drop_duplicates().tolist())}.get(st.session_state.get('insurance'), -1) ,
                            label_visibility="collapsed", horizontal=True
                        )
        
            col5, col6, col7, col8, col9 = st.columns([0.2,0.2,0.2,0.2,0.2])
            with col9:
                st.write(' ')
                submitted_car = st.form_submit_button("적용")


              
air_model = joblib.load("air_test.pkl")
hotel_model = joblib.load("hotel_rf_model.pkl")
car_model = joblib.load("car_rf_model.pkl")


# 페이지 넘어왔을 때 계산 적용
#항공    
input_data_air = [ korea_air[arr_i], japan_air[det_i], air_st_date.strftime('%Y%m%d'),  air_around_i, air_cls_i , depart_hour, depart_minute, arrival_hour, arrival_minute]
input_array_air = np.array([input_data_air])
air_pre = air_model.predict(input_array_air)

#호텔
input_data_hotel = [region_mapping[det],category_mapping[hot_category],air_st_date.strftime('%Y%m%d'),air_end_date.strftime('%Y%m%d'),hotel_score,hotel_grade_mapping[hotel_grade],hotel_far]
input_array_hotel = np.array([input_data_hotel])
hot_pre = hotel_model.predict(input_array_hotel)
    
   
#렌트카
input_data_car = [region_mapping[det],japan_air[det_i],name_encoded,car_st_date.strftime('%Y%m%d'),car_end_date.strftime('%Y%m%d'),
                    car_size_mapping[car_capacity],user_count,insurance_mapping[insurance],brand_mapping[car_brand]]
input_array_car = np.array([input_data_car])
car_pre = car_model.predict(input_array_car)


# 적용하기 눌렀을때 머신러닝 작동
#항공    
if submitted_air :
    input_data_air = [ korea_air[arr_i], japan_air[det_i], air_st_date.strftime('%Y%m%d'),  air_around_i, air_cls_i , depart_hour, depart_minute, arrival_hour, arrival_minute]
    input_array_air = np.array([input_data_air])
    air_pre = air_model.predict(input_array_air)



#호텔
if submitted_hotel :
    input_data_hotel = [region_mapping[det],category_mapping[hot_category],air_st_date.strftime('%Y%m%d'),air_end_date.strftime('%Y%m%d'),hotel_score,hotel_grade_mapping[hotel_grade],hotel_far]
    input_array_hotel = np.array([input_data_hotel])
    hot_pre = hotel_model.predict(input_array_hotel)
    
   
#렌트카
if submitted_car :
    input_data_car = [region_mapping[det],japan_air[det_i],name_encoded,car_st_date.strftime('%Y%m%d'),car_end_date.strftime('%Y%m%d'),
                        car_size_mapping[car_capacity],user_count,insurance_mapping[insurance],brand_mapping[car_brand]]
    input_array_car = np.array([input_data_car])
    car_pre = car_model.predict(input_array_car)




def won(number):
    return np.array2string(number, formatter={'all': lambda x: f'{x:,.0f}'}).replace('[', '').replace(']', '')


add_vertical_space()

col1, col2, col3 = st.columns(3)

with col1:
   st.header("""항공권
              {}원/1인""".format(won(air_pre)))

## 편도 각각 구하기

with col2:
   st.header("""숙박
              {}원/1박""".format(int(hot_pre[0])))

with col3:
   st.header("""렌트카
              {}원/1일""".format(int(car_pre[0])))
   


cola, colb, colc = st.columns(3)


with colc:
    st.header("""총합 : {}원
              """.format(f"{int(air_pre[0]+hot_pre[0]+car_pre[0]):,}"))
   
    
add_vertical_space()
add_vertical_space()




row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row3_1:
    st.subheader("일본 지역별 항공권 가격")
    # Figure 생성
    fig = go.Figure()
    
# 선택한 일본행 출발 날짜, 항공 클래스  기준 일본 지역별 평균 price 계산
# 2023-08-20
    filtered_air = air[(air['Arr'] == arr_i) & (air['Arr_date'] == air_st.strftime('%Y-%m-%d')) & 
                    (air['grade'] == air_cls)]

    average_prices = filtered_air.groupby('Det')['price'].mean().reset_index()
    average_prices.sort_values(by='price', inplace =True)
        
    # 원 단위(KRW)로 평균 가격 포맷팅
    average_prices['price'] = average_prices['price'].apply(lambda x: '{:,}'.format(int(x)))
    
    # 이름 변경
    average_prices['Det'] = average_prices['Det'].map(airport_to_name)

    # 평균 가격에 따라 막대 그래프 생성
    x = average_prices['Det'].tolist()
    colors = ['LightSalmon' if i == airport_to_name[det_i] else 'LightSkyBlue' for i in x]

    fig.add_trace(go.Bar(
    x=average_prices['Det'],
    y=average_prices['price'],
    marker_color=colors,
    text=average_prices['price'],
    textposition='outside'
    ))
    
    
    fig.update_layout(title=f"날짜 : {air_st}, 클래스 : {air_cls}",
                    xaxis_title='일본 지역',
                    yaxis_title='항공권 평균 가격',
                    font=dict( {'family':'NanumSquareRoundR'} ))

    fig.add_annotation(
                x=airport_to_name[det_i], # x 축 기준 주석 위치
                y=air_pre[0], # y 축 기준 주석 위치
                text=f"""예측 결과 <br>{won(air_pre)}원""",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    {'family':'NanumSquareRoundR'},
                    size=12,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )
    # # add horizontal lines
    # fig.update_layout(shapes=[
    # dict(type='rect',
    #         xref='x', x0='2020-03-21', x1='2020-03-21',
    #         yref='paper', y0=0, y1=1,
    #         line=dict(color="MediumPurple", width=3, dash="dot")
    #         ),
    # dict(type='rect',
    #         xref='x', x0='2020-06-21', x1='2020-06-21',
    #         yref='paper', y0=0, y1=1,
    #         line=dict(color="MediumPurple", width=3, dash="solid")
    #         )
    # ])


    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    



with row3_2:
    st.subheader("날짜별 항공권 가격")
    
    filtered_air_date = air[(air['Arr'] == arr_i) & (air['Det'] == det_i) & 
                    (air['grade'] == air_cls)]

    average_prices_date = filtered_air_date.groupby('Arr_date')['price'].mean().reset_index()
    average_prices_date['price'] = average_prices_date['price'].apply(lambda x: '{:,}'.format(int(x)))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=average_prices_date['Arr_date'], y=average_prices_date['price'], mode='lines+markers', marker_color='LightSkyBlue'))
    fig.update_layout(title="날짜별 항공권 가격", xaxis_title="날짜", yaxis_title="항공권 평균 가격")
    fig.update_xaxes(tickformat="%m-%d (%a)")
    
    fig.add_annotation(
                x=air_st.strftime('%Y-%m-%d'), # x 축 기준 주석 위치
                y=air_pre[0], # y 축 기준 주석 위치
                text=f"""예측 결과 <br>{won(air_pre)}원""",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    {'family':'NanumSquareRoundR'},
                    size=12,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )
    # ## 출국 입국 가격??
    # fig.add_annotation(
    #     x=air_end.strftime('%Y-%m-%d'), # x 축 기준 주석 위치
    #     y=air_pre[0], # y 축 기준 주석 위치
    #     text=f"""내 항공권 <br>{won(air_pre)}원""",
    #     showarrow=True, # 화살표 표시 여부
    #     font=dict( # 주석 폰트
    #         {'family':'NanumSquareRoundR'},
    #         size=12,
    #         color="#ffffff"
    #         ),
    #         align="center", # 정렬
    #         arrowhead=2, # 화살표 머리 크기
    #         arrowsize=1, # 화살표 크기
    #         arrowwidth=2, # 화살표 넓이
    #         arrowcolor="#F25D50", # 화살표 색상
    #         ax=100, #박스 위치 가로
    #         ay=50,# 박스 위치 세로
    #         borderpad=10, # 주석칸 크기
    #         bgcolor="#F25D50", # 배경색
    #         opacity=1, # 투명도
    #         captureevents =True
    # )
    st.plotly_chart(fig, use_container_width=True)





add_vertical_space()
add_vertical_space()


row4_space1, row4_1, row4_space2, row4_2, row4_space4 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
airport_to_hotel_name = {
'CTS': '삿포로',
'FUK': '후쿠오카',
'HND': '도쿄',
'KIX': '오사카(간사이)',
'NRT': '도쿄',
'OKA': '오키나와'
}


hotel['입실'] = pd.to_datetime(hotel['입실'])


with row4_1:
    st.subheader("유형별 숙박 가격")
    fig = go.Figure()

    filtered_df_hotel = hotel[(hotel['지역'] == airport_to_hotel_name[det_i]) & (hotel['입실'] ==air_st.strftime('%Y-%m-%d'))]

    average_prices_hotel = filtered_df_hotel.groupby('숙박유형')['가격'].mean().reset_index()
    average_prices_hotel.sort_values(by='가격', inplace =True)
    average_prices_hotel['가격'] = average_prices_hotel['가격'].apply(lambda x: '{:,}'.format(int(x)))

    # plotly 그래프 그리기
    hotel_type=average_prices_hotel['숙박유형'].tolist()
    colors = ['LightSalmon' if i == hot_category else 'Lavender' for i in hotel_type]
    

    fig.add_trace(go.Bar(x=average_prices_hotel['숙박유형'], y=average_prices_hotel['가격'],
                        marker_color=colors,
                        text=average_prices_hotel['가격'],
                        textposition='outside'))
    fig.update_layout(title="다른 유형의 숙박 평균 가격",
                    xaxis_title='숙박 유형',
                    yaxis_title='숙박 평균 가격')

    fig.add_annotation(
                x=hot_category, # x 축 기준 주석 위치
                y=hot_pre[0], # y 축 기준 주석 위치
                text=f"""예측 결과 <br>{won(air_pre)}원""",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    size=12,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    

with row4_2:
    st.subheader("평점별 숙박 가격")
    fig = go.Figure()

    filtered_df_hotel = hotel[(hotel['지역'] == airport_to_hotel_name[det_i]) & (hotel['입실'] ==air_st.strftime('%Y-%m-%d')) ]

    average_prices_hotel = filtered_df_hotel.groupby('별점')['가격'].mean().reset_index()
    average_prices_hotel.sort_values(by='가격', inplace =True)

    # plotly 그래프 그리기
    hotel_type_score=average_prices_hotel['별점'].drop_duplicates().tolist()
    colors = ['DarkOrange' if i == str(float(hotel_score)) else 'Lavender' for i in hotel_type_score]

    fig.add_trace(go.Bar(x=average_prices_hotel['별점'], y=average_prices_hotel['가격'],
                        marker_color=colors))
    fig.update_layout(title="다른 평점의 숙박 평균 가격",
                    xaxis_title='평점',
                    yaxis_title='숙박 평균 가격')

    fig.add_annotation(
                x=str(float(hotel_score)), # x 축 기준 주석 위치
                y=hot_pre[0], # y 축 기준 주석 위치
                text=f"""예측 결과 <br>{won(hot_pre)}원""",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    size=12,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    

add_vertical_space()
add_vertical_space()


row5_space1, row5_1, row5_space2, row5_2, row5_space5 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)




with row5_1:
    st.subheader("차종별 렌트카 가격")
    # Figure 생성
    fig = go.Figure()
    
    # 특정 Arr, Arr_date, grade 기준 Det별 평균 price 계산

    filtered_df_car = car[(car['지역'] == airport_to_car_name[det_i] ) ]

    average_prices_car = filtered_df_car.groupby('크기')['가격'].mean().reset_index()
    average_prices_car.sort_values(by='가격',inplace=True)
    average_prices_car['가격'] = average_prices_car['가격'].apply(lambda x: '{:,}'.format(int(x)))

    # plotly 그래프 그리기
    car_type=average_prices_car['크기'].drop_duplicates().tolist()
    colors = ['LightSalmon' if i == car_capacity else 'LightGreen' for i in car_type]

    fig.add_trace(go.Bar(x=average_prices_car['크기'], y=average_prices_car['가격'],
                        marker_color=colors,
                        text=average_prices_car['가격'],
                        textposition='outside'))
    fig.update_layout(title="차종별 렌트카 평균 가격",
                    xaxis_title='차종',
                    yaxis_title='렌트카 평균 가격')

    fig.add_annotation(
                x=car_capacity, # x 축 기준 주석 위치s
                y=car_pre[0], # y 축 기준 주석 위치
                text=f"""예측 결과 <br>{won(car_pre)}원""",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    size=12,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    

   

    
with row5_2:
    st.subheader("날짜별 렌트카 가격")
    
    filtered_df_date = car[(car['공항'] == det_i) & (car['크기'] == car_capacity) ]
    filtered_df_date['대여일'] = pd.to_datetime(filtered_df_date['대여일'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    average_prices_date = filtered_df_date.groupby('대여일')['가격'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=average_prices_date['대여일'], y=average_prices_date['가격'], mode='lines+markers',marker_color='LightGreen') )
    fig.update_layout(title="날짜별 렌트카 가격", xaxis_title="날짜", yaxis_title="렌트카 평균 가격")
    fig.update_xaxes(tickformat="%m-%d (%a)")
    fig.add_annotation(
            x=car_st.strftime('%Y-%m-%d'), # x 축 기준 주석 위치
            y=car_pre[0], # y 축 기준 주석 위치
            text=f"""예측 결과 <br>{won(car_pre)}원""",
            showarrow=True, # 화살표 표시 여부
            font=dict( # 주석 폰트
                size=12,
                color="#ffffff"
                ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#F25D50", # 화살표 색상
                ax=100, #박스 위치 가로
                ay=50,# 박스 위치 세로
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=1, # 투명도
                captureevents =True
    )

    st.plotly_chart(fig, use_container_width=True)
