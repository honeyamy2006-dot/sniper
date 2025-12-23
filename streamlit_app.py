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
    if st.button("🧮 스나후보계산기", use_container_width=True):
        st.session_state.page = 'Calculator'
        st.rerun()
with nav_col3:
    if st.button("📜 설명서", use_container_width=True):
        st.session_state.page = 'Instrument'
        st.rerun()

st.markdown("---")

# --- CASE 1: 설명서 페이지 (Instrument) ---
if st.session_state.page == 'Instrument':
    st.header("📜 스나이핑 지표 설명서 (Instrument)")
    
   def show_manual():
    st.header("📘 서비스 이용 가이드")
    
    # 9타입 매트릭스 시각화 (HTML/CSS 사용)
    st.subheader("1. 9타입 매트릭스 판정표")
    
    matrix_html = """
    <style>
        .matrix-table { width: 100%; text-align: center; border-collapse: collapse; font-family: sans-serif; }
        .matrix-table td { border: 1px solid #ddd; padding: 10px; width: 25%; }
        .header-y { background-color: #f8f9fa; font-weight: bold; }
        .header-x { background-color: #f8f9fa; font-weight: bold; }
        .s-core { background-color: #ff4b4b; color: white; font-weight: bold; }
        .maybe { background-color: #ffa500; color: white; }
        .filter { background-color: #f1f1f1; color: #888; }
    </style>
    <table class="matrix-table">
        <tr>
            <td class="header-y">토양 \ 사건</td>
            <td class="header-x">S (Sniper Core)</td>
            <td class="header-x">M (Maybe)</td>
            <td class="header-x">F (Filter Out)</td>
        </tr>
        <tr>
            <td class="header-y">A (High Vitality)</td>
            <td class="s-core">A-S (최우수)</td>
            <td class="maybe">A-M (주력)</td>
            <td class="filter">A-F (안정)</td>
        </tr>
        <tr>
            <td class="header-y">B (Potential)</td>
            <td class="maybe">B-S (전략)</td>
            <td class="maybe">B-M (참고)</td>
            <td class="filter">B-F (하위)</td>
        </tr>
        <tr>
            <td class="header-y">C (Low Priority)</td>
            <td class="filter">C-S (로또)</td>
            <td class="filter">C-M (희박)</td>
            <td class="filter">C-F (제외)</td>
        </tr>
    </table>
    """
    st.markdown(matrix_html, unsafe_allow_html=True)

    # 지표 상세 설명
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**지속펑크지수 (Consistency)**")
        st.write("""
        - **철학**: 꾸준히 잘 빠지는 '비옥한 토양'인가?
        - **산식**: $Average_{3y} \\times (1 - Volatility)$
        - **A(0.8↑)**: 최상급 토양. 3년 내내 안정적 유출.
        - **C(0.4↓)**: 딱딱한 토양. 붕괴 가능성 낮음.
        """)
        
    with col2:
        st.warning("**폭발펑크지수 (Explosion)**")
        st.write("""
        - **철학**: 입결이 완전히 무너진 '이상치'가 있는가?
        - **산식**: $Max(60\%) + Gap(25\%) + Range(15\%)$
        - **S(1.3↑)**: 찐 스나 타겟. 보상 확실.
        - **F(0.8↓)**: 변동성 작음. 분석 제외.
        """)

# 사이드바 메뉴나 탭으로 구성
menu = st.sidebar.selectbox("메뉴", ["분석기", "설명서"])
if menu == "설명서":
    show_manual()



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
