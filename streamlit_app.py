import streamlit as st
import pandas as pd
import numpy as np
import uuid

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'Calculator'  # 기본 페이지
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 상단 네비게이션 버튼 (우측 정렬 느낌) ---
nav_col1, nav_col2, nav_col3 = st.columns([7, 1.5, 1.5])
with nav_col2:
    if st.button("🧮 Calculator", use_container_width=True):
        st.session_state.page = 'Calculator'
        st.rerun()
with nav_col3:
    if st.button("📜 Instrument", use_container_width=True):
        st.session_state.page = 'Instrument'
        st.rerun()

st.markdown("---")

# --- CASE 1: 설명서 페이지 (Instrument) ---
if st.session_state.page == 'Instrument':
    st.header("📜 스나이핑 지표 설명서 (Instrument)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. 지속펑크지수 (Sustainability)")
        st.write("**'이 학과의 펑크 토양이 얼마나 비옥하고 꾸준한가?'**를 측정합니다.")
        st.info("수식: (최소비율 * 0.5) + (중앙값 * 0.3) + (3년평균 * 0.2)")
        st.markdown("""
        - **A (High Vitality):** 3년 내내 추합이 안정적으로 발생하는 최상급 토양
        - **B (Potential):** 상황에 따라 전략적 접근이 필요한 중간 토양
        - **C (Low Priority):** 추합이 적어 선이 잘 붕괴되지 않는 딱딱한 토양
        """)

    with col_b:
        st.subheader("2. 폭발펑크지수 (Explosion)")
        st.write("**'한 번 터질 때 얼마나 미친 듯이 무너지는가?'**를 측정합니다.")
        st.warning("수식: (최대비율 * 0.6) + (최대-중앙 * 0.25) + (변동폭 * 0.15)")
        st.markdown("""
        - **S (Sniper Core):** 과거에 합격선이 완전히 무너진 경험이 있는 찐 타겟
        - **M (Maybe):** 조건이 맞으면 언제든 사고를 칠 잠재력이 있는 그룹
        - **F (Filter Out):** 변동성이 작아 대박을 기대하기 힘든 분석 제외 그룹
        """)

# --- CASE 2: 계산기 페이지 (Calculator) ---
else:
    st.header("🎯 정시 스나이핑 9타입 분석기")

    # 입력칸 (가로 그룹화)
    with st.expander("➕ 데이터 입력", expanded=True):
        c1, c2 = st.columns(2)
        univ = c1.text_input("대학 이름")
        dept = c2.text_input("학과명")

        st.markdown("**인원수 및 비율(%) 입력**")
        r_count = st.columns(3)
        c23 = r_count[0].number_input("23 추합인원", step=1, value=0)
        c24 = r_count[1].number_input("24 추합인원", step=1, value=0)
        c25 = r_count[2].number_input("25 추합인원", step=1, value=0)

        r_rate = st.columns(3)
        # 사용자는 %단위(예: 65.4)로 입력
        pr23 = r_rate[0].number_input("23 비율(%)", format="%.2f", value=0.0)
        pr24 = r_rate[1].number_input("24 비율(%)", format="%.2f", value=0.0)
        pr25 = r_rate[2].number_input("25 비율(%)", format="%.2f", value=0.0)

    if st.button("🚀 분석 및 기록 저장"):
        if univ and dept:
            # 계산 시에는 %를 소수점으로 변환 (65.4 -> 0.654)
            rates = [pr23/100, pr24/100, pr25/100]
            J_avg = np.mean(rates)
            K_vol = np.max(rates) - np.min(rates)
            L_min = np.min(rates)
            M_median = np.median(rates)
            
            # 은서 엑셀 수식
            sustain = (L_min * 0.5) + (M_median * 0.3) + (J_avg * 0.2)
            explosion = (np.max(rates) * 0.6) + ((np.max(rates) - M_median) * 0.25) + (K_vol * 0.15)
            
            # 타입 판정
            if sustain >= 0.55 and L_min >= 0.4: s_type = "A"
            elif sustain >= 0.45 and L_min >= 0.25: s_type = "B"
            else: s_type = "C"
            
            if explosion >= 1.3: e_type = "S"
            elif explosion >= 0.8: e_type = "M"
            else: e_type = "F"
            
            st.session_state.history.append({
                "id": str(uuid.uuid4()), "찜": False, "대학": univ, "학과": dept,
                "지속": round(sustain, 3), "폭발": round(explosion, 3), "타입": f"{s_type}-{e_type}"
            })
            st.rerun()

    # 결과 리스트
    st.subheader("📋 스나이핑 타겟 리스트")
    color_map = {
        "A-S": "#FDE1E1FF", "A-M": "#FEDCC4FF", "A-F": "#FDEDBAFF",
        "B-S": "#F5FDBAFF", "B-M": "#C3FDBAFF", "B-F": "#E0FBE2FF",
        "C-S": "#BAFAFDFF", "C-M": "#BACFFDFF", "C-F": "#C4BAFDFF"
    }

    if st.session_state.history:
        sorted_h = sorted(st.session_state.history, key=lambda x: (not x['찜'], x['타입']))
        for entry in sorted_h:
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
