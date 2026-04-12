import streamlit as st
from konlpy.tag import Okt
import streamlit_components as ui
import korean_text_analyzer as analyzer

# 페이지 설정
st.set_page_config(
    page_title="단어 빈도수 분석",
    page_icon="📊"
)

# 헤더
ui.show_main_header()

# 사이드바
with st.sidebar:
    st.subheader("파일 선택")
    
    uploaded_file = st.file_uploader(
        "파일 선택",
        type=['csv'],
        label_visibility="collapsed"
    )
    
    ui.check_file_uploaded(uploaded_file)
    
    config = None
    
    if uploaded_file:
        config = ui.get_user_settings()
    else:
        st.warning("파일을 첨부해주세요")


# 메인 영역
if uploaded_file and config and config["column"]:
    
    st.subheader("단어 빈도수 시각화")
    
    # 불용어 설정 (코드에 직접 포함)
    stopwords = [
        '영화', '정말', '진짜', '하는', '입니다', '좀', '그', '이', '것', '잘', '점',
        '수', '나', '내', '들', '보', '본', '보고', '하고', '있는', '생각', '사람', 
        '더', '그냥', '정도', '할', '볼', '꼭', '왜', '때', '봤는데', '보는', '느낌',
        '있다', '하다', '되다', '같다', '이다', '없다', '너무', '좀'
    ]
    
    # 형태소 분석기 설정
    okt = Okt()
    pos_tags = ['Noun', 'Verb', 'Adjective']
    font_path = 'c:/Windows/Fonts/malgun.ttf'
    
    try:
        with st.spinner("분석 중..."):
            # 데이터 로드
            corpus = analyzer.load_data_from_csv(uploaded_file, config['column'])
            
            # 토큰화
            tokens = analyzer.tokenize_korean_corpus(
                corpus, 
                okt.pos, 
                pos_tags, 
                stopwords
            )
            
            # 빈도수 계산
            word_freq = analyzer.get_word_frequency(tokens)
        
        st.success(f"분석이 완료되었습니다! (총 {len(tokens):,}개 단어)")
        
        # 시각화
        if config.get("bar"):
            with st.spinner("빈도수 그래프 생성중..."):
                analyzer.draw_bar_chart(
                    word_freq,
                    config['bar_count'],
                    "영화 리뷰",
                    "빈도수",
                    "키워드",
                    font_path
                )
        
        if config.get("cloud"):
            analyzer.draw_wordcloud(
                word_freq,
                config['cloud_count'],
                font_path
            )
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.info("컬럼명이 올바른지 확인해주세요.")

elif uploaded_file and config and not config["column"]:
    st.warning("컬럼명을 입력하세요")

elif not uploaded_file:
    st.info("파일을 업로드하여 시작하세요")