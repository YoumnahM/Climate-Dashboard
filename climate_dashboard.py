import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="AI vs Climate", layout="wide")

# ============ Load Data ============
df = pd.read_excel('AI_vs_Climate_Dataset.xlsx', sheet_name='AI_Climate_Use_Cases')

# Load model emissions data
df_models = pd.read_excel('AI_vs_Climate_Dataset.xlsx', sheet_name='AI_Model_Emissions')
df_models = df_models.rename(columns={
    'AI Model': 'model_name',
    'Queries per Day': 'daily_queries',
    'CO2 Emissions (Tons)': 'emissions'
})

# Load emissions tradeoff data
df_tradeoffs = pd.read_excel('AI_vs_Climate_Dataset.xlsx', sheet_name='CO2_Tradeoffs')
df_tradeoffs = df_tradeoffs.rename(columns={
    'AI Use Case': 'AI Use Case',
    'Emissions Generated (tons)': 'co2_emissions',
    'Emissions Prevented (tons)': 'co2_saved',
    'Net CO2 Savings (tons)': 'net_co2_savings'
})

# ============ Sidebar ============
st.sidebar.image("logo.png", use_container_width=True)

# Sidebar filters
selected_country = st.sidebar.selectbox("🌍 Select Country", options=["All"] + sorted(df['Country'].dropna().unique()))
selected_use_case = st.sidebar.selectbox("🧠 Select Use Case", options=["All"] + sorted(df['Use Case Description'].dropna().unique()))

# Apply filters
df_filtered = df.copy()

if selected_country != "All":
    df_filtered = df_filtered[df_filtered['Country'] == selected_country]

if selected_use_case != "All":
    df_filtered = df_filtered[df_filtered['Use Case Description'] == selected_use_case]

# ============ Helper Function ============
def stat_card(title, value, color="black"):
    st.markdown(f"<div style='border: 1px solid #ddd; border-radius:8px; padding:15px; text-align:center; color:{color}'>"
                f"<h3>{title}</h3><h2>{value}</h2></div>", unsafe_allow_html=True)

# --- Custom KPI Card Function ---
def stat_card(title, value, icon=None, color="black"):
    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h4 style="color: {color}; margin-bottom: 10px;">{title}</h4>
            <h2 style="margin: 0; font-size: 28px;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)


# ============ Main Content ============
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Overview",
    "🗺️ Global Impact & Use Cases",
    "⚖️ Emissions vs Benefits",
    "🎯 Conclusion"
])

# --- Slide 1: ---
with tab1:
    st.title("🌍 AI vs Climate: Can Tech Save the Planet?")

    # 3 KPI-style cards
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        stat_card("🌐 Global AI for Climate", "50+ Countries", color="blue")
    with kpi2:
        stat_card("♻️ Net CO₂ Impact", "↑ 120M tons saved", color="green")
    with kpi3:
        stat_card("⚡ AI Energy Demand", "150 TWh/year", color="red")
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("## 🎯 Objective")
    st.markdown("""
    To evaluate if **AI is truly a net positive** for the planet and to understand how we can **amplify its benefits** while minimizing its climate cost.
    """)

    # Global Map of AI Impact
    st.markdown("### 🌎 Where is AI making an impact?")
    fig_map = px.choropleth(
        df_filtered,
        locations='Country',
        locationmode='country names',
        color='Estimated Impact',
        hover_name='Country',
        hover_data=['Application Area', 'Use Case Description', 'Estimated Impact'],
        title='Global AI Use for Climate Impact'
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Top Use Cases Chart
    st.markdown("### 🧠 Most Common AI Use Cases in Climate")
    use_case_counts = df_filtered['Use Case Description'].value_counts().nlargest(10).reset_index()
    use_case_counts.columns = ['Use Case Description', 'Count']
    fig_usecases = px.bar(
        use_case_counts,
        x='Use Case Description',
        y='Count',
        title='Top 10 AI Use Cases for Climate Solutions',
        color='Count',
        color_continuous_scale='Greens'
    )
    fig_usecases.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_usecases, use_container_width=True)


# --- Slide 2: ---
with tab2:
    st.title("🗺️ Global Impact & Use Cases")

    # --- Choropleth Map ---
    st.markdown("### 🌍 Where AI is Being Used for Climate Solutions")

    fig_map = px.choropleth(
        df_filtered,
        locations='Country',
        locationmode='country names',
        color='Estimated Impact',
        hover_name='Country',
        hover_data={
            'Country': False,
            'Application Area': True,
            'Use Case Description': True,
            'Estimated Impact': True
        },
        title='🌐 Global Footprint of AI for Climate Action',
        color_continuous_scale=px.colors.sequential.PuBuGn,
        height=600
    )

    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            landcolor='lightgray',
            showland=True,
            showcountries=True
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Estimated<br>Climate Impact",
            ticksuffix=' Mt CO₂e',
            lenmode='fraction',
            len=0.75
        )
    )

    fig_map.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                    "🧠 <b>Area:</b> %{customdata[0]}<br>" +
                    "🌱 <b>Use Case:</b> %{customdata[1]}<br>" +
                    "💡 <b>Impact:</b> %{z} Mt CO₂e<extra></extra>"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.info("🌍 **Insight:** AI adoption for climate is spreading across continents, with varying estimated impact by region and use case.")



    # --- Sector / Use Case Breakdown ---
    st.markdown("### 🧠 Top Sectors Where AI Tackles Climate Change")
    sector_counts = df_filtered['Application Area'].value_counts().reset_index()
    sector_counts.columns = ['Sector', 'Use Count']

    fig_sector = px.bar(
        sector_counts,
        x='Sector',
        y='Use Count',
        title="AI Applications by Sector",
        color='Use Count',
        color_continuous_scale='tealgrn'
    )
    fig_sector.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sector, use_container_width=True)

    st.markdown("✅ **Insight:** AI is concentrated in key sectors like **energy**, **agriculture**, and **transport**, but some sectors remain underutilized — an opportunity for growth.")


# --- Slide 3: ---
with tab3:
    st.title("⚖️ AI Emissions vs Climate Benefit")

    # Load the emissions/savings sheet
    df_tradeoffs = pd.read_excel("AI_vs_Climate_Dataset.xlsx", sheet_name="CO2_Tradeoffs")

    # Clean column names
    df_tradeoffs = df_tradeoffs.rename(columns={
        'AI Use Case': 'AI Use Case',
        'Emissions Generated (tons)': 'co2_emissions',
        'Emissions Prevented (tons)': 'co2_saved',
        'Net CO2 Savings (tons)': 'net_co2_savings'
    })

    # --- Grouped Bar Chart ---
    st.markdown("### 📊 Emissions vs Savings by AI Use Case")
    fig_tradeoff = go.Figure(data=[
        go.Bar(name='CO₂ Emitted', x=df_tradeoffs['AI Use Case'], y=df_tradeoffs['co2_emissions'], marker_color='red'),
        go.Bar(name='CO₂ Saved', x=df_tradeoffs['AI Use Case'], y=df_tradeoffs['co2_saved'], marker_color='green')
    ])
    fig_tradeoff.update_layout(
        barmode='group',
        title="Carbon Emissions vs Climate Benefit by AI Use Case",
        xaxis_title='AI Use Case',
        yaxis_title='CO₂ (tons)',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_tradeoff, use_container_width=True)

    # --- Net Impact Metric ---
    total_saved = df_tradeoffs['co2_saved'].sum()
    total_emitted = df_tradeoffs['co2_emissions'].sum()
    net_impact = total_saved - total_emitted

    st.metric(
        label="♻️ Net CO₂ Impact Across All Use Cases",
        value=f"{net_impact:,.0f} tons CO₂e saved",
        delta=f"{total_saved:,.0f} saved - {total_emitted:,.0f} emitted"
    )

    st.markdown("✅ **Insight:** Most AI use cases prevent more emissions than they generate, suggesting a **net positive** role — but efficiency and scope vary widely.")
    st.markdown("<br><br>", unsafe_allow_html=True)

# --- Sustainability Metrics ---
    st.markdown("### 🌿 Sustainability Efficiency Metrics")

    # Calculate efficiency
    df_tradeoffs['Efficiency (tons saved per ton emitted)'] = df_tradeoffs['net_co2_savings'] / df_tradeoffs['co2_emissions']

    # Remove infinite or NaN
    df_eff = df_tradeoffs.replace([float('inf'), float('-inf')], None).dropna(subset=['Efficiency (tons saved per ton emitted)'])

    # KPI Cards
    col1, col2 = st.columns(2)
    with col1:
        avg_eff = df_eff['Efficiency (tons saved per ton emitted)'].mean()
        stat_card("🌱 Avg. Efficiency", f"{avg_eff:.2f} tons saved/ton emitted", color="green")
    with col2:
        best_row = df_eff.loc[df_eff['Efficiency (tons saved per ton emitted)'].idxmax()]
        stat_card("💡 Most Efficient Use Case", f"{best_row['AI Use Case']} ({best_row['Efficiency (tons saved per ton emitted)']:.2f})", color="blue")

    st.markdown("<br><br>", unsafe_allow_html=True)
    # Efficiency Ranking Chart
    st.markdown("### 📊 Efficiency by Use Case (Net CO₂ Savings ÷ Emissions)")
    fig_efficiency = px.bar(
        df_eff.sort_values('Efficiency (tons saved per ton emitted)', ascending=False),
        x='AI Use Case',
        y='Efficiency (tons saved per ton emitted)',
        color='Efficiency (tons saved per ton emitted)',
        color_continuous_scale='Viridis',
        title="Sustainability Efficiency by AI Use Case"
    )
    fig_efficiency.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_efficiency, use_container_width=True)

    st.info("🧮 **Insight:** Higher efficiency means more climate benefit per unit of emission. Focus on scaling these use cases.")

# --- Slide 4:  ---
with tab4:
    st.title("🎯 Conclusion & Call to Action")

    # Summary box
    st.markdown("""
    <div style='background-color:#f5f5f5; padding:25px; border-radius:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1)'>
        <h3>🌍 Key Takeaways</h3>
        <ul style='line-height: 1.8'>
            <li>AI is already making a global impact in tackling climate issues, with widespread use across <b>50+ countries</b>.</li>
            <li>Top sectors leveraging AI include <b>energy, agriculture, and transport</b>.</li>
            <li>Many use cases show <b>more emissions prevented than generated</b> — suggesting AI can be a net positive for the planet.</li>
            <li><b>Model efficiency matters</b> — choosing lower-emission AI tools is key to sustainable tech deployment.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📌 What You Can Do")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🌱 **Use Eco-efficient Models**\n\nFavor smaller, energy-conscious models when possible.")
    with col2:
        st.info("🔍 **Target High-Impact Areas**\n\nApply AI where it can deliver real climate benefits.")
    with col3:
        st.warning("📢 **Advocate for Responsible AI**\n\nPush for transparency and sustainability in AI policies.")

    st.markdown("---")

    st.markdown("## 🚀 Final Thought")
    st.markdown("**Technology alone won’t save the planet — but used wisely, it can be a powerful ally.** 💡")

    # --- Forecast Explanation ---
    st.markdown("""
    ---
    ### 🔮 Future Carbon Savings Forecast

    **What is this forecast?**

    This projection shows potential future carbon dioxide savings if AI use cases for climate continue to expand over the next 6 years (2025-2030).

    - The starting point (baseline) is the current total net CO₂ savings from all AI use cases in our dataset.
    - We simulate three scenarios:
        - **Baseline (0% growth):** Net savings stay the same each year.
        - **Moderate Growth (10% yearly increase):** Savings increase by 10% every year.
        - **Aggressive Growth (20% yearly increase):** Savings increase by 20% every year.

    This helps illustrate the possible climate benefits as AI adoption scales up.
    """)

    import pandas as pd
    import plotly.graph_objects as go

    # Calculate baseline net CO2 savings from your dataset
    total_saved = df_tradeoffs['co2_saved'].sum()
    total_emitted = df_tradeoffs['co2_emissions'].sum()
    net_impact = total_saved - total_emitted

    years = list(range(2025, 2031))  # 2025 to 2030

    # Define growth rates
    growth_scenarios = {
        "Baseline (0% growth)": 0.00,
        "Moderate Growth (10%)": 0.10,
        "Aggressive Growth (20%)": 0.20
    }

    # Create forecast data
    forecast_data = {}
    for scenario, growth_rate in growth_scenarios.items():
        values = []
        current_value = net_impact
        for year in years:
            values.append(current_value)
            current_value = current_value * (1 + growth_rate)
        forecast_data[scenario] = values

    # Plotly figure
    fig_forecast = go.Figure()

    for scenario, values in forecast_data.items():
        fig_forecast.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            name=scenario
        ))

    fig_forecast.update_layout(
        title="Projected Net CO₂ Savings from AI Use Cases (tons CO₂e)",
        xaxis_title="Year",
        yaxis_title="Net CO₂ Savings (tons)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

    # Summary takeaway below the chart
    st.markdown("""
    **Key takeaway:**  
    Even a moderate 10% annual growth in AI adoption can more than double net CO₂ savings by 2030, highlighting AI’s powerful potential for climate action.
    """)

    # Optional technical explanation in an expander
    with st.expander("📊 How is this forecast calculated?"):
        st.markdown("""
        - The current net CO₂ savings (baseline) are taken from the sum of savings in our dataset.
        - Each year, savings are projected to grow by a fixed percentage:
            - Moderate: multiply previous year by 1.10 (10% increase)
            - Aggressive: multiply previous year by 1.20 (20% increase)
        - This compounds annually, so savings grow exponentially.
        """)


# Footer
footer = """
<style>
footer { visibility: hidden; }
.footer-style {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #001f3f;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    opacity: 0.8;
    z-index: 1000;
}
</style>
<div class="footer-style">
    © Copyright 2025 Youmnah Mungur - All rights reserved.
</div>
"""
st.markdown(footer, unsafe_allow_html=True)