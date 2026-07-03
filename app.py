import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RetailIQ Pro",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

BASE_DIR = Path(__file__).parent

retail_df = pd.read_excel(BASE_DIR / "Retail Data.xlsx")
super_df = pd.read_excel(BASE_DIR / "Sample SuperStore.xlsx")

# ==========================================
# DATA CLEANING
# ==========================================

retail_df["Date"] = pd.to_datetime(
    retail_df["Date"],
    errors="coerce"
)

retail_df["Total Amount"] = (
    retail_df["Quantity"] *
    retail_df["Price per Unit"]
)

# ==========================================
# TITLE
# ==========================================

st.title("📊 RetailIQ Pro")
st.caption(
    "Business Intelligence Dashboard | Python • Streamlit • Pandas • Plotly"
)

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(
    [
        "RetailIQ Dataset",
        "SuperStore Dataset",
        "Comparison Dashboard"
    ]
)

# ====================================================
# RETAIL IQ TAB
# ====================================================

with tab1:

    st.header("RetailIQ Analytics")

    # KPIs

    revenue = retail_df["Total Amount"].sum()
    customers = retail_df["Customer ID"].nunique()
    transactions = retail_df["Transaction ID"].nunique()
    units_sold = retail_df["Quantity"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Revenue", f"${revenue:,.0f}")
    c2.metric("Customers", customers)
    c3.metric("Transactions", transactions)
    c4.metric("Units Sold", units_sold)

    st.markdown("---")

    # =====================================
    # CHART 1
    # BAR CHART
    # =====================================

    category_sales = (
        retail_df.groupby("Product Category")
        ["Total Amount"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Product Category",
        y="Total Amount",
        color="Product Category",
        title="Revenue by Product Category",
        text_auto=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    # =====================================
    # CHART 2
    # LINE CHART
    # =====================================

    time_sales = (
        retail_df.groupby("Date")
        ["Total Amount"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        time_sales,
        x="Date",
        y="Total Amount",
        markers=True,
        title="Revenue Trend Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =====================================
    # CHART 3
    # PIE CHART
    # =====================================

    gender_df = (
        retail_df.groupby("Gender")
        .size()
        .reset_index(name="Customers")
    )

    fig3 = px.pie(
        gender_df,
        names="Gender",
        values="Customers",
        title="Customer Distribution by Gender"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # =====================================
    # CHART 4
    # HISTOGRAM
    # =====================================

    fig4 = px.histogram(
        retail_df,
        x="Age",
        nbins=15,
        title="Customer Age Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # =====================================
    # CHART 5
    # SCATTER PLOT
    # =====================================

    customer_spending = (
        retail_df.groupby(
            ["Customer ID", "Age"]
        )["Total Amount"]
        .sum()
        .reset_index()
    )

    fig5 = px.scatter(
        customer_spending,
        x="Age",
        y="Total Amount",
        trendline="ols",
        title="Customer Age vs Spending"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # =====================================
    # INSIGHTS
    # =====================================

    st.subheader("🧠 Business Insights")

    top_category = (
        retail_df.groupby("Product Category")
        ["Total Amount"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Top-performing category: {top_category}"
    )

# ====================================================
# SUPERSTORE TAB
# ====================================================

with tab2:

    st.header("SuperStore Analytics")

    sales = super_df["Sales"].sum()
    profit = super_df["Profit"].sum()
    quantity = super_df["Quantity"].sum()

    profit_margin = (
        profit / sales * 100
    ) if sales > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Sales", f"${sales:,.0f}")
    c2.metric("Profit", f"${profit:,.0f}")
    c3.metric("Profit Margin", f"{profit_margin:.2f}%")
    c4.metric("Units Sold", quantity)

    st.markdown("---")

    # =====================================
    # CHART 6
    # BAR CHART
    # =====================================

    region_profit = (
        super_df.groupby("Region")
        ["Profit"]
        .sum()
        .reset_index()
    )

    fig6 = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region",
        text_auto=True
    )

    st.plotly_chart(fig6, use_container_width=True)

    # =====================================
    # CHART 7
    # SALES BY CATEGORY
    # =====================================

    category_sales2 = (
        super_df.groupby("Category")
        ["Sales"]
        .sum()
        .reset_index()
    )

    fig7 = px.bar(
        category_sales2,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category",
        text_auto=True
    )

    st.plotly_chart(fig7, use_container_width=True)

    # =====================================
    # CHART 8
    # SCATTER PLOT
    # =====================================

    fig8 = px.scatter(
        super_df,
        x="Discount",
        y="Profit",
        color="Category",
        title="Discount vs Profit"
    )

    st.plotly_chart(fig8, use_container_width=True)

    # =====================================
    # CHART 9
    # HEATMAP
    # =====================================

    heatmap_df = (
        super_df.groupby(
            ["Region", "Category"]
        )["Sales"]
        .sum()
        .reset_index()
    )

    heatmap_pivot = heatmap_df.pivot(
        index="Region",
        columns="Category",
        values="Sales"
    )

    fig9 = px.imshow(
        heatmap_pivot,
        text_auto=True,
        aspect="auto",
        title="Sales Heatmap: Region vs Category"
    )

    st.plotly_chart(fig9, use_container_width=True)

# ====================================================
# COMPARISON TAB
# ====================================================

with tab3:

    st.header("RetailIQ vs SuperStore")

    retail_revenue = retail_df["Total Amount"].sum()
    retail_units = retail_df["Quantity"].sum()

    super_sales = super_df["Sales"].sum()
    super_units = super_df["Quantity"].sum()
    super_profit = super_df["Profit"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "RetailIQ Revenue",
        f"${retail_revenue:,.0f}"
    )

    c2.metric(
        "SuperStore Sales",
        f"${super_sales:,.0f}"
    )

    c3.metric(
        "SuperStore Profit",
        f"${super_profit:,.0f}"
    )

    comparison_df = pd.DataFrame(
        {
            "Dataset": [
                "RetailIQ",
                "SuperStore"
            ],
            "Revenue/Sales": [
                retail_revenue,
                super_sales
            ]
        }
    )

    fig10 = px.bar(
        comparison_df,
        x="Dataset",
        y="Revenue/Sales",
        color="Dataset",
        text_auto=True,
        title="Revenue Comparison"
    )

    st.plotly_chart(fig10, use_container_width=True)

    units_df = pd.DataFrame(
        {
            "Dataset": [
                "RetailIQ",
                "SuperStore"
            ],
            "Units Sold": [
                retail_units,
                super_units
            ]
        }
    )

    fig11 = px.bar(
        units_df,
        x="Dataset",
        y="Units Sold",
        color="Dataset",
        text_auto=True,
        title="Units Sold Comparison"
    )

    st.plotly_chart(fig11, use_container_width=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
### About This Project

**RetailIQ Pro** is a Business Intelligence dashboard built using:

- Python
- Pandas
- Streamlit
- Plotly

### Features

- KPI Monitoring
- Customer Analytics
- Revenue Analysis
- Profitability Analysis
- Demographic Insights
- Comparative Benchmarking
- Interactive Visualizations

### Visualizations Used

- Bar Charts
- Line Charts
- Pie Charts
- Histograms
- Scatter Plots
- Heatmaps

**Developer:** Adebowale Adesida  
**Degree:** B.B.A. Management Information Systems  
**University:** Georgia Southern University
"""
)