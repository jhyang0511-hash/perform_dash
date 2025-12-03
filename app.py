import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 페이지 설정
st.set_page_config(layout="wide", page_title="Simple Exhibition ROI", page_icon="💰")

# 제목
st.title("💰 전시 참가 ROI 시뮬레이터")
st.markdown("복잡한 엑셀 없이, **예상 비용과 성과**를 입력하여 투자 가치를 즉시 확인하세요.")

# --- 사이드바: 입력 패널 ---
st.sidebar.header("1. 비용 입력 (Cost)")
cost_booth = st.sidebar.number_input("부스 임차료 및 시공비 (만원)", value=500, step=50)
cost_staff = st.sidebar.number_input("인건비 및 체류비 (만원)", value=200, step=10)
cost_marketing = st.sidebar.number_input("마케팅 및 판촉물 (만원)", value=100, step=10)
cost_etc = st.sidebar.number_input("기타 예비비 (만원)", value=50, step=10)

st.sidebar.markdown("---")
st.sidebar.header("2. 예상 성과 입력 (Performance)")
leads_count = st.sidebar.slider("획득 명함(Lead) 수 (개)", 0, 1000, 200)
conversion_rate = st.sidebar.slider("상담 → 계약 전환율 (%)", 1.0, 50.0, 5.0, step=0.5)
deal_value = st.sidebar.number_input("계약 건당 평균 매출 (만원)", value=300, step=100)

# --- 계산 로직 ---
total_cost = cost_booth + cost_staff + cost_marketing + cost_etc
expected_deals = int(leads_count * (conversion_rate / 100))
expected_revenue = expected_deals * deal_value
profit = expected_revenue - total_cost

# ROI 계산 (분모가 0일 경우 방지)
if total_cost > 0:
    roi_percentage = (profit / total_cost) * 100
else:
    roi_percentage = 0

cost_per_lead = total_cost / leads_count if leads_count > 0 else 0

# --- 메인 대시보드 화면 ---

# 1. 핵심 지표 (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 지출 (Cost)", f"{total_cost:,.0f} 만원", delta_color="inverse")
col2.metric("예상 매출 (Revenue)", f"{expected_revenue:,.0f} 만원")
col3.metric("순수익 (Profit)", f"{profit:,.0f} 만원", delta=f"{roi_percentage:.1f}% ROI")
col4.metric("리드 당 비용 (CPL)", f"{cost_per_lead:,.0f} 만원")

st.markdown("---")

# 2. 시각화 (Plotly)
chart_col1, chart_col2 = st.columns([1, 1])

with chart_col1:
    st.subheader("📊 비용 vs 매출 비교")
    # 단순 막대 그래프
    fig_bar = go.Figure(data=[
        go.Bar(name='총 비용', x=['금액'], y=[total_cost], marker_color='#FF6B6B'),
        go.Bar(name='예상 매출', x=['금액'], y=[expected_revenue], marker_color='#4ECDC4')
    ])
    fig_bar.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("🚀 ROI 달성률 (손익분기점)")
    # 게이지 차트 (손익분기점 시각화)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = roi_percentage,
        title = {'text': "투자 수익률 (ROI %)"},
        delta = {'reference': 0}, # 0%가 본전
        gauge = {
            'axis': {'range': [-100, 300]}, # -100% ~ 300% 범위
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [-100, 0], 'color': "lightgray"},
                {'range': [0, 300], 'color': "lightgreen"}],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}
        }
    ))
    fig_gauge.update_layout(height=400)
    st.plotly_chart(fig_gauge, use_container_width=True)

# 3. 데이터 요약 및 다운로드
st.markdown("### 📝 시뮬레이션 결과 요약")
result_data = {
    "구분": ["부스비", "인건비", "마케팅비", "기타", "총 비용", "획득 명함", "전환율", "예상 계약수", "예상 매출", "ROI"],
    "값": [cost_booth, cost_staff, cost_marketing, cost_etc, total_cost, leads_count, f"{conversion_rate}%", expected_deals, expected_revenue, f"{roi_percentage:.1f}%"]
}
df = pd.DataFrame(result_data)

# 테이블 표시
st.dataframe(df.set_index("구분").T, use_container_width=True)

# 다운로드 버튼
csv = df.to_csv().encode('utf-8')
st.download_button(
    label="📥 보고서 데이터 다운로드 (CSV)",
    data=csv,
    file_name='exhibition_roi_simulation.csv',
    mime='text/csv',
)
