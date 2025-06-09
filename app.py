import streamlit as st
import pandas as pd

# Importing modules for different pages
import pages.overview as overview
import pages.rfm_analysis as rfm_analysis
import pages.churn_prediction as churn_prediction
import pages.customer_segmentation as customer_segmentation
import pages.future_predictions as future_predictions

# Set page configuration
st.set_page_config(page_title="CRM Dashboard", layout="wide")

# Define required columns for valid data upload
REQUIRED_COLUMNS = ['CustomerID', 'InvoiceDate', 'Quantity', 'UnitPrice']

@st.cache_data
def load_data(uploaded_file):
    """Load and preprocess data from uploaded file"""
    if uploaded_file is None:
        return None

    try:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
        
        # Convert InvoiceDate to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        
        # Ensure required columns exist
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            st.error(f"🚨 Missing required columns: {', '.join(missing_columns)}. Please check your dataset.")
            return None
        
        # Compute Revenue
        df['Revenue'] = df['UnitPrice'] * df['Quantity']
        
        st.success("✅ Data loaded successfully!")
        return df
    except Exception as e:
        st.error(f"🚨 Error loading file: {e}")
        return None

# Sidebar File Uploader
st.sidebar.header("📂 Upload Your Dataset")
st.sidebar.markdown("""
**📌 Required Columns for Uploading Data:**
- `CustomerID` (Unique identifier for customers)
- `InvoiceDate` (Date of the transaction)
- `Quantity` (Number of units sold)
- `UnitPrice` (Price per unit)

✔ Ensure your CSV file contains these columns.
""")

uploaded_file = st.sidebar.file_uploader("Drag & Drop or Browse a CSV file", type=["csv"])

# Load Data
df = load_data(uploaded_file)

# Sidebar for navigation
st.sidebar.header("📊 CRM Analysis")
page = st.sidebar.radio("Select a Page", ["Overview", "RFM Analysis", "Churn Prediction", "Customer Segmentation", "Future Predictions"])

# Routing to selected page
if df is not None and not df.empty:
    if page == "Overview":
        overview.show(df)
    elif page == "RFM Analysis":
        rfm_analysis.show(df)
    elif page == "Churn Prediction":
        churn_prediction.show(df)
    elif page == "Customer Segmentation":
        customer_segmentation.show(df)
    elif page == "Future Predictions":
        future_predictions.show(df)
else:
    st.warning("⚠ No data available. Please upload a dataset.")
