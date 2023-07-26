import streamlit as st
import datetime
import time
import pandas as pd
import plotly.express as px
import joblib
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(layout="wide")

# 사이트 헤드라인
st.title('일본 여행 경비 예측 프로젝트')

st.markdown("""
 * 항공권, 숙박, 렌트카를 기준으로 비용을 예측해드립니다.
 * 왼쪽 옵션의 조정에 따라 비용이 계산됩니다.
""")


# 사이드바 옵션
st.sidebar.markdown("## 비용 예측 옵션")

with st.sidebar.form('my_form'):
    
    # people = 성인 몇명, 유아 몇명인지 
    
    air_st=st.selectbox('출발 공항을 선택해주세요',
                        ['인천', '청주', '대구', '광주', '부산'])

    air_end=st.selectbox('도착 공항을 선택해주세요',
                            ['도쿄', '오사카', '삿포로', '오키나와', '후쿠오카'])

    clas=st.selectbox('클래스를 선택해주세요',
                            ['economy', 'preminum', 'business', 'first'])
    
    today = datetime.datetime.now()
    start = datetime.date(today.year, 7, 1)
    end = datetime.date(today.year, 9, 30)

    air_d = st.date_input(
        "출국 날짜와 입국 날짜를 선택해주세요",
        (start, datetime.date(today.year, 7, 1)),
        start,
        end,
        format="MM.DD.YYYY",
    )

    st.write('--------------------------')

    h_t=st.selectbox('숙박 유형을 선택해주세요',
                            ['호텔', '게스트하우스,캡슐호텔,호스텔', '리조트,펜션,료칸'])
    # 이거 선택 옵션을 어떻게 해야할지
    # 1. 중복 허용
    # 2. 2번째 3번째 묶인거 하나씩으로 풀어줘야할지

    h_sc=st.slider(
        '평점을 선택해주세요',
        0.0, 10.0, (2.5, 7.5))
    
    h_st=st.slider(
        '호텔 등급을 선택해주세요',
        0, 5, (1,3))


    h_d = st.date_input(
        "숙박 체크인, 아웃 날짜를 선택해주세요",
        (start, datetime.date(today.year, 7, 1)),
        start,
        end,
        format="MM.DD.YYYY",
    )

    st.write('--------------------------')


    c_t=st.selectbox('렌트카 차종을 선택해 주세요',
                            ['경형', '소형', '준중형', '중형', '대형', 'SUV', 'RV', '왜건' ,'사용안함'])


    c_d = st.date_input(
        "렌트카를 사용하는 날짜를 선택해주세요",
        (start, datetime.date(today.year, 7, 1)),
        start,
        end,
        format="MM.DD.YYYY",
    )

    
            
    submitted = st.form_submit_button('적용하기')







df = pd.read_csv('data/air.csv',encoding='CP949')
df['Arr_date'] = pd.to_datetime(df['Arr_date'])


city_to_airport_code_jp = {
    '도쿄': 'NRT',
    '오사카': 'KIX',
    '삿포로': 'CTS',
    '오키나와': 'OKA',
    '후쿠오카': 'FUK'
}

airport_codes_jp = city_to_airport_code_jp[air_end]

city_to_airport_code_kr = {
    '인천': 'ICN',
    '청주': 'CJJ',
    '대구': 'TAE',
    '광주': 'KWJ',
    '부산': 'PUS'
}

airport_codes_kr = city_to_airport_code_kr[air_st]

selected_arr = airport_codes_kr
selected_arr_date = air_d[0].strftime('%Y-%m-%d')
selected_grade = clas
selected_det = airport_codes_jp


st.write(selected_arr,selected_det,selected_arr_date,selected_grade,)


# # 적용하기 눌렀을때 머신러닝 작동
# if st.button("Submit"):
# #항공    
#     # Unpickle classifier
#     air_model = joblib.load("air_model.pkl")
#     # Store inputs into dataframe
#     X_air = pd.DataFrame([[air_st,air_end,clas,air_d]], 
#                      columns = ["Arr", "Det", "grade",'Arr_date','Det_date'])
#     # Get prediction
#     air_pre = air_model.predict(X_air)[0]

# #호텔
#     h_model = joblib.load("h_model.pkl")
#     X_h = pd.DataFrame([[h_t,h_sc,h_st,h_d,]], 
#                      columns = ["hotel_type", "review_score", "grade",'date',''])
#     hot_pre = air_model.predict(X_h)[0]
    
# #렌트카    
#     car_model = joblib.load("car_model.pkl")
#     X_c = pd.DataFrame([[c_t,c_d]], 
#                      columns = ["car_type", "date"])
#     car_pre = car_model.predict(X_c)[0]



col1, col2, col3 = st.columns(3)
air_pre =1
hot_pre =1
car_pre =1

with col1:
   st.header("""{}->{} 항공권
              {}원""".format(air_st,air_end,air_pre))

## 편도 각각 구하기

with col2:
   st.header("""숙박
              {}원""".format(hot_pre))

with col3:
   st.header("""렌트카
              {}원""".format(car_pre))
   

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(3)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)

cola, colb, colc = st.columns(3)


with colc:
   st.header("""총합 : {}원
              """.format(air_pre+hot_pre+car_pre))
   
    

add_vertical_space()

row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row3_1:
    st.subheader("지역별 항공권 가격")
    # Figure 생성
    fig = go.Figure()
    
    # 특정 Arr, Arr_date, grade 기준 Det별 평균 price 계산

    filtered_df = df[(df['Arr'] == selected_arr) & (df['Arr_date'] == selected_arr_date) & 
                    (df['grade'] == selected_grade)]

    average_prices = filtered_df.groupby('Det')['price'].mean().reset_index()

    # plotly 그래프 그리기
    det=['CTS', 'FUK' ,'KIX', 'NRT', 'OKA']
    colors = ['crimson' if i == selected_det else 'lightslategray' for i in det]

    fig.add_trace(go.Bar(x=average_prices['Det'], y=average_prices['price'],
                        marker_color=colors,
                        text=average_prices['price'],
                        textposition='auto'))
    fig.update_layout(title=f"{selected_arr},{selected_det}, {selected_arr_date}, {selected_grade} 일 때 다른 지역의 항공권 평균 가격",
                    xaxis_title='일본 지역',
                    yaxis_title='항공권 평균 가격')

    fig.add_annotation(
                x=selected_det, # x 축 기준 주석 위치
                # y=air_pre, # y 축 기준 주석 위치
                text="<b>나의 선택</b>",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    size=10,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#77CFD9", # 화살표 색상
                ax=20, #박스 위치 가로
                ay=-30,# 박스 위치 세로
                bordercolor="#77CFD9", # 주석 테두리 색상
                borderwidth=2, # 주석 테두리 크기
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=0.9 # 투명도
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    

with row3_2:
    st.subheader("날짜별 항공권 가격")
    
    filtered_df_date = df[(df['Arr'] == selected_arr) & (df['Det'] == selected_det) & 
                    (df['grade'] == selected_grade)]

    average_prices_date = filtered_df_date.groupby('Arr_date')['price'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=average_prices_date['Arr_date'], y=average_prices_date['price'], mode='lines+markers'))
    fig.update_layout(title="날짜별 항공권 가격", xaxis_title="날짜", yaxis_title="항공권 평균 가격")
    fig.update_xaxes(tickformat="%m-%d (%a)")
    fig.add_annotation(
            x=air_d[0], # x 축 기준 주석 위치
            # y=air_pre, # y 축 기준 주석 위치
            text="<b>출국</b>",
            showarrow=True, # 화살표 표시 여부
            font=dict( # 주석 폰트
                size=10,
                color="#ffffff"
                ),
            align="center", # 정렬
            arrowhead=2, # 화살표 머리 크기
            arrowsize=1, # 화살표 크기
            arrowwidth=2, # 화살표 넓이
            arrowcolor="#77CFD9", # 화살표 색상
            ax=20, #박스 위치 가로
            ay=-30,# 박스 위치 세로
            bordercolor="#77CFD9", # 주석 테두리 색상
            borderwidth=2, # 주석 테두리 크기
            borderpad=10, # 주석칸 크기
            bgcolor="#F25D50", # 배경색
            opacity=0.9 # 투명도
        )
    fig.add_annotation(
        x=air_d[1], # x 축 기준 주석 위치
        # y=air_pre, # y 축 기준 주석 위치
        text="<b>입국</b>",
        showarrow=True, # 화살표 표시 여부
        font=dict( # 주석 폰트
            size=10,
            color="#ffffff"
            ),
        align="center", # 정렬
        arrowhead=2, # 화살표 머리 크기
        arrowsize=1, # 화살표 크기
        arrowwidth=2, # 화살표 넓이
        arrowcolor="#77CFD9", # 화살표 색상
        ax=20, #박스 위치 가로
        ay=-30,# 박스 위치 세로
        bordercolor="#77CFD9", # 주석 테두리 색상
        borderwidth=2, # 주석 테두리 크기
        borderpad=10, # 주석칸 크기
        bgcolor="#F25D50", # 배경색
        opacity=0.9 # 투명도
    )
    st.plotly_chart(fig, use_container_width=True)




add_vertical_space()


row4_space1, row4_1, row4_space2, row4_2, row4_space4 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


hotel = pd.read_csv('data\hotel_how_far.csv',encoding='CP949')
hotel['입실'] = pd.to_datetime(hotel['입실'])

selected_hotel_date = h_d[0].strftime('%Y-%m-%d')
st.write(h_t,h_sc,h_st,selected_hotel_date,air_end)



with row4_1:

    fig = go.Figure()

    filtered_df_hotel = hotel[(hotel['지역'] == air_end) & (hotel['입실'] ==selected_hotel_date)]

    average_prices_hotel = filtered_df_hotel.groupby('숙박유형')['가격'].mean().reset_index()

    # plotly 그래프 그리기
    hotel_type=['게스트하우스,캡슐호텔,호스텔', '리조트,펜션,료칸', '호텔']
    colors = ['crimson' if i == h_t else 'lightslategray' for i in hotel_type]

    fig.add_trace(go.Bar(x=average_prices_hotel['숙박유형'], y=average_prices_hotel['가격'],
                        marker_color=colors,
                        text=average_prices_hotel['가격'],
                        textposition='auto'))
    fig.update_layout(title="다른 유형의 숙박 평균 가격",
                    xaxis_title='숙박 유형',
                    yaxis_title='숙박 평균 가격')

    fig.add_annotation(
                x=h_t, # x 축 기준 주석 위치
                # y=hot_pre, # y 축 기준 주석 위치
                text="<b>나의 선택</b>",
                showarrow=True, # 화살표 표시 여부
                font=dict( # 주석 폰트
                    size=10,
                    color="#ffffff"
                    ),
                align="center", # 정렬
                arrowhead=2, # 화살표 머리 크기
                arrowsize=1, # 화살표 크기
                arrowwidth=2, # 화살표 넓이
                arrowcolor="#77CFD9", # 화살표 색상
                ax=20, #박스 위치 가로
                ay=-30,# 박스 위치 세로
                bordercolor="#77CFD9", # 주석 테두리 색상
                borderwidth=2, # 주석 테두리 크기
                borderpad=10, # 주석칸 크기
                bgcolor="#F25D50", # 배경색
                opacity=0.9 # 투명도
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    
hotel_star = {
    1:'1성급',
    2:'2성급',
    3:'3성급',
    4:'4성급',
    5:'5성급'
}


with row4_2:
    fig = go.Figure()

    filtered_df_hotel = hotel[(hotel['지역'] == air_end) & (hotel['입실'] ==selected_hotel_date) & (hotel['숙박유형'] == h_t)]

    average_prices_hotel = filtered_df_hotel.groupby('등급')['가격'].mean().reset_index()

    # plotly 그래프 그리기
    # hotel_type=['1성급','2성급','3성급','4성급','5성급']
    # colors = ['crimson' if i == hotel_star_to_str else 'lightslategray' for i in hotel_type]

    fig.add_trace(go.Bar(x=average_prices_hotel['등급'], y=average_prices_hotel['가격'],
                        # marker_color=colors,
                        text=average_prices_hotel['가격'],
                        textposition='auto'))
    fig.update_layout(title="다른 등급의 숙박 평균 가격",
                    xaxis_title='등급',
                    yaxis_title='숙박 평균 가격')

#     fig.add_annotation(
#                 x=hotel_star_to_str, # x 축 기준 주석 위치
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

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    



