import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="CSV Converter",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.header("⚙️ Settings")
st.sidebar.info("Upload a CSV file and download as JSON, Excel or PDF")

# ---------------------------
# Main Title / Banner
# ---------------------------
st.markdown("""
# 📄 CSV Converter App  
Easily upload your CSV file and download it in **JSON**, **Excel**, or **PDF** formats.  
---
""")

# ---------------------------
# Tabs for UI Sections
# ---------------------------
tab1, tab2, tab3 = st.tabs(["Upload & Preview", "Download Options", "About App"])

# Global variable to hold df
df = None

with tab1:
    st.subheader("📤 Upload Your CSV")
    uploadfile = st.file_uploader("Choose a CSV file", type='csv')
    if uploadfile is not None:
        df = pd.read_csv(uploadfile)
        st.success(f"File uploaded successfully! Rows: {len(df)}, Columns: {len(df.columns)}")
        st.write("### 👀 Preview of Data")
        st.write(df.head())

with tab2:
    if df is not None:
        st.subheader("📥 Download Converted Files")

        # --- JSON download ---
        json_data = df.to_json(orient='records')
        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name="your_file.json",
            mime='application/json'
        )

        # --- Excel download ---
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name='Sheet1')
        excel_data = output.getvalue()

        st.download_button(
            label="⬇️ Download Excel (.xlsx)",
            data=excel_data,
            file_name="your_file.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # --- PDF download ---
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)
        c.drawString(100, 800, "📄 CSV Converter App - PDF Summary")
        c.drawString(100, 780, f"DataFrame has {len(df)} rows and {len(df.columns)} columns")
        c.drawString(100, 760, "First few columns:")
        # write column names
        y = 740
        for col in df.columns[:5]:  # only first few cols
            c.drawString(120, y, f"- {col}")
            y -= 15
        c.showPage()
        c.save()
        pdf_buffer.seek(0)
        pdf_data = pdf_buffer.getvalue()

        st.download_button(
            label="⬇️ Download PDF Summary",
            data=pdf_data,
            file_name="your_file.pdf",
            mime='application/pdf'
        )
    else:
        st.info("Please upload a CSV in the first tab to enable download options.")

with tab3:
    st.subheader("ℹ️ About This App")
    st.markdown("""
    This app was built with [Streamlit](https://streamlit.io/) to quickly **convert CSV files**  
    into other formats like **JSON**, **Excel** and **PDF summaries**.

    **How it works:**
    1. Upload a CSV file in the first tab.
    2. Preview your data.
    3. Switch to the "Download Options" tab to save your data in your desired format.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by [Om Gajipara](https://www.linkedin.com/in/omgajipara7/)")

