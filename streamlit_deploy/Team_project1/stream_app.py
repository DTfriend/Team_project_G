import streamlit as st
import requests

def main():
    st.title("Flask와 Streamlit을 이용한 머신러닝 앱")

    # Streamlit에서 입력값을 받음
    input_value = st.number_input("머신러닝 모델에 입력할 값: ", value=1.0)

    # Flask 앱으로 입력값을 전송
    url = 'https://port-0-flask-deploy-cu6q2blkkexse9.sel4.cloudtype.app'
    data = {'input_value': input_value}
    response = requests.post(url, json=data)
    
    # Flask 앱으로부터 예측 결과를 받아와 출력
    # Flask 앱으로부터 예측 결과를 받아와 출력adfa
    if response.status_code == 200:
        result = response.json()
        prediction = result['prediction']
        st.write(f"머신러닝 모델의 예측 결과: {prediction}")

if __name__ == "__main__":
    main()