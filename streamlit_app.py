import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="정시 9타입 분석기", layout="wide")

# 세션 상태 초기화 (기록 및 찜 기능)
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "찜", "대학", "학과", "23_인원", "24_인원", "25_인원", 
        "23_비율", "24_비율", "25_비율", "지속지수", "폭발지수", "타입"
    ])

st.title("🎯 정시 스나이핑 9타입 분석기")

# --- 1. 입력칸 (가로 배치 & 그룹화) ---
with st.expander("➕ 데이터 입력", expanded=True):
    col1, col2 = st.columns(2)
    univ = col1.text_input("대학 이름")
    dept = col2.text_input("학과명")

    st.markdown("---")
    # 인원수와 비율을 그룹화하여 배치
    row_count = st.columns(3)
    c23 = row_count[0].number_input("23 추합인원", step=1, value=0)
    c24 = row_count[1].number_input("24 추합인원", step=1, value=0)
    c25 = row_count[2].number_input("25 추합인원", step=1, value=0)

    row_rate = st.columns(3)
    r23 = row_rate[0].number_input("23 비율(%)", format="%.3f", value=0.0)
    r24 = row_rate[1].number_input("24 비율(%)", format="%.3f", value=0.0)
    r25 = row_rate[2].number_input("25 비율(%)", format="%.3f", value=0.0)

# --- 2. 계산 로직 (은서의 엑셀 함수 100% 반영) ---
if st.button("🚀 분석 및 기록 저장"):
    rates = [r23, r24, r25]
    
    # 엑셀 기준값들
    J_avg = np.mean(rates)           # 3년 평균 비율
    K_vol = np.max(rates) - np.min(rates) # 변동성
    L_min = np.min(rates)           # 3년 최소 추합비율
    M_median = np.median(rates)      # 중앙값
    
    # 지속펑크지수 (N6): L6*0.5 + M6*0.3 + J6*0.2
    sustain = (L_min * 0.5) + (M_median * 0.3) + (J_avg * 0.2)
    
    # 폭발펑크지수 (P6): MAX*0.6 + (MAX-M6)*0.25 + K6*0.15
    explosion = (np.max(rates) * 0.6) + ((np.max(rates) - M_median) * 0.25) + (K_vol * 0.15)
    
    # 타입 판정 로직
    # 지속타입 (A, B, C)
    if sustain >= 0.55 and L_min >= 0.4: s_type = "A"
    elif sustain >= 0.45 and L_min >= 0.25: s_type = "B"
    else: s_type = "C"
    
    # 폭발타입 (S, M, F)
    if explosion >= 1.3: e_type = "S"
    elif explosion >= 0.8: e_type = "M"
    else: e_type = "F"
    
    final_type = f"{s_type}-{e_type}"
    
    # 데이터프레임에 추가
    new_data = pd.DataFrame([{
        "찜": False, "대학": univ, "학과": dept,
        "23_인원": c23, "24_인원": c24, "25_인원": c25,
        "23_비율": r23, "24_비율": r24, "25_비율": r25,
        "지속지수": round(sustain, 3), "폭발지수": round(explosion, 3), "타입": final_type
    }])
    st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)

# --- 3. 타겟 리스트 (찜/삭제 기능 포함) ---
st.markdown("---")
st.subheader("📋 스나이핑 타겟 리스트")

if not st.session_state.history.empty:
    # 정렬: 찜(True가 위로) -> 타입(알파벳순)
    display_df = st.session_state.history.copy()
    display_df = display_df.sort_values(by=["찜", "타입"], ascending=[False, True])

    # 타입별 9가지 색상 지정 (추후 수정 가능)
    type_colors = {
        "A-S": "#FF4B4B", "A-M": "#FF8C00", "A-F": "#FFD700",
        "B-S": "#ADFF2F", "B-M": "#00FF7F", "B-F": "#00CED1",
        "C-S": "#1E90FF", "C-M": "#9370DB", "C-F": "#D3D3D3"
    }

    def style_rows(row):
        color = type_colors.get(row["타입"], "white")
        return [f'background-color: {color}; color: black' if i == len(row)-1 else '' for i in range(len(row))]

    # 데이터 편집기 (찜 기능 및 데이터 삭제용 체크박스 역할)
    edited_df = st.data_editor(
        display_df[["찜", "대학", "학과", "지속지수", "폭발지수", "타입"]],
        column_config={
            "찜": st.column_config.CheckboxColumn("⭐", default=False),
            "타입": st.column_config.TextColumn("타입 (A-S~C-F)")
        },
        disabled=["대학", "학과", "지속지수", "폭발지수", "타입"],
        use_container_width=True,
        hide_index=True,
        key="editor"
    )

    # 삭제 버튼 (선택한 행 삭제 기능 우회 구현)
    if st.button("🗑️ 선택 항목 기록에서 영구 삭제"):
        # editor에서 변경된 '찜' 상태를 반영하고 싶다면 추가 로직이 필요하지만, 
        # 일단은 가장 최근 입력 데이터 기반으로 삭제 기능을 위해 index를 활용하는 것이 좋음.
        st.warning("삭제 기능은 현재 체크박스 선택 후 리프레시 시 반영되도록 로직 구성이 필요합니다. (세션 기반)")

else:
    st.write("아직 분석된 데이터가 없습니다. 위에서 데이터를 입력해주세요.")
