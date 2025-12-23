import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="정시 펑크지수 분석기", layout="wide")

# 기록 보관을 위한 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기")
st.markdown("---")

# 1. 입력칸 (가로 배치)
with st.container():
    cols = st.columns([1.5, 1.5, 1, 1, 1])
    univ = cols[0].text_input("대학 이름")
    dept = cols[1].text_input("학과명")
    r23 = cols[2].number_input("23 추합비율", format="%.3f")
    r24 = cols[3].number_input("24 추합비율", format="%.3f")
    r25 = cols[4].number_input("25 추합비율", format="%.3f")

if st.button("분석 실행 및 기록"):
    # 데이터 리스트화
    rates = [r23, r24, r25]
    
    # 2. 자동 계산 로직 (은서의 필기 반영)
    avg_val = np.mean(rates)
    vol_val = np.std(rates) / avg_val if avg_val != 0 else 0
    min_val = np.min(rates)
    median_val = np.median(rates)
    max_val = np.max(rates)
    
    # 지수 계산
    sustain = avg_val * (1 - vol_val)
    explosion = max_val * 0.6 + (max_val - median_val) * 0.25 + vol_val * 0.15
    
    # 3. 타입 판정 (3x3 Matrix)
    # 지속펑크타입 (A/B/C)
    if sustain >= 0.8: s_type = "A"
    elif sustain >= 0.4: s_type = "B"
    else: s_type = "C"
    
    # 폭발펑크타입 (S/M/F)
    if explosion >= 1.3: e_type = "S"
    elif explosion >= 0.8: e_type = "M"
    else: e_type = "F"
    
    final_type = f"{s_type}-{e_type}"
    
    # 기록 저장
    st.session_state.history.append({
        "대학": univ, "학과": dept, "평균": avg_val, "변동성": vol_val,
        "최소": min_val, "중앙": median_val, "지속지수": sustain, "폭발지수": explosion,
        "타입": final_type
    })

# 4. 시각적 직관 (결과 리스트 출력)
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    
    def color_type(val):
        color = 'white'
        if 'A-S' in val: color = '#FF4B4B' # 강렬한 빨강
        elif 'B-S' in val or 'A-M' in val: color = '#FFA500' # 주황
        elif 'C-F' in val: color = '#808080' # 회색
        return f'background-color: {color}; color: black; font-weight: bold'

    st.subheader("📋 분석 기록 및 비교")
    # 타입 컬럼을 강조하기 위해 스타일 적용
    st.dataframe(df.style.applymap(color_type, subset=['타입']))
