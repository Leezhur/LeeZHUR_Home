import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO  # Text를 제외한 나머지 파일(이미지, 동영상, 엑셀 파일 등)들을바이너리 파일로 인식

#데이터 크롤링
def get_exchange_rate_data(currency_code, last_page_num):
    # base_url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver"
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num+1):
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_num}"

        dfs = pd.read_html(url, header=1,encoding='cp949')
        
        # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if (page_num==1):
                print(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                print(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df
# -----------------------------------------------------------------------------

def exchange_main():
    st.subheader("환율 정보를 가져오는 Web App")

    #딕셔너리로 통화 정보
    currency_name_dict = {'미국': 'USD', '유럽연합': 'EUR', '일본 (100엔)': 'JPY', '중국': 'CNY'}

    #콤보상자 생성
    currency_name = st.selectbox("▼ 통화 선택", currency_name_dict.keys())

    clicked = st.button("환율 Data 가져오기")  # Button

    select_currency_code = currency_name_dict[currency_name]  # key값에 해당하는 value값
    last_page = 10  # Page

    if clicked == True: # Button이 Click되면 실행
        #환율 Code 크롤링
        df_exchange = get_exchange_rate_data(select_currency_code, last_page)

        #원하는 Column만 선택 (*전일대비 Column 삭제)
        df_exchange_rate = df_exchange[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

        df_exchange_rate = df_exchange_rate.set_index(['날짜']) # 날짜 Column을 index로 지정

        #웹페이지 내에 환율 데이터 DataFrame 출력하기
        st.dataframe(df_exchange_rate)

        #차트 그리기(선그래프, Pandas 이용)
        df_exchange_rate_2 = df_exchange_rate.copy()  # 위 DataFrame에 사용할 Data와 차트에 사용할  Data 분리
        df_exchange_rate_2.index = pd.to_datetime(df_exchange_rate_2.index)  # 날짜 형식으로 변환

        #Cf_ Pandas로 그래프 생성 시, index가 X축이 됨

        ax = df_exchange_rate_2['매매기준율'].plot(grid=True, figsize=(10,5))        # 웹 앱에 출력하기 위해 변수(ax)에 저장
        ax.set_title("Exchange Rate Graph", fontsize = 12) # Web App에서 한글 출력 설정하려면 코드가 복잡하므로 일단 영어로 작성
        ax.set_ylabel(f'KRW/{select_currency_code}')
        ax.set_xlabel('Date')
        fig = ax.get_figure()  #차트 객체로 변환!
        st.pyplot(fig)

        # File Download
        st.subheader("============= 환율 Data Download =============")
        
        #Text Data 변환
        csv_data = df_exchange_rate.to_csv()  # df_exchange_rate.to_csv() : 가상의 공간에 기억 시키기
        # 파일명 적지 않으면 가상 메모리(csv_data 변수)에 저장됨 (파일명 적으면 local에 저장됨)

        #Excel Data 변환
        excel_data = BytesIO()  #메모리 버퍼에 바이너리 객체 생성
        df_exchange_rate.to_excel(excel_data)   # df_exchange_rate.to_excel 의 데이터들이 excel_data 바이너리 객체에 들어간다!


        #2개의 세로단을 구성
        col = st.columns(2)  # st내에서 칸을 2개로 나누기 (list로 구성됨  Ex_ col[0], col[1])
        with col[0]:
            st.download_button("CSV File Download", csv_data, file_name="Exchange_Rate_Data.csv")
        with col[1]:
            st.download_button("Excel File Download", excel_data, file_name="Exchange_Rate_Data.xlsx")




if __name__ == "__main__":
    exchange_main()