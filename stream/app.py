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
                            ['Economy', 'Preminum', 'Business', 'First'])
    
    today = datetime.datetime.now()
    start = datetime.date(today.year, 7, 1)
    end = datetime.date(today.year, 8, 31)

    air_d = st.date_input(
        "출국 날짜와 입국 날짜를 선택해주세요",
        (start, datetime.date(today.year, 7, 1)),
        start,
        end,
        format="MM.DD.YYYY",
    )

    st.write('--------------------------')

    h_t=st.selectbox('숙박 유형을 선택해주세요',
                            ['호텔', '게스트하우스/캡슐호텔/호스텔', '리조트/펜션/료칸'])
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
                            ['소형', '중형', '대형', 'SUV', '밴' , '사용안함'])


    c_d = st.date_input(
        "렌트카를 사용하는 날짜를 선택해주세요",
        (start, datetime.date(today.year, 7, 1)),
        start,
        end,
        format="MM.DD.YYYY",
    )

    
    arr=st.selectbox('arr_test',
                        ['Feature A', 'Feature B', 'Feature C','Feature D', 'Feature E'])
    price = st.selectbox('price_test',
                        [20, 14, 23, 25, 22])
            
    submitted = st.form_submit_button('적용하기')


row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
with row3_1:
    # Figure 생성
    fig = go.Figure()
    x=['Feature A', 'Feature B', 'Feature C','Feature D', 'Feature E']

    #막대 색 리스트 
    colors = ['crimson' if i == arr else 'lightslategray' for i in x]


    # Trace 추가
    fig.add_trace(go.Bar(x=['Feature A', 'Feature B', 'Feature C','Feature D', 'Feature E'],y=[20, 14, 23, 25, 22],
        marker_color=colors))

    fig.add_annotation(
                x=arr, # x 축 기준 주석 위치
                y=price, # y 축 기준 주석 위치
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


    

# # 적용하기 눌렀을때 머신러닝 작동
# if st.button("Submit"):
# #항공    
#     # Unpickle classifier
#     air_model = joblib.load("air_model.pkl")
#     # Store inputs into dataframe
#     X_air = pd.DataFrame([[air_st,air_end,clas,air_d,]], 
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
    
    
    
    

    

# col1, col2, col3 = st.columns(3)

# with col1:
#    st.header("""{}->{} 항공권
#               {}원""".format(air_st,air_end,air_pre))

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
#     """ 
#     #### 총합 : {}원
#     """.format(air_pre+hot_pre+car_pre)
    


add_vertical_space()


# row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
#     (0.1, 1, 0.1, 1, 0.1)
# )
# df = pd.read_csv('data/air.csv',encoding='CP949')

# with row3_1:
#     st.subheader("지역별 항공권 가격")

#     df = df.sort_values(by="Det")
    
#     fig = px.bar(
#         df[["Det", "price"]],
#         x="Det",
#         y="price",
#         title="지역별 항공권 가격",
#         color_discrete_sequence=["#9EE6CF"],
#     )
#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#     st.markdown(
#         "나의 선택 {} -> {} ".format(
#             air_st, air_end
#         )
#     )
    
    


# with row3_2:
#     st.subheader("날짜별 항공권 가격")
    
#     df['Arr_date'] = pd.to_datetime(df['Arr_date'])
#     df3 = df.groupby('Arr_date')['price'].mean().reset_index()

#     fig = px.line(
#         df3,
#         x="Arr_date",
#         y="price",
#         title="날짜별 항공권 가격",
#     )
#     fig.update_xaxes(title_text="날짜별 항공권 가격")
#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    







