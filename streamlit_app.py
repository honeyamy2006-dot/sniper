import streamlit as st
import pandas as pd
import numpy as np
import uuid

# 1. 페이지 설정
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기")

# --- 2. 입력칸 (그룹화 유지) ---
with st.expander("➕ 데이터 입력", expanded=True):
    col1, col2 = st.columns(2)
    univ = col1.text_input("대학 이름", key="univ_in")
    dept = col2.text_input("학과명", key="dept_in")

    st.markdown("---")
    r_count = st.columns(3)
    c23 = r_count[0].number_input("23 추합인원", step=1, value=0)
    c24 = r_count[1].number_input("24 추합인원", step=1, value=0)
    c25 = r_count[2].number_input("25 추합인원", step=1, value=0)

    r_rate = st.columns(3)
    r23 = r_rate[0].number_input("23 비율(단위:0.xxx)", format="%.3f", value=0.0)
    r24 = r_rate[1].number_input("24 비율(단위:0.xxx)", format="%.3f", value=0.0)
    r25 = r_rate[2].number_input("25 비율(단위:0.xxx)", format="%.3f", value=0.0)

# --- 3. 엑셀 함수 100% 이식 로직 ---
if st.button("🚀 분석 및 기록 저장"):
    if univ and dept:
        rates = [r23, r24, r25]
        J_avg = np.mean(rates)
        K_vol = np.max(rates) - np.min(rates) # 변동성: MAX-MIN (수정됨)
        L_min = np.min(rates)
        M_median = np.median(rates)
        
        # 지속펑크지수(N) & 폭발펑크지수(P)
        sustain = (L_min * 0.5) + (M_median * 0.3) + (J_avg * 0.2)
        explosion = (np.max(rates) * 0.6) + ((np.max(rates) - M_median) * 0.25) + (K_vol * 0.15)
        
        # 타입 판정 (은서 엑셀 조건식)
        if sustain >= 0.55 and L_min >= 0.4: s_type = "A"
        elif sustain >= 0.45 and L_min >= 0.25: s_type = "B"
        else: s_type = "C"
        
        if explosion >= 1.3: e_type = "S"
        elif explosion >= 0.8: e_type = "M"
        else: e_type = "F"
        
        # 데이터 저장
        st.session_state.history.append({
            "id": str(uuid.uuid4()), "찜": False, "대학": univ, "학과": dept,
            "지속": round(sustain, 3), "폭발": round(explosion, 3), "타입": f"{s_type}-{e_type}"
        })
        st.rerun()

# --- 4. 타겟 리스트 (색상/찜/즉시삭제) ---
st.markdown("---")
st.subheader("📋 스나이핑 타겟 리스트")

color_map = {
    "A-S": "#FDE1E1FF", "A-M": "#FEDCC4FF", "A-F": "#FDEDBAFF",
    "B-S": "#F5FDBAFF", "B-M": "#C3FDBAFF", "B-F": "#E0FBE2FF",
    "C-S": "#BAFAFDFF", "C-M": "#BACFFDFF", "C-F": "#C4BAFDFF"
}

if st.session_state.history:
    sorted_history = sorted(st.session_state.history, key=lambda x: (not x['찜'], x['타입']))
    h_cols = st.columns([0.6, 2, 2, 1.2, 1.2, 1.5, 0.6])
    h_cols[0].write("**찜**"); h_cols[1].write("**대학**"); h_cols[2].write("**학과**")
    h_cols[3].write("**지속**"); h_cols[4].write("**폭발**"); h_cols[5].write("**타입**"); h_cols[6].write("**삭제**")

    for entry in sorted_history:
        bg = color_map.get(entry['타입'], "#FFFFFF")
        with st.container():
            cols = st.columns([0.6, 2, 2, 1.2, 1.2, 1.5, 0.6])
            if cols[0].button("⭐" if entry['찜'] else "☆", key=f"p_{entry['id']}"):
                entry['찜'] = not entry['찜']; st.rerun()
            cols[1].write(entry['대학']); cols[2].write(entry['학과'])
            cols[3].write(str(entry['지속'])); cols[4].write(str(entry['폭발']))
            cols[5].markdown(f"<div style='background-color:{bg};border-radius:5px;padding:5px;text-align:center;color:black;font-weight:bold;'>{entry['타입']}</div>", unsafe_allow_html=True)
            if cols[6].button("🗑️", key=f"d_{entry['id']}"):
                st.session_state.history = [e for e in st.session_state.history if e['id'] != entry['id']]; st.rerun()
