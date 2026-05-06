import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Climate Dashboard",
    layout="wide"
)

st.title("🌍 Global Climate Indicators Dashboard")
st.markdown("Interactive analysis of CO₂ emissions and temperature anomalies")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    co2 = pd.read_csv("co2-emissions-per-capita.csv")
    co2 = co2[['Entity', 'Year', 'CO₂ emissions per capita']].dropna()
    co2['CO2'] = co2['CO₂ emissions per capita'].astype(float)
    co2_yearly = co2.groupby('Year')['CO2'].mean().reset_index()

    temp = pd.read_csv("NH.Ts+dSST.csv", skiprows=1)
    temp.columns = temp.columns.str.strip()
    temp = temp[['Year', 'J-D']]
    temp.columns = ['Year', 'Temp_Anomaly']
    temp = temp[temp['Temp_Anomaly'] != '***']
    temp['Temp_Anomaly'] = temp['Temp_Anomaly'].astype(float)

    df = pd.merge(temp, co2_yearly, on='Year')
    df = df.sort_values("Year")

    # Rolling averages (5-year)
    df["Temp_Roll"] = df["Temp_Anomaly"].rolling(window=5).mean()
    df["CO2_Roll"] = df["CO2"].rolling(window=5).mean()

    return df

df = load_data()

# -----------------------
# Sidebar Controls
# -----------------------
st.sidebar.header("Controls")

view = st.sidebar.selectbox(
    "Select Time Range",
    ["1880–Present", "1880–1949", "1950–1999", "2000–Present"]
)

mode = st.sidebar.radio(
    "Data Mode",
    ["Raw Data", "Smoothed Trend (5-year avg)"]
)

use_smoothed = (mode == "Smoothed Trend (5-year avg)")

# -----------------------
# Filter Data
# -----------------------
if view == "1880–Present":
    filtered = df
    color = "white"

elif view == "1880–1949":
    filtered = df[(df['Year'] >= 1880) & (df['Year'] <= 1949)]
    color = "blue"

elif view == "1950–1999":
    filtered = df[(df['Year'] >= 1950) & (df['Year'] <= 1999)]
    color = "orange"

else:
    filtered = df[df['Year'] >= 2000]
    color = "red"

st.subheader(f"📅 Viewing: {view}")

# Optional description for full dataset
if view == "1880–Present":
    st.caption("Full dataset view shows the long-term relationship between CO₂ and temperature.")

# Choose columns based on mode
temp_col = "Temp_Roll" if use_smoothed else "Temp_Anomaly"
co2_col = "CO2_Roll" if use_smoothed else "CO2"

st.markdown("---")

# -----------------------
# Tabs
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trends",
    "🔗 Relationship",
    "📊 Dual Axis",
    "📉 Industrialization Comparison"
])

# -----------------------
# 📈 Trends
# -----------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            filtered,
            x="Year",
            y=temp_col,
            title="Temperature Over Time",
            template="plotly_dark"
        )
        fig1.update_traces(line=dict(color=color))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            filtered,
            x="Year",
            y=co2_col,
            title="CO₂ Over Time",
            template="plotly_dark"
        )
        fig2.update_traces(line=dict(color=color))
        st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# 🔗 Relationship
# -----------------------
with tab2:
    fig3 = px.scatter(
        filtered,
        x=co2_col,
        y=temp_col,
        trendline="ols",
        color="Year",
        title="CO₂ vs Temperature",
        template="plotly_dark"
    )
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# 📊 Dual Axis
# -----------------------
with tab3:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered["Year"],
        y=filtered[temp_col],
        name="Temperature",
        yaxis="y1"
    ))

    fig.add_trace(go.Scatter(
        x=filtered["Year"],
        y=filtered[co2_col],
        name="CO₂",
        yaxis="y2"
    ))

    fig.update_layout(
        title="CO₂ vs Temperature (Dual Axis)",
        template="plotly_dark",
        yaxis=dict(title="Temperature Anomaly"),
        yaxis2=dict(title="CO₂", overlaying="y", side="right"),
        xaxis=dict(title="Year")
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 📉 Industrialization Comparison
# -----------------------
with tab4:
    pre = df[df["Year"] < 1950]
    post = df[df["Year"] >= 1950]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pre-1950")
        st.metric("Avg Temp Anomaly", f"{pre['Temp_Anomaly'].mean():.2f}")
        st.metric("Avg CO₂", f"{pre['CO2'].mean():.2f}")

    with col2:
        st.subheader("Post-1950")
        st.metric("Avg Temp Anomaly", f"{post['Temp_Anomaly'].mean():.2f}")
        st.metric("Avg CO₂", f"{post['CO2'].mean():.2f}")

    st.markdown("---")

    comparison = pd.DataFrame({
        "Period": ["Pre-1950", "Post-1950"],
        "Temp": [pre["Temp_Anomaly"].mean(), post["Temp_Anomaly"].mean()],
        "CO2": [pre["CO2"].mean(), post["CO2"].mean()]
    })

    fig4 = px.bar(
        comparison,
        x="Period",
        y=["Temp", "CO2"],
        barmode="group",
        title="Before vs After Industrialization",
        template="plotly_dark"
    )

    st.plotly_chart(fig4, use_container_width=True)

# -----------------------
# Insights
# -----------------------
st.markdown("## Key Insights")
st.markdown("""
- Rolling averages reveal long-term climate trends more clearly  
- CO₂ and temperature show strong positive correlation  
- Post-1950 period shows major acceleration in both metrics  
""")