import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

# 세션 상태 초기화 (데이터 저장소)
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기")

# --- 1. 입력칸 (은서 픽 가로 그룹화 유지) ---
with st.expander("➕ 데이터 입력", expanded=True):
    col1, col2 = st.columns(2)
    univ = col1.text_input("대학 이름")
    dept = col2.text_input("학과명")

    st.markdown("---")
    st.markdown("**인원수 입력**")
    row_count = st.columns(3)
    c23 = row_count[0].number_input("23 추합인원", step=1, key="c23")
    c24 = row_count[1].number_input("24 추합인원", step=1, key="c24")
    c25 = row_count[2].number_input("25 추합인원", step=1, key="c25")

    st.markdown("**비율(%) 입력**")
    row_rate = st.columns(3)
    r23 = row_rate[0].number_input("23 비율(%)", format="%.3f", key="r23")
    r24 = row_rate[1].number_input("24 비율(%)", format="%.3f", key="r24")
    r25 = row_rate[2].number_input("25 비율(%)", format="%.3f", key="r25")

# --- 2. 계산 로직 (은서의 엑셀 함수 100% 유지) ---
if st.button("🚀 분석 및 기록 저장"):
    if univ and dept:
        rates = [r23, r24, r25]
        J_avg = np.mean(rates)
        K_vol = np.max(rates) - np.min(rates)
        L_min = np.min(rates)
        M_median = np.median(rates)
        
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
        
        # 새로운 기록 추가 (id값 부여로 삭제/찜 관리)
        new_entry = {
            "id": len(st.session_state.history),
            "찜": False, "대학": univ, "학과": dept,
            "지속지수": round(sustain, 3), "폭발지수": round(explosion, 3), "타입": final_type
        }
        st.session_state.history.append(new_entry)
        st.rerun()

# --- 3. 타겟 리스트 (색상/찜/삭제 기능 커스텀) ---
st.markdown("---")
st.subheader("📋 스나이핑 타겟 리스트")

# 9가지 타입별 HEX 색상 사전
color_map = {
    "A-S": "#FDE1E1FF", "A-M": "#FEDCC4FF", "A-F": "#FDEDBAFF",
    "B-S": "#F5FDBAFF", "B-M": "#C3FDBAFF", "B-F": "#E0FBE2FF", # B-F 임시
    "C-S": "#BAFAFDFF", "C-M": "#BACFFDFF", "C-F": "#C4BAFDFF"
}

if st.session_state.history:
    # 찜한 것 위로, 그 다음 타입순 정렬
    sorted_history = sorted(st.session_state.history, key=lambda x: (not x['찜'], x['타입']))

    # 헤더
    h_cols = st.columns([0.5, 2, 2, 1.5, 1.5, 2, 0.5])
    h_cols[0].write("**찜**")
    h_cols[1].write("**대학**")
    h_cols[2].write("**학과**")
    h_cols[3].write("**지속지수**")
    h_cols[4].write("**폭발지수**")
    h_cols[5].write("**타입**")
    h_cols[6].write("**삭제**")

    # 리스트 렌더링
    for i, entry in enumerate(sorted_history):
        bg_color = color_map.get(entry['타입'], "#FFFFFF")
        
        # 한 줄 컨테이너 및 스타일링
        with st.container():
            cols = st.columns([0.5, 2, 2, 1.5, 1.5, 2, 0.5])
            
            # 찜 버튼 (⭐)
            star = "⭐" if entry['찜'] else "☆"
            if cols[0].button(star, key=f"star_{entry['id']}"):
                entry['찜'] = not entry['찜']
                st.rerun()
            
            # 텍스트 정보
            cols[1].write(entry['대학'])
            cols[2].write(entry['학과'])
            cols[3].write(str(entry['지속지수']))
            cols[4].write(str(entry['폭발지수']))
            
            # 타입 칸 (은서가 준 색상 적용)
            cols[5].markdown(f"""
                <div style="background-color:{bg_color}; border-radius:5px; padding:5px; text-align:center; color:black; font-weight:bold;">
                    {entry['타입']}
                </div>
                """, unsafe_allow_width=True, unsafe_allow_html=True)
            
            # 삭제 버튼 (🗑️)
            if cols[6].button("🗑️", key=f"del_{entry['id']}"):
                st.session_state.history = [e for e in st.session_state.history if e['id'] != entry['id']]
                st.rerun()
else:
    st.info("데이터를 입력하고 '분석 실행' 버튼을 눌러주세요.")
