
import streamlit as st
import pandas as pd

st.set_page_config(page_title="لوحة حضور الموظفين", layout="wide")

# تحميل البيانات مع طباعة الأعمدة للتأكد من أسمائها
@st.cache_data
def load_data():
    df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name="Table 3", skiprows=6)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ✅ طباعة أسماء الأعمدة في الواجهة
st.write("🧾 الأعمدة المتوفرة:", df.columns.tolist())

# نموذج بحث مبسط
st.title("🔎 البحث عن موظف")
query = st.text_input("اكتب اسم الموظف أو رقمه")

if query:
    st.info("🔍 سيتم تنفيذ البحث بعد التأكد من أسماء الأعمدة.")
else:
    st.warning("⚠️ أدخل استعلام للبحث لعرض النتائج.")
