import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import platform
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 페이지 설정 (가장 먼저 실행되어야 함)
st.set_page_config(page_title="FIN SCOPE (Public)", page_icon="🏢", layout="wide")

# 2. 커스텀 CSS 적용 (글자색 흰색 현상 해결)
st.markdown("""
    <style>
    /* 전체 폰트 및 배경 설정 - 배경은 밝게, 기본 글자색은 어둡게 */
    .stApp {
        background-color: #f8f9fa;
        color: #2c3e50;
    }
    
    /* Streamlit 제목(h1, h2, h3, p 등) 글자색 강제 고정 */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #2c3e50 !important;
    }
    
    /* 사이드바 다크 테마 디자인 (사이드바 안의 글자는 예외로 흰색/밝은색 유지) */
    [data-testid="stSidebar"] {
        background-color: #1a252c !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .css-17lntkn {
        color: #ffffff !important;
        font-size: 16px;
    }
    .stRadio > div > label {
        padding: 10px;
        background-color: transparent;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stRadio > div > label:hover {
        background-color: #2c3e50;
    }
    
    /* 상단 KPI 메트릭 카드 스타일링 */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 메트릭 카드 안의 숫자와 레이블 색상 고정 */
    div[data-testid="metric-container"] > div {
        color: #2c3e50 !important; 
    }
    
    /* 표(Dataframe) 내부 글자색 고정 */
    [data-testid="stDataFrame"] div {
        color: #2c3e50 !important;
    }
    </style>
""", unsafe_allow_html=True)


# 3. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


# 4. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("public.csv")
    df['region_name'] = df['자치구'] + " " + df['행정동']
    df['older_pop'] = (df['인구수_명'] * (df['고령인구비율_%'] / 100)).astype(int)
    df['income'] = df['월평균가구소득_만원']
    df['current_facilities'] = df['노인복지시설수']
    return df

df = load_data()
ref_income = df['income'].median()

# 5. 사이드바 구성
with st.sidebar:
    st.markdown("<h2 style='color: #f1c40f !important;'>F | FIN SCOPE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #bdc3c7 !important;'>공공 데이터 시각화 웹</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<p style='color: #7f8c8d !important; font-size: 12px;'>WORKSPACE</p>", unsafe_allow_html=True)
    menu = st.radio(
        "", 
        ["📊 종합 대시보드", "⚖️ 민감도 및 순위 분석", "📁 데이터 & 사용 안내"]
    )
    
    st.markdown("---")
    st.markdown("<p style='color: #7f8c8d !important; font-size: 12px;'>● EDUCATION EDITION</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #bdc3c7 !important; font-size: 12px;'>관찰하고, 비교하고, <br>근거를 바탕으로 판단합니다.</p>", unsafe_allow_html=True)

# ==========================================
# [메뉴 1] 종합 대시보드
# ==========================================
if menu == "📊 종합 대시보드":
    st.markdown("<p style='color: #e67e22 !important; font-weight: bold;'>01 / PUBLIC OVERVIEW</p>", unsafe_allow_html=True)
    st.markdown("<h1>공공·사회 종합 대시보드</h1>", unsafe_allow_html=True)
    st.markdown("<p>전체 행정동의 노인 인구 규모와 현재 복지시설 공급 현황을 한눈에 살펴봅니다.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("분석 대상 지역", f"총 {len(df)}개 행정동")
    col2.metric("총 노인 인구", f"{df['older_pop'].sum():,} 명", "전체 합계")
    col3.metric("현재 노인복지시설", f"{df['current_facilities'].sum()} 개소", "공급 현황")
    col4.metric("월평균소득(중앙값)", f"{df['income'].median():.0f} 만원", "기준점")
    
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h4>🏙️ 인구 규모 상위 10개 행정동</h4>", unsafe_allow_html=True)
        top_pop = df.sort_values("older_pop", ascending=False).head(10)
        fig_pop = px.bar(top_pop, x="region_name", y="older_pop", text_auto=True, color="older_pop", color_continuous_scale="Blues")
        # 글자색 강제 지정(font_color) 추가
        fig_pop.update_layout(xaxis_title="", yaxis_title="노인 인구(명)", font_color="#2c3e50", coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        # theme=None을 추가하여 Streamlit의 강제 다크모드 무력화
        st.plotly_chart(fig_pop, use_container_width=True, theme=None)

    with c2:
        st.markdown("<h4>🏢 노인복지시설 밀도 하위 10개 동 (1만명당)</h4>", unsafe_allow_html=True)
        df['fac_per_10k'] = (df['current_facilities'] / df['older_pop']) * 10000
        bottom_fac = df.sort_values("fac_per_10k", ascending=True).head(10)
        fig_fac = px.bar(bottom_fac, x="region_name", y="fac_per_10k", text_auto='.2f', color="fac_per_10k", color_continuous_scale="Reds_r")
        fig_fac.update_layout(xaxis_title="", yaxis_title="1만명당 시설 수(개소)", font_color="#2c3e50", coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_fac, use_container_width=True, theme=None)

# ==========================================
# [메뉴 2] 민감도 및 순위 변동 분석
# ==========================================
elif menu == "⚖️ 민감도 및 순위 분석":
    st.markdown("<p style='color: #e67e22 !important; font-weight: bold;'>02 / SENSITIVITY ANALYSIS</p>", unsafe_allow_html=True)
    st.markdown("<h1>소득 보정 가중치에 따른 우선순위 변동</h1>", unsafe_allow_html=True)
    st.markdown("<p>단순 인구수가 아닌 <b>지역별 경제적 여력(월평균가구소득)</b>을 반영하는 가중치($\\alpha$)를 조절하여, 예산 배정의 시급성이 어떻게 변하는지 시뮬레이션합니다.</p>", unsafe_allow_html=True)
    
    with st.expander("🎛️ 시뮬레이션 파라미터 조절", expanded=True):
        c1, c2 = st.columns(2)
        alpha = c1.slider("소득 부족 보정 강도 (α)", 0.0, 1.0, 0.5, 0.05)
        T_std = c2.slider("시설 1개당 기준 노인수 (T)", 1000, 5000, 2000, 500)
    
    temp_df = df.copy()
    temp_df['income_gap_g'] = temp_df['income'].apply(lambda a: max(0.0, min(1.0, 1.0 - (a / ref_income))))
    temp_df['adjusted_demand_E'] = temp_df['older_pop'] * (1 + alpha * temp_df['income_gap_g'])
    temp_df['planned_facilities_N'] = np.ceil(temp_df['adjusted_demand_E'] / T_std)
    temp_df['shortage_S'] = temp_df['planned_facilities_N'] - temp_df['current_facilities']
    
    temp_df['rank_pop'] = temp_df['older_pop'].rank(ascending=False).astype(int)
    temp_df['rank_adjusted'] = temp_df['adjusted_demand_E'].rank(ascending=False).astype(int)
    temp_df['rank_change'] = temp_df['rank_pop'] - temp_df['rank_adjusted'] 

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<h4>📈 소득 보정 시 우선순위 급상승 TOP 10</h4>", unsafe_allow_html=True)
        top_changed = temp_df.sort_values("rank_change", ascending=False).head(10)
        fig_bar = px.bar(top_changed, x="rank_change", y="region_name", orientation='h', color="rank_change", color_continuous_scale="Teal")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="순위 상승 폭 (+)", yaxis_title="", font_color="#2c3e50", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True, theme=None)

    with c2:
        st.markdown("<h4>🔵 월평균소득 vs 보정된 복지 수요</h4>", unsafe_allow_html=True)
        fig_scatter = px.scatter(temp_df, x="income", y="adjusted_demand_E", size="older_pop", color="shortage_S", hover_name="region_name", color_continuous_scale="Sunsetdark", size_max=25)
        fig_scatter.update_layout(xaxis_title="월평균가구소득(만원)", yaxis_title="보정된 노인 수요(명 상당)", font_color="#2c3e50", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True, theme=None)

    st.markdown("<h4>📌 시뮬레이션 결과 데이터</h4>", unsafe_allow_html=True)
    display_df = temp_df[['region_name', 'older_pop', 'income', 'rank_pop', 'rank_adjusted', 'rank_change', 'shortage_S']].sort_values("rank_adjusted")
    display_df.columns = ["행정동명", "노인인구(명)", "월평균소득(만)", "기존순위", "보정후순위", "순위변동", "추가확충필요(개)"]
    st.dataframe(display_df, use_container_width=True)

# ==========================================
# [메뉴 3] 데이터 & 사용 안내
# ==========================================
elif menu == "📁 데이터 & 사용 안내":
    st.markdown("<p style='color: #e67e22 !important; font-weight: bold;'>03 / METHODOLOGY & DATA</p>", unsafe_allow_html=True)
    st.markdown("<h1>산정 근거 및 원천 데이터</h1>", unsafe_allow_html=True)
    st.info("본 대시보드는 제공된 `public.csv` 데이터를 기반으로 구성된 공공 복지시설 확충 모의 시뮬레이터입니다.")
    
    st.markdown("<h3>📊 분석 방법론</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color: #2c3e50;'>
    <ul>
        <li><b>인구 산출</b>: <code>인구수_명</code> × <code>고령인구비율_%</code> = <code>older_pop</code></li>
        <li><b>자산 기준</b>: 지역구별 <code>월평균가구소득</code> 중앙값을 기준 자산(Aref)으로 설정</li>
        <li><b>수요 보정</b>: 단순 인구 우선이 아닌 경제적 소외 계층을 감안한 가중합 적용</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 분석용 데이터셋 (CSV) 다운로드", data=csv, file_name="processed_public_data.csv", mime="text/csv")