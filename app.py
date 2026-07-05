from pathlib import Path

import pandas as pd
try:
    import plotly.express as px
except Exception:
    px = None

# Ensure statsmodels availability for Plotly OLS trendline
try:
    import statsmodels.api as sm  # noqa: F401 - imported for plotly trendline
    _HAS_STATSMODELS = True
except Exception:
    _HAS_STATSMODELS = False

import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RetailIQ Pro",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# LOAD DATA (SAFE VERSION)
# ==========================================

BASE_DIR = Path(__file__).parent

def load_excel(filename):
    file_path = BASE_DIR / filename

    if file_path.exists():
        # FIX APPLIED HERE
        return pd.read_excel(file_path, engine="openpyxl")
    else:
        st.warning(f"⚠️ File not found: **{filename}**. Please upload it below.")
        uploaded = st.file_uploader(f"Upload {filename}", type=["xlsx"])
        if uploaded:
            # FIX APPLIED HERE
            return pd.read_excel(uploaded, engine="openpyxl")
        else:
            st.stop()  # Prevent the app from crashing

retail_df = load_excel("Retail Data.xlsx")
super_df = load_excel("Sample SuperStore.xlsx")

# ==========================================
# DATA CLEANING
# ==========================================

retail_df["Date"] = pd.to_datetime(retail_df["Date"], errors="coerce")
retail_df["Total Amount"] = retail_df["Quantity"] * retail_df["Price per Unit"]

# ==========================================
# TITLE
# ==========================================

st.title("📊 RetailIQ Pro")
st.caption("Business Intelligence Dashboard | Python • Streamlit • Pandas • Plotly")

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(["RetailIQ Dataset", "SuperStore Dataset", "Comparison Dashboard"])

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

    if px is not None:
        # BAR CHART
        category_sales = retail_df.groupby("Product Category")["Total Amount"].sum().reset_index()
        fig1 = px.bar(category_sales, x="Product Category", y="Total Amount", color="Product Category",
                      title="Revenue by Product Category", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

        # LINE CHART
        time_sales = retail_df.groupby("Date")["Total Amount"].sum().reset_index()
        fig2 = px.line(time_sales, x="Date", y="Total Amount", markers=True, title="Revenue Trend Over Time")
        st.plotly_chart(fig2, use_container_width=True)

        # PIE CHART
        gender_df = retail_df.groupby("Gender").size().reset_index(name="Customers")
        fig3 = px.pie(gender_df, names="Gender", values="Customers", title="Customer Distribution by Gender")
        st.plotly_chart(fig3, use_container_width=True)

        # HISTOGRAM
        fig4 = px.histogram(retail_df, x="Age", nbins=15, title="Customer Age Distribution")
        st.plotly_chart(fig4, use_container_width=True)

        # SCATTER PLOT
        customer_spending = retail_df.groupby(["Customer ID", "Age"])["Total Amount"].sum().reset_index()
        if _HAS_STATSMODELS:
            fig5 = px.scatter(customer_spending, x="Age", y="Total Amount", trendline="ols",
                              title="Customer Age vs Spending")
        else:
            fig5 = px.scatter(customer_spending, x="Age", y="Total Amount",
                              title="Customer Age vs Spending")
            st.warning("statsmodels is not installed — OLS trendline disabled. Install with `pip install statsmodels` to enable the trendline.")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Plotly is not installed. Charts are disabled. Install with `pip install plotly` to enable visualizations.")

    # INSIGHTS
    st.subheader("🧠 Business Insights")
    top_category = retail_df.groupby("Product Category")["Total Amount"].sum().idxmax()
    st.success(f"Top-performing category: {top_category}")

# ====================================================
# SUPERSTORE TAB
# ====================================================

with tab2:
    st.header("SuperStore Analytics")

    sales = super_df["Sales"].sum()
    profit = super_df["Profit"].sum()
    quantity = super_df["Quantity"].sum()
    profit_margin = (profit / sales * 100) if sales > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sales", f"${sales:,.0f}")
    c2.metric("Profit", f"${profit:,.0f}")
    c3.metric("Profit Margin", f"{profit_margin:.2f}%")
    c4.metric("Units Sold", quantity)

    st.markdown("---")

    if px is not None:
        region_profit = super_df.groupby("Region")["Profit"].sum().reset_index()
        fig6 = px.bar(region_profit, x="Region", y="Profit", color="Region",
                      title="Profit by Region", text_auto=True)
        st.plotly_chart(fig6, use_container_width=True)

        category_sales2 = super_df.groupby("Category")["Sales"].sum().reset_index()
        fig7 = px.bar(category_sales2, x="Category", y="Sales", color="Category",
                      title="Sales by Category", text_auto=True)
        st.plotly_chart(fig7, use_container_width=True)

        fig8 = px.scatter(super_df, x="Discount", y="Profit", color="Category",
                          title="Discount vs Profit")
        st.plotly_chart(fig8, use_container_width=True)

        heatmap_df = super_df.groupby(["Region", "Category"])["Sales"].sum().reset_index()
        heatmap_pivot = heatmap_df.pivot(index="Region", columns="Category", values="Sales")
        fig9 = px.imshow(heatmap_pivot, text_auto=True, aspect="auto",
                         title="Sales Heatmap: Region vs Category")
        st.plotly_chart(fig9, use_container_width=True)
    else:
        st.info("Plotly is not installed. Charts are disabled. Install with `pip install plotly` to enable visualizations.")

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
    c1.metric("RetailIQ Revenue", f"${retail_revenue:,.0f}")
    c2.metric("SuperStore Sales", f"${super_sales:,.0f}")
    c3.metric("SuperStore Profit", f"${super_profit:,.0f}")

    comparison_df = pd.DataFrame({
        "Dataset": ["RetailIQ", "SuperStore"],
        "Revenue/Sales": [retail_revenue, super_sales]
    })

    if px is not None:
        fig10 = px.bar(comparison_df, x="Dataset", y="Revenue/Sales", color="Dataset",
                       text_auto=True, title="Revenue Comparison")
        st.plotly_chart(fig10, use_container_width=True)

        units_df = pd.DataFrame({
            "Dataset": ["RetailIQ", "SuperStore"],
            "Units Sold": [retail_units, super_units]
        })

        fig11 = px.bar(units_df, x="Dataset", y="Units Sold", color="Dataset",
                       text_auto=True, title="Units Sold Comparison")
        st.plotly_chart(fig11, use_container_width=True)
    else:
        st.info("Plotly is not installed. Charts are disabled. Install with `pip install plotly` to enable visualizations.")

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
### About This Project


**Developer:** Adebowale Adesida  
**Degree:** B.B.A. Management Information Systems  
**University:** Georgia Southern University
""")
