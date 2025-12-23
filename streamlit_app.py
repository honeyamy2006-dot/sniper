import streamlit as st

st.set_page_config(page_title="펑크지수 계산기", layout="centered")

st.title("🎯 정시 스나이핑 펑크지수")

st.markdown("### 입력")

avg = st.number_input("3년 평균 추합비율", 0.0, 20.0, 1.0)
vol = st.number_input("변동성", 0.0, 5.0, 0.5)
maxv = st.number_input("3년 최대 추합비율", 0.0, 20.0, 2.0)
median = st.number_input("중앙값", 0.0, 20.0, 1.0)

sustain = avg * (1 - vol)
explosion = maxv * 0.6 + (maxv - median) * 0.25 + vol * 0.15

st.markdown("### 결과")
st.write("지속펑크지수:", round(sustain, 3))
st.write("폭발펑크지수:", round(explosion, 3))
