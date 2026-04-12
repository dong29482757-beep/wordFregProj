import streamlit as st
import pandas as pd


def show_main_header():
    """메인 헤더 표시"""
    st.header("[미니 프로젝트] 단어 빈도수 분석 웹 대시보드")


@st.dialog("데이터 미리보기")
def preview_data(df):
    """데이터 미리보기"""
    st.dataframe(df)


def check_file_uploaded(file):
    """업로드된 파일 확인"""
    if file:
        if st.button("데이터 파일 확인"):
            data = pd.read_csv(file)
            preview_data(data)


def get_user_settings():
    """사용자 설정 받기"""
    
    col_input = st.text_input("데이터가 있는 컬럼명")
    
    st.subheader("설정")
    
    with st.form("settings_form"):
        show_bar_chart = st.checkbox("빈도수 그래프")
        bar_num = st.slider("단어 수", 10, 50, 30, 1)
        
        show_word_cloud = st.checkbox("워드 클라우드")
        cloud_num = st.slider("단어 수", 20, 500, 250, 1, key="cloud")
        
        submit_btn = st.form_submit_button("분석 시작")
        
        if submit_btn:
            if not show_bar_chart and not show_word_cloud:
                st.warning("빈도수 그래프나 워드 클라우드를 선택하세요")
                return None
            
            return {
                "column": col_input,
                "bar": show_bar_chart,
                "bar_count": bar_num,
                "cloud": show_word_cloud,
                "cloud_count": cloud_num
            }
    
    return None