
import streamlit as st
import pandas as pd

st.set_page_config(page_title="لوحة حضور الموظفين", layout="wide")

# تحميل البيانات مع تخطي الصفوف العلوية
@st.cache_data
def load_data():
    df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name="Table 3", skiprows=6)
df.columns = df.columns.str.strip()  # إزالة الفراغات من أسماء الأعمدة
st.write("🧾 الأعمدة المتوفرة:", df.columns.tolist())

    df.columns = df.columns.str.strip()
    return df

df = load_data()

# واجهة البحث
st.title("🔎 نظام البحث عن الموظف")

query = st.text_input("👨‍💼 الاسم أو رقم الموظف")

if query:
    # البحث بحسب الاسم أو الرقم
    result = df[
        df["ID#"].astype(str).str.contains(query.strip(), case=False, na=False) |
        df["EMP#"].astype(str).str.contains(query.strip(), case=False, na=False) |
        df["NAME"].astype(str).str.contains(query.strip(), case=False, na=False)
    ]
    if not result.empty:
        for _, row in result.iterrows():
            st.markdown("---")
            st.subheader(f"👤 {row['NAME']}")
            st.write(f"🪪 رقم الهوية: `{row['ID#']}`")
            st.write(f"🏷️ رقم الموظف: `{row['EMP#']}`")
            st.write(f"🏢 الشركة: `{row['COMPANY']}`")
            st.write(f"🧑‍💼 الوظيفة: `{row['POSITION']}`")
            st.write(f"📍 الموقع: `{row['LOCATION']}`")

            st.write("📊 جدول الحضور الأسبوعي:")
            week_df = pd.DataFrame({
                "اليوم": ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
                "الحالة": [row["SUN"], row["MON"], row["TUE"], row["WED"], row["THU"], row["FRI"], row["SAT"]]
            })
            st.dataframe(week_df, use_container_width=True)

            attended_days = sum([row["SUN"], row["MON"], row["TUE"], row["WED"], row["THU"]])
            total_days = 5
            percentage = round((attended_days / total_days) * 100, 2)

            if percentage >= 75:
                st.success(f"✅ نسبة الحضور: {percentage}%")
            else:
                st.warning(f"⚠️ نسبة الحضور منخفضة: {percentage}%")

    else:
        st.warning("❌ لا توجد نتائج مطابقة.")
