import streamlit as st
import pandas as pd
import numpy as np
import uuid

# 1. 페이지 설정
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

# 세션 상태 초기화 (데이터 저장소)
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기")

# --- 2. 입력칸 (가로 그룹화 및 가독성 개선) ---
with st.expander("➕ 데이터 입력 (대학/학과 및 3개년 수치)", expanded=True):
    col1, col2 = st.columns(2)
    univ = col1.text_input("대학 이름", key="univ_input")
    dept = col2.text_input("학과명", key="dept_input")

    st.markdown("---")
    st.markdown("**인원수 입력**")
    row_count = st.columns(3)
    c23 = row_count[0].number_input("23 추합인원", step=1, value=0, key="c23")
    c24 = row_count[1].number_input("24 추합인원", step=1, value=0, key="c24")
    c25 = row_count[2].number_input("25 추합인원", step=1, value=0, key="c25")

    st.markdown("**비율(%) 입력**")
    row_rate = st.columns(3)
    r23 = row_rate[0].number_input("23 비율(%)", format="%.3f", value=0.0, key="r23")
    r24 = row_rate[1].number_input("24 비율(%)", format="%.3f", value=0.0, key="r24")
    r25 = row_rate[2].number_input("25 비율(%)", format="%.3f", value=0.0, key="r25")

# --- 3. 계산 로직 (은서의 엑셀 함수 100% 반영) ---
if st.button("🚀 분석 및 기록 저장"):
    if univ and dept:
        rates = [r23, r24, r25]
        j_avg = np.mean(rates)
        k_vol = np.max(rates) - np.min(rates)
        l_min = np.min(rates)
        m_median = np.median(rates)
        
        # 은서 전용 지수 수식
        sustain = (l_min * 0.5) + (m_median * 0.3) + (j_avg * 0.2)
        explosion = (np.max(rates) * 0.6) + ((np.max(rates) - m_median) * 0.25) + (k_vol * 0.15)
        
        # 타입 판정 로직
        if sustain >= 0.55 and l_min >= 0.4: s_type = "A"
        elif sustain >= 0.45 and l_min >= 0.25: s_type = "B"
        else: s_type = "C"
        
        if explosion >= 1.3: e_type = "S"
        elif explosion >= 0.8: e_type = "M"
        else: e_type = "F"
        
        final_type = f"{s_type}-{e_type}"
        
        # 기록 추가 (고유 ID 부여)
        st.session_state.history.append({
            "id": str(uuid.uuid4()), "찜": False, "대학": univ, "학과": dept,
            "지속지수": round(sustain, 3), "폭발지수": round(explosion, 3), "타입": final_type
        })
        st.rerun()

# --- 4. 타겟 리스트 (찜/삭제 기능 및 색상 반영) ---
st.markdown("---")
st.subheader("📋 스나이핑 타겟 리스트")

# 은서가 준 9가지 HEX 색상
color_map = {
    "A-S": "#FDE1E1", "A-M": "#FEDCC4", "A-F": "#FDEDBA",
    "B-S": "#F5FDBA", "B-M": "#C3FDBA", "B-F": "#E0FBE2",
    "C-S": "#BAFAFD", "C-M": "#BACFFD", "C-F": "#C4BAFD"
}

if st.session_state.history:
    # 찜(True) 우선 정렬 후 타입순 정렬
    sorted_history = sorted(st.session_state.history, key=lambda x: (not x['찜'], x['타입']))

    # 리스트 헤더
    h_cols = st.columns([0.6, 2, 2, 1.2, 1.2, 1.5, 0.6])
    h_cols[0].write("**찜**")
    h_cols[1].write("**대학**")
    h_cols[2].write("**학과**")
    h_cols[3].write("**지속**")
    h_cols[4].write("**폭발**")
    h_cols[5].write("**타입**")
    h_cols[6].write("**삭제**")

    # 리스트 렌더링
    for entry in sorted_history:
        bg_color = color_map.get(entry['타입'], "#FFFFFF")
        
        with st.container():
            cols = st.columns([0.6, 2, 2, 1.2, 1.2, 1.5, 0.6])
            
            # 찜 기능 (⭐ 노란색 채우기)
            star_icon = "⭐" if entry['찜'] else "☆"
            if cols[0].button(star_icon, key=f"pin_{entry['id']}"):
                entry['찜'] = not entry['찜']
                st.rerun()
            
            cols[1].write(entry['대학'])
            cols[2].write(entry['학과'])
            cols[3].write(str(entry['지속지수']))
            cols[4].write(str(entry['폭발지수']))
            
            # 타입 칸 (은서 픽 색상 적용)
            cols[5].markdown(f"""
                <div style="background-color:{bg_color}; border-radius:5px; padding:5px; 
                text-align:center; color:black; font-weight:bold; border: 1px solid #eee; font-size: 0.9em;">
                    {entry['타입']}
                </div>
                """, unsafe_allow_html=True)
            
            # 삭제 기능 (즉시 삭제)
            if cols[6].button("🗑️", key=f"del_{entry['id']}"):
                st.session_state.history = [e for e in st.session_state.history if e['id'] != entry['id']]
                st.rerun()
else:
    st.info("입력창에 데이터를 넣고 분석을 시작하세요.")
