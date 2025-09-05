import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas

st.title("CSV Converter App")

# Upload CSV
uploadfile = st.file_uploader("Choose a CSV file", type='csv')

if uploadfile is not None:
    df = pd.read_csv(uploadfile)
    st.subheader("Preview of Uploaded CSV")
    st.write(df.head())

    # --- JSON download ---
    json_data = df.to_json(orient='records')
    st.download_button(
        label="Click to download JSON",
        data=json_data,
        file_name="converted_file.json",
        mime='application/json'
    )

    # --- Excel download ---
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, sheet_name='Sheet1')
    excel_data = excel_buffer.getvalue()
    st.download_button(
        label="Click to download Excel",
        data=excel_data,
        file_name="converted_file.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # --- PDF download ---
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 800, "This is a PDF generated in Streamlit")
    c.drawString(100, 780, f"DataFrame has {len(df)} rows and {len(df.columns)} columns")
    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    pdf_data = pdf_buffer.getvalue()
    st.download_button(
        label="Click to download PDF",
        data=pdf_data,
        file_name="converted_file.pdf",
        mime='application/pdf'
    )
else:
    st.info("Upload a CSV file to see the conversion options.")
