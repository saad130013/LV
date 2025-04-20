
import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام البحث عن الموظف", layout="centered")
st.title("🔍 نظام البحث عن الموظف")

@st.cache_data
def load_data():
    df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name="Table 3")
    df.columns = df.columns.str.strip()
    return df

df = load_data()
st.write("📋 الأعمدة المتوفرة:", df.columns.tolist())

search_by = st.radio("نوع البحث:", ["بالاسم", "برقم الموظف"])
query = st.text_input("👤 الاسم أو رقم الموظف")

if query:
    if search_by == "بالاسم" and "EMP#" in df.columns:
        result = df[df["EMP#"].astype(str).str.contains(query.strip(), case=False, na=False)]
    elif search_by == "برقم الموظف" and "ID#" in df.columns:
        result = df[df["ID#"].astype(str).str.contains(query.strip(), case=False, na=False)]
    else:
        result = pd.DataFrame()

    if not result.empty:
        st.success("✅ تم العثور على النتائج:")
        st.dataframe(result)
    else:
        st.warning("⚠️ لا توجد نتائج مطابقة.")
