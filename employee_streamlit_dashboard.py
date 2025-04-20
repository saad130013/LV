
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    sheets = {}
    for sheet in ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6"]:
        try:
            df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name=sheet, skiprows=6)
            df.columns = df.columns.str.strip()
            sheets[sheet] = df
        except Exception as e:
            st.warning(f"لم يتم تحميل الصفحة {sheet} بسبب: {e}")
    return sheets

st.set_page_config(layout="wide", page_title="نظام البحث عن الموظف")
st.title("🔎 نظام البحث عن موظف")

query = st.text_input("🧑‍💼 الاسم أو رقم الموظف")

if query:
    all_sheets = load_data()
    results = []
    for sheet, df in all_sheets.items():
        mask = df.astype(str).apply(lambda row: row.str.contains(query, case=False, na=False)).any(axis=1)
        matched = df[mask]
        if not matched.empty:
            st.subheader(f"📄 النتائج من الورقة: {sheet}")
            st.dataframe(matched)
            results.append(matched)

    if not results:
        st.warning("⚠️ لا توجد نتائج مطابقة.")
else:
    st.info("✍️ أدخل استعلام البحث لعرض النتائج.")
