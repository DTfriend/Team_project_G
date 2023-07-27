import streamlit as st
import pandas as pd
import streamlit_survey as ss
from datetime import datetime


st.set_page_config(
    page_title="Survey",
    page_icon="✅",
)

# 사이트 헤드라인
st.title('일본 여행 비용 예측')

st.markdown("""
 * AI를 통해 항공권, 숙박, 렌트카의 비용을 예측해드립니다.
 * 아래의 질문에 답해주세요!
""")

df = pd.read_csv('data/air.csv',encoding='CP949')


city_to_airport_code_jp = {
    '상관없음' : 'NRT HND',
    '하네다' : 'HND',
    '나리타': 'NRT',
    '오사카': 'KIX',
    '삿포로': 'CTS',
    '오키나와': 'OKA',
    '후쿠오카': 'FUK'
}


city_to_airport_code_kr = {
    '인천공항': 'ICN',
    '청주공항': 'CJJ',
    '대구공항': 'TAE',
    '광주공항': 'KWJ',
    '부산공항': 'PUS'
}

class_to_eng={
    '상관 없음': 'none',
    '이코노미': 'economy',
    '프리미엄': 'premium',
    '비즈니스': 'business',
    '퍼스트': 'first'
}

dict_around={'상관 없음' : '직항 경유 1',
'직항만':'직항',
'상관 없음':'경유 1'}

dict_how_far={'0~20':0, '21~50':1,'그외':2}

size_mapping = {'RV':0,'SUV':1,'경형':2,'대형':3,'소형':4,'왜건':5,'준중형':6,'중형':7}


with st.expander(" ", expanded=True):
    survey = ss.StreamlitSurvey("Survey Example")
    pages = survey.pages(10, on_submit=lambda: st.success("비용을 계산 중 입니다..!"))
    with pages:
      
# 1. 몇 명이서 여행을 가시나요? 
        if pages.current == 0:
            st.markdown("#### 1. 몇 명이서 여행을 가시나요?")
            user_count = survey.number_input( 'user_count', min_value=1, max_value=10)
            st.session_state['user_count'] = user_count


# 2. 누구와 함께 가시나요?(객관식)
# ⇒ 1) 가족 2) 연인 3) 친구 등
            if user_count >= 2:
                st.markdown("#### 2. 누구와 함께 가시나요?")
                user_with =survey.radio(
                   'user_with',  options=["가족", "연인", "친구"], index=0, label_visibility="collapsed", horizontal=True
                )
                st.session_state['user_with'] = user_with
                
                
# 3. 여행 기간은 어떻게 되시나요?(~9월까지 제공)
# ⇒ 달력으로 표시(직접 선택) == 출발, 도착일 정해짐 + 일수계산 필요
        if pages.current == 1:
                st.markdown("#### 3. 여행 기간은 어떻게 되시나요?")
                air_st = survey.dateinput('출국날짜')
                air_end = survey.dateinput('입국날짜')
                st.markdown("##### 여행 기간")
                if air_st == air_end :
                  st.markdown("##### 날짜를 선택해주세요")
                elif air_st < air_end :
                  dir_days=(datetime.strptime(air_end, '%Y-%m-%d')-datetime.strptime(air_st, '%Y-%m-%d')).days
                  st.markdown("##### {}일".format(str(dir_days)))
                else : 
                  st.markdown("##### 날짜를 올바르게 선택해주세요")
                st.session_state['air_st'] = air_st
                st.session_state['air_end'] = air_end
                st.session_state['dir_days'] = dir_days
                
    

# - 항공권 질문
# 4. 일본 어디로 가시나요?
# ⇒ 1) 도쿄 2) 오사카 3) 삿포로 4) 오키나와 5) 후쿠오카
        if pages.current == 2:
            st.markdown("#### 4. 일본 어디로 가시나요?")
            arr =survey.radio(
               'arr', options=["도쿄", "오사카", "삿포로" , '오키나와', '후쿠오카'], index=0, label_visibility="collapsed", horizontal=True
            )
            arr_i=city_to_airport_code_jp[arr]
            st.session_state['arr'] = city_to_airport_code_jp[arr]

# 5. 어느 공항이 좋으신가요?
# 1) 상관없음 2) 하네다 3) 나리타
# :if 상관없음 선택 시 둘 다 제공
            if arr == '도쿄':
                st.markdown("#### 5. 어느 공항이 좋으신가요?")
                arr =survey.radio(
                 'arr2',    options=['상관없음' ,'하네다' ,'나리타'], index=0, label_visibility="collapsed", horizontal=True
                )
            arr_i=city_to_airport_code_jp[arr]
            st.session_state['arr'] = city_to_airport_code_jp[arr]
            

# 6. 어디에서 출발하시나요?
# ⇒ 1) 인천공항 2) 청주공항 3) 광주공항 4) 대구공항 5)김해공항
        if pages.current == 3:
            st.markdown("#### 6. 어디 공항에서 출발하시나요?")
            det =survey.radio(
              'det',   options=['인천공항' ,'청주공항' ,'광주공항' ,'대구공항', '김해공항'], index=0, label_visibility="collapsed", horizontal=True
            )
            det_i=city_to_airport_code_jp[det]
            st.session_state['det'] = city_to_airport_code_jp[det]


# 7. 항공편에 선호하는 좌석 등급이 있나요?(상관없음을 빼고 복수선택 가능을 해도 괜찮을 듯)
# ⇒ 1) 상관 없음 2) 이코노미 3)프리미엄 이코노미 4) 비즈니스 5)퍼스트
        if pages.current == 4:
            st.markdown("#### 7. 항공편에 선호하는 좌석 등급이 있나요?")
            air_cls =survey.radio(
              'air_cls',   options=['상관 없음' ,'이코노미' ,'프리미엄' ,'이코노미' ,'비즈니스' ,'퍼스트'], index=0, label_visibility="collapsed", horizontal=True
            )
            air_cls_i=class_to_eng[air_cls]
            st.session_state['air_cls'] = class_to_eng[air_cls]



# 8. 경유를 해도 괜찮나요?
# ⇒ 1) 상관없음 2) 직항만

# : if 해당 항공권이 없다면(ex 퍼스트&직항 없는경우 많음) [항공권이 없습니다] 팝업 후
# ⇒ 3번 부터 다시 선택
        if pages.current == 5:
            st.markdown("#### 8. 경유를 해도 괜찮나요?")
            air_around =survey.radio(
              'air_around', options=['상관 없음' ,'직항만' ,'없을 경우'], index=0, label_visibility="collapsed", horizontal=True
            )
            st.session_state['air_around'] = air_around
            filtered_df = df[(df['Arr'] == arr_i) & (df['Det']==det_i) & (df['Arr_date'] == air_st) & (df['grade'] == air_cls_i)]
            if not filtered_df:
              st.markdown('조건에 맞는 항공권이 없습니다')
            
            
            
            # if air_around == '없을 경우':
            #     st.write("3. 여행 기간은 어떻게 되시나요?")
            #     air_st2 = survey.dateinput('출국날짜')
            #     air_end2 = survey.dateinput('입국날짜')
            #     st.write("여행 기간")
            #     st.write((datetime.strptime(air_end, '%Y-%m-%d')-datetime.strptime(air_st, '%Y-%m-%d')).days)
                    


# 9. 항공권을 예약할 때 어느 요소가 더 중요한가요?

# ⇒  1) 가격 2) 출발 시간

# : if 가격 선택 시 항공권3에서 선택한 등급의 출발날짜/ 도착날짜 가장 저렴한 항공권 선택 후 가격 예측

#   else 출발 시간 선택한 경우 6번으로
        if pages.current == 6:
            st.markdown("#### 9. 항공권을 예약할 때 어느 요소가 더 중요한가요?")
            air_pref =survey.radio(
              'air_pref',   options=[ '가격' , '출발 시간'], index=0, label_visibility="collapsed", horizontal=True
            )
            st.session_state['air_pref'] = air_pref
            


# 10. 시간대는 언제가 좋나요? 

# ⇒ 박스 선택(오전(~12:00PM),오후(~18:00),저녁(18:00~) )으로 가는날[박스], 오는날[박스]해서 한번에 받기
# 7-1 갈 때는 언제가 좋나요?

# ⇒ 1) 오전(~12:00PM) 2)오후(~18:00) 3)저녁(18:00~)

# 7-2 올 때는 언제가 좋나요?
# ⇒ 1) 오전(~12:00PM) 2)오후(~18:00) 3)저녁(18:00~)
# # 7번이나 7-1/7-2 중에 하나를 질문지로 하면 될듯합니다.
        if pages.current == 7:
            if air_pref == '출발 시간' :
              st.markdown("#### 10. 가는 시간대는 언제가 좋나요?")
              time_st =survey.radio(
                'time_st',  options=['오전(~12:00PM)' ,'오후(~18:00)' , '저녁(18:00~)'], index=0, label_visibility="collapsed", horizontal=True
              )
              st.session_state['time_st'] = time_st
              
              st.markdown("#### 11. 오는 시간대는 언제가 좋나요?")
              time_end =survey.radio(
                  'time_end', options=['오전(~12:00PM)' ,'오후(~18:00)' , '저녁(18:00~)'], index=0, label_visibility="collapsed", horizontal=True
              )
              st.session_state['time_end'] = time_end

# 선택 완료 시 해당 시간대의 가장 저렴한 항공권 선택 후 가격 예측




#호텔명	입실	퇴실	지역	숙박유형	별점	등급	가격	가장 가까운 공항	가장 가까운 공항과의 거리	가장 가까운 공항까지 시간
#입실 == 출발날이랑 같다고 가정
#지역 == 도착지랑 같다고 가정


        if pages.current == 8:
            st.markdown("#### 11. 어떤 숙박 유형을 찾을까요?")
            h_t=survey.radio('h_t',
                        option=['호텔', '게스트하우스,캡슐호텔,호스텔', '리조트,펜션,료칸'], index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['h_t'] = h_t
        
        
        if pages.current == 9:
            st.markdown("#### 12. 공항에서 호텔과의 거리를 선택해주세요")
            h_far=survey.radio('h_far',option=['0~20분 거리', '21~50분 거리', '그 외'], index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['h_far'] = dict_how_far[h_far]
            
            
            
# 렌트카 :: 지역	공항	이름	대여일	반납일	크기	제한인원수	보험	가격	브랜드

        if pages.current == 10:
            st.markdown("#### 12. 렌트카는 언제 빌리실 예정이신가요?")
            car_st = survey.dateinput('빌리는 날짜')
            car_end = survey.dateinput('반납하는 날짜')
            st.markdown("##### 렌트 기간")
            if car_st == car_end :
              st.markdown("##### 날짜를 선택해주세요")
            elif car_st < car_end :
              car_days=(datetime.strptime(car_end, '%Y-%m-%d')-datetime.strptime(car_st, '%Y-%m-%d')).days
              st.markdown("##### {}일".format(str(car_days)))
            else : 
              st.markdown("##### 날짜를 올바르게 선택해주세요")
            st.session_state['car_st'] = car_st
            st.session_state['car_end'] = car_end
            st.session_state['car_days'] = car_days
            
            
        if pages.current ==11:
            st.markdown("#### 13. 차종은 어떤 걸 선호하시나요?")
            car_size=survey.radio('car_size',
                        option=['RV', 'SUV', '경형', '대형', '소형', '왜건', '준중형', '중형'], index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['car_size'] = car_size
            
            
        if pages.current ==12:
            st.markdown("#### 14. 보험은 어떤 걸로 할까요?")
            insurance=survey.radio('insurance',
                        option=['면책커버보험 포함', '스탠다드플랜 포함', '프리미엄플랜 포함'], index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['insurance'] = insurance
                 
        if pages.current ==13:
            st.markdown("#### 14. 선호하시는 자동차 브랜드가 있나요?")
            brand=survey.radio('brand',
                        option=['닛산', '다이하쓰', '도요타','마쯔다','미쓰비시','스바루','스즈키','혼다'], index=0, label_visibility="collapsed", horizontal=True
                     )
            st.session_state['brand'] = brand
          
          
