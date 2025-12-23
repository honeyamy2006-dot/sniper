import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

# 세션 상태 초기화 (데이터 저장소)
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기")

# --- 1. 입력칸 (가로 그룹화 유지) ---
with st.expander("➕ 데이터 입력", expanded=True):
    col1, col2 = st.columns(2)
    univ = col1.text_input("대학 이름")
    dept = col2.text_input("학과명")

    st.markdown("---")
    st.markdown("**인원수 입력**")
    row_count = st.columns(3)
    c23 = row_count[0].number_input("23 추합인원", step=1, value=0)
    c24 = row_count[1].number_input("24 추합인원", step=1, value=0)
    c25 = row_count[2].number_input("25 추합인원", step=1, value=0)

    st.markdown("**비율(%) 입력**")
    row_rate = st.columns(3)
    r23 = row_rate[0].number_input("23 비율(%)", format="%.3f", value=0.0)
    r24 = row_rate[1].number_input("24 비율(%)", format="%.3f", value=0.0)
    r25 = row_rate[2].number_input("25 비율(%)", format="%.3f", value=0.0)

# --- 2. 계산 로직 (은서의 엑셀 함수 100% 적용) ---
if st.button("🚀 분석 및 기록 저장"):
    if univ and dept:
        rates = [r23, r24, r25]
        J_avg = np.mean(rates)
        K_vol = np.max(rates) - np.min(rates)
        L_min = np.min(rates)
        M_median = np.median(rates)
        
        # 은서 수식 반영
        sustain = (L_min * 0.5) + (M_median * 0.3) + (J_avg * 0.2)
        explosion = (np.max(rates) * 0.6) + ((np.max(rates) - M_median) * 0.25) + (K_vol * 0.15)
        
        # 타입 판정
        if sustain >= 0.55 and L_min >= 0.4: s_type = "A"
        elif sustain >= 0.45 and L_min >= 0.25: s_type = "B"
        else: s_type = "C"
        
        if explosion >= 1.3: e_type = "S"
        elif explosion >= 0.8: e_type = "M"
        else: e_type = "F"
        
        final_type = f"{s_type}-{e_type}"
        
        # 중복 방지를 위한 ID 생성
        import time
        new_id = str(time.time())
        
        new_entry = {
            "id": new_id, "찜": False, "대학": univ, "학과": dept,
            "지속지수": round(sustain, 3), "폭발지수": round(explosion, 3), "타입": final_type
        }
        st.session_state.history.append(new_entry)
        st.rerun()

# --- 3. 타겟 리스트 (오류 수정 및 기능 강화) ---
st.markdown("---")
st.subheader("📋 스나이핑 타겟 리스트")

# 은서 픽 9가지 HEX 색상
color_map = {
    "A-S": "#FDE1E1FF", "A-M": "#FEDCC4FF", "A-F": "#FDEDBAFF",
    "B-S": "#F5FDBAFF", "B-M": "#C3FDBAFF", "B-F": "#E0FBE2FF",
    "C-S": "#BAFAFDFF", "C-M": "#BACFFDFF", "C-F": "#C4BAFDFF"
}

if st.session_state.history:
