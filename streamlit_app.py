import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="Sniping Dashboard", layout="wide")

# 2. 데이터 정렬 우선순위 정의 (A-S ~ C-F)
TYPE_ORDER = [
    "A-S", "A-M", "A-F", 
    "B-S", "B-M", "B-F", 
    "C-S", "C-M", "C-F"
]

# 샘플 데이터 생성 (기존 데이터 로드 로직이 있다면 그 부분을 사용하면 돼)
def load_data():
    # 실제 환경에서는 pd.read_csv() 등을 사용하겠지만, 
    # 구조 확인을 위해 너가 말한 지표들로 예시를 만들었어.
    data = {
        "학과명": ["정치외교", "경영학", "철학", "경제학", "사회학"],
        "타입": ["A-M", "A-S", "C-F", "B-S", "B-M"],
        "지속펑크지수": [0.85, 0.92, 0.25, 0.55, 0.48],
        "폭발펑크지수": [1.1, 1.4, 0.5, 1.35, 0.9]
    }
    return pd.DataFrame(data)

df = load_data()

# 사이드바 메뉴
menu = st.sidebar.selectbox("메뉴 선택", ["스나이핑 타겟 리스트", "시스템 설명서"])

# --- [페이지 1: 리스트] ---
if menu == "스나이핑 타겟 리스트":
    st.title("🎯 스나이핑 타겟 분석 리스트")
    
    # 정렬 버튼
    if st.button("🔥 타입별 최적 정렬 (A-S ➔ C-F)"):
        df['타입'] = pd.Categorical(df['타입'], categories=TYPE_ORDER, ordered=True)
        df = df.sort_values('타입').reset_index(drop=True)
        st.success("우선순위에 따라 정렬되었습니다.")

    st.dataframe(df, use_container_width=True)

# --- [페이지 2: 설명서] ---
elif menu == "시스템 설명서":
    st.title("📘 스나이핑 시스템 매뉴얼")
    
    # 9타입 매트릭스 시각화
    st.subheader("1. 9타입 매트릭스 판정표")
    
    matrix_html = """
    <style>
        .m-table { width: 100%; border-collapse: collapse; text-align: center; font-family: sans-serif; }
        .m-table td { border: 1px solid #444; padding: 15px; }
        .label-y { background-color: #f0f2f6; font-weight: bold; width: 150px; }
        .label-x { background-color: #f0f2f6; font-weight: bold; }
        .s-core { background-color: #ff4b4b; color: white; font-weight: bold; } /* Sniper Core */
        .maybe { background-color: #ffa500; color: white; } /* Maybe */
        .filter { background-color: #e0e0e0; color: #888; } /* Filter Out */
    </style>
    <table class="m-table">
        <tr class="label-x">
            <td>토양 \ 잠재력</td>
            <td>S (Sniper Core)</td>
            <td>M (Maybe)</td>
            <td>F (Filter Out)</td>
        </tr>
        <tr>
            <td class="label-y">A (High Vitality)</td>
            <td class="s-core">A-S (최상급)</td>
            <td class="maybe">A-M (주력)</td>
            <td class="filter">A-F (안정)</td>
        </tr>
        <tr>
            <td class="label-y">B (Potential)</td>
            <td class="maybe">B-S (전략)</td>
            <td class="maybe">B-M (관찰)</td>
            <td class="filter">B-F (하위)</td>
        </tr>
        <tr>
            <td class="label-y">C (Low Priority)</td>
            <td class="filter">C-S (로또)</td>
            <td class="filter">C-M (희박)</td>
            <td class="filter">C-F (제외)</td>
        </tr>
    </table>
    """
    st.markdown(matrix_html, unsafe_allow_html=True)
    st.caption("※ A-S부터 순서대로 스나이핑 확률이 높음을 의미합니다.")

    # 지표 상세 설명
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🪵 지속펑크지수 (토양)")
        st.write("**정의:** 얼마나 신뢰할 수 있는 구멍인가?")
        st.latex(r"I_c = \text{Avg}_{3y} \times (1 - \text{Volatility})")
        st.markdown("""
        - **A (0.8↑):** 최상급 토양. 3년 내내 안정적으로 인원 유출.
        - **B (0.4~0.7):** 중간 토양. 전략적 접근 필요.
        - **C (0.4↓):** 딱딱한 토양. 웬만해서는 붕괴되지 않음.
        
        **철학:** 단순히 평균이 높은 것보다 변동성이 낮아야(꾸준히 빠져야) 진정한 '구멍'으로 인정합니다.
        """)

    with col2:
        st.markdown("### 💥 폭발펑크지수 (잠재력)")
        st.write("**정의:** 이상치가 터질 가능성이 있는가?")
        st.markdown("""
        - **S (1.3↑):** 과거 합격선 붕괴 경험 실재. 보상 확실.
        - **M (0.8~1.3):** 잠재력 증명. 정치, 경제 등 주요 학과 포진.
        - **F (0.8↓):** 변동성 낮음. 분석 가치 없음.
        
        **가중치 산정 기준:**
        1. 최근 3개년 최댓값 (60%)
        2. 최댓값 - 중앙값 (25%)
        3. 연도별 변동폭 (15%)
        """)

    st.success("💡 Tip: 'A-S'는 비옥한 토양에 폭발력까지 갖춘 최고의 스나이핑 타겟입니다.")
