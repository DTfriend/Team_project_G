import streamlit as st
import datetime
import time
import pandas as pd
import plotly.express as px
import joblib
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space


st.set_page_config(
    layout="wide",
    page_title="analysis",
    page_icon="📊",
)

# 사이트 헤드라인
st.title('일본 여행 경비 예측 프로젝트')

st.markdown("""
 * 항공권, 숙박, 렌트카를 기준으로 비용을 예측해드립니다.
 * 왼쪽 옵션의 조정에 따라 비용이 계산됩니다.
""")



# 1. 몇 명이서 여행을 가시나요? 
st.write("user_count:", st.session_state.get('user_count'))
# 2. 누구와 함께 가시나요?(객관식)
# ⇒ 1) 가족 2) 연인 3) 친구 등
st.write("user_with:", st.session_state.get('user_with'))
# 3. 여행 기간은 어떻게 되시나요?(~9월까지 제공)
# ⇒ 달력으로 표시(직접 선택) == 출발, 도착일 정해짐 + 일수계산 필요

st.write("air_st air_end", st.session_state.get('air_st'), st.session_state.get('air_end'))


# - 항공권 질문
# 4. 일본 어디로 가시나요?
# ⇒ 1) 도쿄 2) 오사카 3) 삿포로 4) 오키나와 5) 후쿠오카
st.write("det_i", st.session_state.get('det_i'))


# 5. 어느 공항이 좋으신가요?
# 1) 상관없음 2) 하네다 3) 나리타
# st.write("Value from Page 1:", st.session_state.get('user_count'))

# 6. 어디에서 출발하시나요?
# ⇒ 1) 인천공항 2) 청주공항 3) 광주공항 4) 대구공항 5)김해공항
st.write("arr_i", st.session_state.get('arr_i'))

# 7. 항공편에 선호하는 좌석 등급이 있나요?(상관없음을 빼고 복수선택 가능을 해도 괜찮을 듯)
# ⇒ 1) 상관 없음 2) 이코노미 3)프리미엄 이코노미 4) 비즈니스 5)퍼스트 
st.write("air_cls_i", st.session_state.get('air_cls_i'))

# 8. 경유를 해도 괜찮나요?
# ⇒ 1) 상관없음 2) 직항만
st.write("air_around_i", st.session_state.get('air_around_i'))

# 9. 항공권을 예약할 때 어느 요소가 더 중요한가요?
# ⇒  1) 가격 2) 출발 시간
st.write("air_pref", st.session_state.get('air_pref'))

# 10. 시간대는 언제가 좋나요? 

# 10-1 갈 때는 언제가 좋나요?
st.write("time_st", st.session_state.get('time_st'))

# 10-2 올 때는 언제가 좋나요?
st.write("time_end", st.session_state.get('time_end'))





# # 사이드바 옵션
st.sidebar.markdown("## 비용 예측 옵션")


with st.sidebar.form('my_form'):
    
#     # people = 성인 몇명, 유아 몇명인지 
    
    air_st=st.selectbox('출발 공항을 선택해주세요',
                        ['인천', '청주', '대구', '광주', '부산'])

#     air_end=st.selectbox('도착 공항을 선택해주세요',
#                             ['하네다(도쿄)','나리타(도쿄)', '오사카', '삿포로', '오키나와', '후쿠오카', '기타큐슈'])


#     clas=st.selectbox('클래스를 선택해주세요',
#                             ['economy', 'preminum', 'business', 'first'])
    
    today = datetime.datetime.now()
    start = datetime.date(today.year, 7, 1)
    end = datetime.date(today.year, 9, 30)

#     air_d = st.date_input(
#         "출국 날짜와 입국 날짜를 선택해주세요",
#         (start, datetime.date(today.year, 7, 1)),
#         start,
#         end,
#         format="MM.DD.YYYY",
#     )

#     st.write('--------------------------')

#     h_t=st.selectbox('숙박 유형을 선택해주세요',
#                             ['호텔', '게스트하우스,캡슐호텔,호스텔', '리조트,펜션,료칸'])
#     # 이거 선택 옵션을 어떻게 해야할지
#     # 1. 중복 허용
#     # 2. 2번째 3번째 묶인거 하나씩으로 풀어줘야할지

#     h_sc=st.slider(
#         '평점을 선택해주세요',
#         0.0, 10.0, (2.5, 7.5))
    
#     h_st=st.slider(
#         '등급을 선택해주세요',
#         1, 5, (2,3))


#     h_d = st.date_input(
#         "숙박 체크인, 아웃 날짜를 선택해주세요",
#         (start, datetime.date(today.year, 7, 1)),
#         start,
#         end,
#         format="MM.DD.YYYY",
#     )

#     st.write('--------------------------')
    

    
    
#     # 지역    공항    이름    대여일    반납일    크기    제한인원수    보험    브랜드
#     # 지역 선택
#     region_mapping = {'도쿄': 0, '삿포로': 1, '오사카': 2, '오키나와': 3, '후쿠오카': 4}
#     region = air_end  # 위에서 도착 지역 선택한 거 재활용
#     selected_region_value = region_mapping[region]

#     # 공항 선택
#     airport_mapping = {'CTS':0, 'FUK':1, 'HND':2, 'KIX':3, 'KKJ':4, 'NRT':5, 'OKA':6}
#     air_to_loca = {
#         '하네다(도쿄)': 'HND',
#         '나리타(도쿄)': 'NRT',
#         '오사카': 'KIX',
#         '오키나와': 'OKA',
#         '후쿠오카': 'FUK',
#         '기타큐슈': 'KKJ',
#         '삿포로': 'CTS'
#     }
#     airport = air_to_loca[air_end]
#     selected_airport_value = airport_mapping[airport]

#     # 이름 입력
#     name_mapping = {'86':0,'C-HR':1,'eK왜건':2,'노트5도어':3,'노트E-파워':4,'데미오':5,'델리카8인승':6,'라이즈':7,
#     '랜드크루저프라도':8,'레보그':9,'루미':10,'무브콘테':11,'벨파이어8인승':12,'복시':13,'비츠':14,'스마일':15,
#     '스텝왜건':16,'스텝왜건8인승':17,'시엔타':18,'시엔타6인승':19,'아쿠아':20,'알파드':21,'알파드8인승':22,'야리스':23,
#     '엔박스':24,'왜건R':25,'이클립스크로스':26,'임프레자':27,'캠리':28,'코롤라':29,'코롤라필더':30,'큐브':31,'크라운':32,
#     '태프트':33,'프리우스':34,'피트':35,'하이에이스그랜드캐빈':36,'허슬러':37}
#     name = st.selectbox('이름',list(name_mapping.keys()))
#     selected_name_value = name_mapping[name]

#     # 대여 반납
#     c_d = st.date_input(
#         "렌트카를 사용하는 날짜를 선택해주세요",
#         (start, datetime.date(today.year, 7, 1)),
#         start,
#         end,
#         format="MM.DD.YYYY",
#     )

#     # 크기 선택
#     size_mapping = {'RV':0,'SUV':1,'경형':2,'대형':3,'소형':4,'왜건':5,'준중형':6,'중형':7}
#     size = st.radio('크기',list(size_mapping.keys()))
#     selected_size_value = size_mapping[size]

#     # 제한인원수 입력
#     capacity = st.number_input('제한인원수', min_value=1, max_value=10, value=5)

#     # 보험 선택
#     insurance_mapping = {'면책커버보험 포함':0,'스탠다드플랜 포함':1,'프리미엄플랜 포함':2}
#     insurance = st.radio('보험', list(insurance_mapping.keys()))
#     selected_insurance_value = insurance_mapping[insurance]

#     # 브랜드 입력
#     brand_mapping = {'닛산':0,'다이하쓰':1,'도요타':2,'마쯔다':3,'미쓰비시':4,'스바루':5,'스즈키':6,'혼다':7}
#     brand = st.radio('브랜드',list(brand_mapping.keys()))
#     selected_brand_value = brand_mapping[brand]

    
    submitted = st.form_submit_button('적용하기')
    
st.write(air_st)
# # 학습된 모델 로드
# # air_model = joblib.load("air_model.pkl")
# h_model = joblib.load("hotel_rf_model.pkl")
# car_model = joblib.load("car_rf_model.pkl")



# # st.write(selected_arr,selected_det,selected_arr_date,selected_grade,)





# # 적용하기 눌렀을때 머신러닝 작동
# if st.button("Submit"):
# #항공    
#     air_model = joblib.load("air_model.pkl")
#     input_data_air = [region, airport, name, c_d[0], c_d[1], size, capacity, insurance, brand]
#     air_pre = air_model.predict([input_data_air])[0]

# #호텔
#     h_model = joblib.load("h_model.pkl")
#     input_data_hotel = [region, airport, name, c_d[0], c_d[1], size, capacity, insurance, brand]
#     hot_pre = h_model.predict([input_data_hotel])[0]
    
# #렌트카    
#     car_model = joblib.load("car_model.pkl")
#     input_data_car = [selected_region_value,
#                       selected_airport_value,
#                       selected_name_value,
#                       c_d[0].strftime("%Y%m%d"),
#                       c_d[1].strftime("%Y%m%d"),
#                       selected_size_value,
#                       capacity,
#                       selected_insurance_value,
#                       selected_brand_value]               
#     car_pre = car_model.predict([input_data_car])[0]

    



# col1, col2, col3 = st.columns(3)
# air_pre =1
# hot_pre =1
# car_pre =1

# with col1:
#    st.header("""{}->{} 항공권
#               {}원""".format(air_st,air_end,air_pre))

# ## 편도 각각 구하기

# with col2:
#    st.header("""숙박
#               {}원""".format(hot_pre))

# with col3:
#    st.header("""렌트카
#               {}원""".format(car_pre))
   

# st.markdown(
#     """
#     <style>
#         div[data-testid="column"]:nth-of-type(3)
#         {
#             text-align: end;
#         } 
#     </style>
#     """,unsafe_allow_html=True
# )

# cola, colb, colc = st.columns(3)


# with colc:
#    st.header("""총합 : {}원
#               """.format(air_pre+hot_pre+car_pre))
   
    

# add_vertical_space()

# df = pd.read_csv('data/air.csv',encoding='CP949')
# df['Arr_date'] = pd.to_datetime(df['Arr_date'])


# city_to_airport_code_jp = {
#     '도쿄': 'NRT',
#     '오사카': 'KIX',
#     '삿포로': 'CTS',
#     '오키나와': 'OKA',
#     '후쿠오카': 'FUK'
# }

# airport_codes_jp = city_to_airport_code_jp[air_end]

# city_to_airport_code_kr = {
#     '인천': 'ICN',
#     '청주': 'CJJ',
#     '대구': 'TAE',
#     '광주': 'KWJ',
#     '부산': 'PUS'
# }

# airport_codes_kr = city_to_airport_code_kr[air_st]

# selected_arr = airport_codes_kr
# selected_arr_date = air_d[0].strftime('%Y-%m-%d')
# selected_grade = clas
# selected_det = airport_codes_jp

# row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
#     (0.1, 1, 0.1, 1, 0.1)
# )

# with row3_1:
#     st.subheader("지역별 항공권 가격")
#     # Figure 생성
#     fig = go.Figure()
    
#     # 특정 Arr, Arr_date, grade 기준 Det별 평균 price 계산

#     filtered_df = df[(df['Arr'] == selected_arr) & (df['Arr_date'] == selected_arr_date) & 
#                     (df['grade'] == selected_grade)]

#     average_prices = filtered_df.groupby('Det')['price'].mean().reset_index()

#     # plotly 그래프 그리기
#     det=['NRT', 'OKA', 'CTS', 'FUK' ,'KIX']
#     colors = ['crimson' if i == selected_det else 'lightslategray' for i in det]

#     fig.add_trace(go.Bar(x=['NRT', 'OKA', 'CTS', 'FUK' ,'KIX'], y=average_prices['price'],
#                         marker_color=colors,
#                         text=average_prices['price'],
#                         textposition='auto'))
#     fig.update_layout(title=f"{selected_arr},{selected_det}, {selected_arr_date}, {selected_grade} 일 때 다른 지역의 항공권 평균 가격",
#                     xaxis_title='일본 지역',
#                     yaxis_title='항공권 평균 가격')

#     fig.add_annotation(
#                 x=selected_det, # x 축 기준 주석 위치
#                 # y=air_pre, # y 축 기준 주석 위치
#                 text="<b>나의 선택</b>",
#                 showarrow=True, # 화살표 표시 여부
#                 font=dict( # 주석 폰트
#                     size=10,
#                     color="#ffffff"
#                     ),
#                 align="center", # 정렬
#                 arrowhead=2, # 화살표 머리 크기
#                 arrowsize=1, # 화살표 크기
#                 arrowwidth=2, # 화살표 넓이
#                 arrowcolor="#77CFD9", # 화살표 색상
#                 ax=20, #박스 위치 가로
#                 ay=-30,# 박스 위치 세로
#                 bordercolor="#77CFD9", # 주석 테두리 색상
#                 borderwidth=2, # 주석 테두리 크기
#                 borderpad=10, # 주석칸 크기
#                 bgcolor="#F25D50", # 배경색
#                 opacity=0.9 # 투명도
#     )

#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    

# with row3_2:
#     st.subheader("날짜별 항공권 가격")
    
#     filtered_df_date = df[(df['Arr'] == selected_arr) & (df['Det'] == selected_det) & 
#                     (df['grade'] == selected_grade)]

#     average_prices_date = filtered_df_date.groupby('Arr_date')['price'].mean().reset_index()
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=average_prices_date['Arr_date'], y=average_prices_date['price'], mode='lines+markers'))
#     fig.update_layout(title="날짜별 항공권 가격", xaxis_title="날짜", yaxis_title="항공권 평균 가격")
#     fig.update_xaxes(tickformat="%m-%d (%a)")
#     fig.add_annotation(
#             x=air_d[0], # x 축 기준 주석 위치
#             # y=air_pre, # y 축 기준 주석 위치
#             text="<b>출국</b>",
#             showarrow=True, # 화살표 표시 여부
#             font=dict( # 주석 폰트
#                 size=10,
#                 color="#ffffff"
#                 ),
#             align="center", # 정렬
#             arrowhead=2, # 화살표 머리 크기
#             arrowsize=1, # 화살표 크기
#             arrowwidth=2, # 화살표 넓이
#             arrowcolor="#77CFD9", # 화살표 색상
#             ax=20, #박스 위치 가로
#             ay=-30,# 박스 위치 세로
#             bordercolor="#77CFD9", # 주석 테두리 색상
#             borderwidth=2, # 주석 테두리 크기
#             borderpad=10, # 주석칸 크기
#             bgcolor="#F25D50", # 배경색
#             opacity=0.9 # 투명도
#         )
#     fig.add_annotation(
#         x=air_d[1], # x 축 기준 주석 위치
#         # y=air_pre, # y 축 기준 주석 위치
#         text="<b>입국</b>",
#         showarrow=True, # 화살표 표시 여부
#         font=dict( # 주석 폰트
#             size=10,
#             color="#ffffff"
#             ),
#         align="center", # 정렬
#         arrowhead=2, # 화살표 머리 크기
#         arrowsize=1, # 화살표 크기
#         arrowwidth=2, # 화살표 넓이
#         arrowcolor="#77CFD9", # 화살표 색상
#         ax=20, #박스 위치 가로
#         ay=-30,# 박스 위치 세로
#         bordercolor="#77CFD9", # 주석 테두리 색상
#         borderwidth=2, # 주석 테두리 크기
#         borderpad=10, # 주석칸 크기
#         bgcolor="#F25D50", # 배경색
#         opacity=0.9 # 투명도
#     )
#     st.plotly_chart(fig, use_container_width=True)




# add_vertical_space()


# row4_space1, row4_1, row4_space2, row4_2, row4_space4 = st.columns(
#     (0.1, 1, 0.1, 1, 0.1)
# )


# hotel = pd.read_csv('data\hotel_how_far.csv',encoding='CP949')
# hotel['입실'] = pd.to_datetime(hotel['입실'])
# selected_hotel_date = h_d[0].strftime('%Y-%m-%d')





# with row4_1:

#     fig = go.Figure()

#     filtered_df_hotel = hotel[(hotel['지역'] == air_end) & (hotel['입실'] ==selected_hotel_date)]

#     average_prices_hotel = filtered_df_hotel.groupby('숙박유형')['가격'].mean().reset_index()

#     # plotly 그래프 그리기
#     hotel_type=['게스트하우스,캡슐호텔,호스텔', '리조트,펜션,료칸', '호텔']
#     colors = ['crimson' if i == h_t else 'lightslategray' for i in hotel_type]

#     fig.add_trace(go.Bar(x=average_prices_hotel['숙박유형'], y=average_prices_hotel['가격'],
#                         marker_color=colors,
#                         text=average_prices_hotel['가격'],
#                         textposition='auto'))
#     fig.update_layout(title="다른 유형의 숙박 평균 가격",
#                     xaxis_title='숙박 유형',
#                     yaxis_title='숙박 평균 가격')

#     fig.add_annotation(
#                 x=h_t, # x 축 기준 주석 위치
#                 # y=hot_pre, # y 축 기준 주석 위치
#                 text="<b>나의 선택</b>",
#                 showarrow=True, # 화살표 표시 여부
#                 font=dict( # 주석 폰트
#                     size=10,
#                     color="#ffffff"
#                     ),
#                 align="center", # 정렬
#                 arrowhead=2, # 화살표 머리 크기
#                 arrowsize=1, # 화살표 크기
#                 arrowwidth=2, # 화살표 넓이
#                 arrowcolor="#77CFD9", # 화살표 색상
#                 ax=20, #박스 위치 가로
#                 ay=-30,# 박스 위치 세로
#                 bordercolor="#77CFD9", # 주석 테두리 색상
#                 borderwidth=2, # 주석 테두리 크기
#                 borderpad=10, # 주석칸 크기
#                 bgcolor="#F25D50", # 배경색
#                 opacity=0.9 # 투명도
#     )

#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    
# hotel_star = {
#     1:'1성급',
#     2:'2성급',
#     3:'3성급',
#     4:'4성급',
#     5:'5성급'
# }

# # st.write(h_t,h_sc,h_st,selected_hotel_date,air_end)
# a = [hotel_star[i] for i in range(h_st[0], h_st[1] + 1)]

# with row4_2:
#     fig = go.Figure()

#     filtered_df_hotel = hotel[(hotel['지역'] == air_end) & (hotel['입실'] ==selected_hotel_date) ]

#     average_prices_hotel = filtered_df_hotel.groupby('등급')['가격'].mean().reset_index()

#     # plotly 그래프 그리기
#     hotel_type=['1성급','2성급','3성급','4성급','5성급']
#     colors = ['crimson' if i in a else 'lightslategray' for i in hotel_type]

#     fig.add_trace(go.Bar(x=average_prices_hotel['등급'], y=average_prices_hotel['가격'],
#                         marker_color=colors,
#                         text=average_prices_hotel['가격'],
#                         textposition='auto'))
#     fig.update_layout(title="다른 등급의 숙박 평균 가격",
#                     xaxis_title='등급',
#                     yaxis_title='숙박 평균 가격')

# #     fig.add_annotation(
# #                 x=hotel_star_to_str, # x 축 기준 주석 위치
# #                 # y=hot_pre, # y 축 기준 주석 위치
# #                 text="<b>나의 선택</b>",
# #                 showarrow=True, # 화살표 표시 여부
# #                 font=dict( # 주석 폰트
# #                     size=10,
# #                     color="#ffffff"
# #                     ),
# #                 align="center", # 정렬
# #                 arrowhead=2, # 화살표 머리 크기
# #                 arrowsize=1, # 화살표 크기
# #                 arrowwidth=2, # 화살표 넓이
# #                 arrowcolor="#77CFD9", # 화살표 색상
# #                 ax=20, #박스 위치 가로
# #                 ay=-30,# 박스 위치 세로
# #                 bordercolor="#77CFD9", # 주석 테두리 색상
# #                 borderwidth=2, # 주석 테두리 크기
# #                 borderpad=10, # 주석칸 크기
# #                 bgcolor="#F25D50", # 배경색
# #                 opacity=0.9 # 투명도
# #     )

#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    

# add_vertical_space()


# row5_space1, row5_1, row5_space2, row5_2, row5_space5 = st.columns(
#     (0.1, 1, 0.1, 1, 0.1)
# )

# car = pd.read_csv('data/rent_Car_data_1.csv')
# car['대여일'] = pd.to_datetime(car['대여일'])



# with row5_1:
#     st.subheader("차종별 렌트카 가격")
    
#     # Figure 생성
#     fig = go.Figure()
    
#     # 특정 Arr, Arr_date, grade 기준 Det별 평균 price 계산

#     filtered_df_car = car[(car['지역'] == air_end ) & (car['대여일'] == c_d[0].strftime('%Y-%m-%d'))]

#     average_prices_car = filtered_df_car.groupby('크기')['가격'].mean().reset_index()
    

#     # plotly 그래프 그리기
#     car_type=['경형', '소형', '준중형', '중형', '대형', 'SUV', 'RV', '왜건' ,'사용안함']
#     colors = ['crimson' if i == size else 'lightslategray' for i in car_type]

#     fig.add_trace(go.Bar(x=['경형', '소형', '준중형', '중형', '대형', 'SUV', 'RV', '왜건' ,'사용안함'], y=average_prices_car['가격'],
#                         marker_color=colors,
#                         text=average_prices_car['가격'],
#                         textposition='auto'))
#     fig.update_layout(title="차종별 렌트카 평균 가격",
#                     xaxis_title='차종',
#                     yaxis_title='렌트카 평균 가격')

#     fig.add_annotation(
#                 x=size, # x 축 기준 주석 위치
#                 # y=air_pre, # y 축 기준 주석 위치
#                 text="<b>나의 선택</b>",
#                 showarrow=True, # 화살표 표시 여부
#                 font=dict( # 주석 폰트
#                     size=10,
#                     color="#ffffff"
#                     ),
#                 align="center", # 정렬
#                 arrowhead=2, # 화살표 머리 크기
#                 arrowsize=1, # 화살표 크기
#                 arrowwidth=2, # 화살표 넓이
#                 arrowcolor="#77CFD9", # 화살표 색상
#                 ax=20, #박스 위치 가로
#                 ay=-30,# 박스 위치 세로
#                 bordercolor="#77CFD9", # 주석 테두리 색상
#                 borderwidth=2, # 주석 테두리 크기
#                 borderpad=10, # 주석칸 크기
#                 bgcolor="#F25D50", # 배경색
#                 opacity=0.9 # 투명도
#     )

#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    
    

    
# with row5_2:
#     st.subheader("날짜별 렌트카 가격")
    
#     filtered_df_date = car[(car['지역'] == air_end) & (car['크기'] == size) ]

#     average_prices_date = filtered_df_date.groupby('대여일')['가격'].mean().reset_index()
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=average_prices_date['대여일'], y=average_prices_date['가격'], mode='lines+markers'))
#     fig.update_layout(title="날짜별 렌트카 가격", xaxis_title="날짜", yaxis_title="렌트카 평균 가격")
#     fig.update_xaxes(tickformat="%m-%d (%a)")
#     fig.add_annotation(
#             x=c_d[0], # x 축 기준 주석 위치
#             # y=air_pre, # y 축 기준 주석 위치
#             text="<b>예약일</b>",
#             showarrow=True, # 화살표 표시 여부
#             font=dict( # 주석 폰트
#                 size=10,
#                 color="#ffffff"
#                 ),
#             align="center", # 정렬
#             arrowhead=2, # 화살표 머리 크기
#             arrowsize=1, # 화살표 크기
#             arrowwidth=2, # 화살표 넓이
#             arrowcolor="#77CFD9", # 화살표 색상
#             ax=20, #박스 위치 가로
#             ay=-30,# 박스 위치 세로
#             bordercolor="#77CFD9", # 주석 테두리 색상
#             borderwidth=2, # 주석 테두리 크기
#             borderpad=10, # 주석칸 크기
#             bgcolor="#F25D50", # 배경색
#             opacity=0.9 # 투명도
#         )

#     st.plotly_chart(fig, use_container_width=True)
