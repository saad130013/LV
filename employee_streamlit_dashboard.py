import streamlit as st
import pandas as pd

st.set_page_config(page_title="لوحة الموظف", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name="Table3", skiprows=6)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

st.title("🔍 نظام البحث عن موظف")

query = st.text_input("👨‍💼 الاسم أو رقم الموظف", "")

if query:
    result = df[df["ID#"].astype(str).str.contains(query, case=False, na=False) | df["EMP#"].astype(str).str.contains(query, case=False, na=False)]
    if not result.empty:
        for _, row in result.iterrows():
            st.subheader(f"👤 {row['EMP#']} | {row['NAME']}")
            st.markdown(f"🆔 الهوية: `{row['ID#']}`")
            st.markdown(f"🏢 الشركة: `{row['COMPANY']}`")
            st.markdown(f"🧑‍💼 الوظيفة: `{row['POSITION']}`")
            st.markdown(f"📍 الموقع: `{row['LOCATION']}`")
            st.markdown(f"📋 الملاحظات: `{row.get('COMMENTS', 'لا توجد')}`")
            attendance = [row.get(col, 0) for col in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]]
            st.write("📊 الحضور الأسبوعي:")
            st.dataframe(pd.DataFrame({
                "اليوم": ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
                "الحالة": attendance
            }))
            attended = sum(1 for a in attendance if a == 1)
            ratio = attended / 7
            if ratio < 0.75:
                st.warning(f"⚠️ نسبة الحضور منخفضة: %{ratio * 100:.2f}")
            else:
                st.success(f"✅ نسبة الحضور: %{ratio * 100:.2f}")
    else:
        st.info("🚫 لا توجد نتائج مطابقة.")
else:
    st.warning("⚠️ أدخل استعلام البحث لعرض النتائج.")