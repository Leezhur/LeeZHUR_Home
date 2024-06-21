import streamlit as st
from PIL import Image  # local에서 이미지 불러오기
import exchange_rate

#01. 사이드바 화면
st.sidebar.header("Login")
user_id = st.sidebar.text_input("ID 입력", value='', max_chars=15)
user_password = st.sidebar.text_input("P/W 입력", value='', type="password")

if user_id == "suyoung" and user_password == '1234':
    st.sidebar.header("이수영's 포트폴리오")

    # # 선택할 데이터 목록 (여러 개의 데이터 불러올 때는 리스트나 딕셔너리로 불러오기)
    # sel_options = ['', '진주 귀걸이를 한 소녀', '별이 빛나는 밤',
    #             '절규', '생명의 나무', '월하장인']

    # # 콤보 상자 (내가 선택한 작품명)
    # user_opt = st.sidebar.selectbox("▼ 좋아하는 작품 선택", sel_options, index=0)  # index : 기본 선택값

    # .write == print
    # st.sidebar.write("※ Choice한 작품 : ", user_opt)

    # radio Box 생성
    menu = st.sidebar.radio("▼ Menu Choice ▼", ['환율 조회', '부동산 조회(EDA)', '인공지능 예측/분류'], index=None)

    if menu == '환율 조회':
        exchange_rate.exchange_main()
        st.sidebar.write("환율 조회")
    elif menu == '부동산 조회(EDA)':
        st.sidebar.write("부동산 조회(EDA)")
    elif menu == '인공지능 예측/분류':
        st.sidebar.write("인공지능 예측/분류")
    else:
        st.sidebar.write("메뉴를 선택해 주세요!")
    # #02. 메인 화면
    # st.subheader("Main 화면")


