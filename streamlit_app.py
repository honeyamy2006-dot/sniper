import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="정시 9타입 스나이퍼", layout="wide")

# 세션 기록 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎯 정시 스나이핑 9타입 분석기 (인원수 보정 버전)")

# 1. 입력칸 (가로 배치 + 추합 인원 추가)
with st.container():
    # 대학/학과 정보
    row1 = st.columns([2, 2])
    univ = row1[0].text_input("대학 이름", placeholder="ex) 중앙대")
    dept = row1[1].text_input("학과명", placeholder="ex) 심리")
    
    # 3개년 추합 인원 및 비율 입력 (가로로 6칸)
    st.markdown("**3개년 데이터 입력 (인원 및 비율)**")
    row2 = st.columns(6)
    c23 = row2[0].number_input("23 추합인원", step=1)
    r23 = row2[1].number_input("23 비율(%)", format="%.2f")
    c24 = row2[2].number_input("24 추합인원", step=1)
    r24 = row2[3].number_input("24 비율(%)", format="%.2f")
    c25 = row2[4].number_input("25 추합인원", step=1)
    r25 = row2[5].number_input("25 비율(%)", format="%.2f")

if st.button("🚀 9타입 분석 실행"):
    # 리스트화
    counts = [c23, c24, c25]
    rates = [r23 / 100 if r23 > 1 else r23, r24 / 100 if r24 > 1 else r24, r25 / 100 if r25 > 1 else r25]
    
    # --- 은서의 엑셀 로직 반영 ---
    
    # 1. 지속펑크지수 (Sustain)
    # 인원수 가중치: 인원이 많을수록 토양이 비옥하다고 판단 (A타입 유도)
    avg_rate = np.mean(rates)
    avg_count = np.mean(counts)
    vol = np.std(rates) / avg_rate if avg_rate != 0 else 0
    
    # 인원수 규모에 따른 보정 계수 (중앙대 심리 등 대형과 보정용)
    count_weight = 1.2 if avg_count >= 10 else 1.0 # 인원 10명 이상 시 토양 비옥도 가중
    
    sustain = avg_rate * (1 - vol) * count_weight
    
    # 2. 폭발펑크지수 (Explosion)
    max_rate = np.max(rates)
    median_rate = np.median(rates)
    # 은서 수식: (최대*0.6) + (최대-중앙*0.25) + (변동폭*0.15)
    vol_range = max_rate - np.min(rates)
    explosion = (max_rate * 0.6) + ((max_rate - median_rate) * 0.25) + (vol_range * 0.15)
    
    # --- 타입 판정 (필기 기준) ---
    # 지속: A(0.8↑), B(0.4~0.7), C(0.4↓)
    if sustain >= 0.8: s_type = "A"
    elif sustain >= 0.4: s_type = "B"
    else: s_type = "C"
    
    # 폭발: S(1.3↑), M(0.8~1.3), F(0.8↓)
    if explosion >= 1.3: e_type = "S"
    elif explosion >= 0.8: e_type = "M"
    else: e_type = "F"
    
    final_type = f"{s_type}-{e_type}"
    
    # 기록 저장
    st.session_state.history.append({
        "대학": univ, "학과": dept, "평균비율": f"{avg_rate:.3f}", "평균인원": f"{avg_count:.1f}",
        "지속지수": f"{sustain:.3f}", "폭발지수": f"{explosion:.3f}", "타입": final_type
    })

# 3. 결과 대시보드 (타입 강조)
if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 스나이핑 타겟 리스트")
    
    # 최신 결과 강조 카드
    latest = st.session_state.history[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("최종 타입", latest["타입"])
    c2.metric("지속펑크지수", latest["지속지수"])
    c3.metric("폭발펑크지수", latest["폭발지수"])
    
    # 전체 테이블 스타일링
    df = pd.DataFrame(st.session_state.history)
    
    def highlight_type(val):
        if val == 'A-S': return 'background-color: #FF4B4B; color: white; font-weight: bold'
        if val in ['B-S', 'A-M']: return 'background-color: #FFA500; color: white'
        if 'F' in val or 'C' in val: return 'background-color: #f0f0f0; color: #999'
        return ''

    st.table(df.style.applymap(highlight_type, subset=['타입']))
