import pandas as pd
import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud


def load_data_from_csv(csv_file, col_name):
    """CSV 파일에서 데이터 로드"""
    df = pd.read_csv(csv_file)
    df.dropna(subset=[col_name], inplace=True)
    data_list = list(df[col_name])
    return data_list


def tokenize_korean_corpus(text_corpus, tokenize_func, tag_list=None, stop_words=None):
    """한국어 텍스트 토큰화"""
    if stop_words is None:
        stop_words = []
    
    result_tokens = []
    
    for text in text_corpus:
        if tag_list:
            tokens = [word for word, tag in tokenize_func(text) 
                     if tag in tag_list and word not in stop_words]
        else:
            tokens = [word for word, tag in tokenize_func(text) 
                     if word not in stop_words]
        result_tokens.extend(tokens)
    
    return result_tokens


def get_word_frequency(token_list):
    """단어 빈도수 계산"""
    return Counter(token_list)


def setup_korean_font(font_file_path):
    """matplotlib 한글 폰트 설정"""
    font_prop = font_manager.FontProperties(fname=font_file_path)
    font_name = font_prop.get_name()
    rc('font', family=font_name)


def draw_bar_chart(word_counter, word_count, chart_title=None, 
                   x_axis_label=None, y_axis_label=None, font_file=None):
    """막대 그래프 생성"""
    plt.clf()
    
    # 상위 단어 추출
    top_words = word_counter.most_common(word_count)
    
    # 단어와 빈도 분리
    words = [w for w, c in top_words]
    freqs = [c for w, c in top_words]
    
    # 한글 폰트 설정
    if font_file:
        setup_korean_font(font_file)
    
    # 수평 막대 그래프
    plt.barh(words[::-1], freqs[::-1])
    
    # 그래프 제목 및 레이블
    if chart_title:
        plt.title(chart_title)
    if x_axis_label:
        plt.xlabel(x_axis_label)
    if y_axis_label:
        plt.ylabel(y_axis_label)
    
    # 저장 및 출력
    plt.savefig("bar_graph.png")
    st.pyplot(plt.gcf())


def draw_wordcloud(word_counter, word_count, font_file):
    """워드클라우드 생성"""
    wc = WordCloud(
        font_path=font_file,
        width=800,
        height=600,
        max_words=word_count,
        background_color='ivory'
    )
    
    with st.spinner("워드 클라우드 생성중..."):
        cloud = wc.generate_from_frequencies(word_counter)
        cloud.to_file("wordcloud_result.png")
        st.image("wordcloud_result.png")