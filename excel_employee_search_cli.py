
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_excel("duty_roster_mar_2025.xlsx", engine="openpyxl")

def search_employee(df, query, by="id"):
    query = str(query).strip().lower()
    if by == "id":
        return df[df["ID#"].astype(str).str.contains(query, case=False, na=False)]
    else:
        return df[df["Name"].astype(str).str.lower().str.contains(query, na=False)]

st.title("🔍 نظام البحث عن الموظف")

search_type = st.radio("نوع البحث", ["بالاسم", "برقم الموظف"])
query = st.text_input("👤 الاسم أو رقم الموظف")

if query:
    df = load_data()
    if search_type == "بالاسم":
        result = search_employee(df, query, by="name")
    else:
        result = search_employee(df, query, by="id")

    if not result.empty:
        st.success("✅ تم العثور على نتائج مطابقة")
        st.dataframe(result)
    else:
        st.warning("🚫 لا توجد نتائج مطابقة")
