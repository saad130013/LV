
import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="نظام البحث عن الموظفين", layout="wide")
st.title("🔍 نظام إدارة دوام الموظفين")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_excel("duty_roster_mar_2025.xlsx", engine="openpyxl")

df = load_data()

# واجهة البحث
st.sidebar.header("🧭 بحث")
search_type = st.sidebar.radio("نوع البحث", ["🔢 برقم الهوية", "🔤 بالاسم"])
query = st.sidebar.text_input("🔍 أدخل القيمة للبحث")

# نتيجة البحث
if query:
    if search_type == "🔢 برقم الهوية":
        result = df[df["ID#"].astype(str).str.contains(query.strip(), case=False, na=False)]
    else:
        result = df[df["Name"].astype(str).str.contains(query.strip(), case=False, na=False)]

    if not result.empty:
        st.success(f"✅ تم العثور على {len(result)} نتيجة")
        for _, row in result.iterrows():
            st.markdown("---")
            st.markdown(f"### 👤 {row['Name']} | 🆔 {row['ID#']}")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**الوظيفة:** {row.get('POSITION', 'غير محددة')}")
                st.info(f"**الشركة:** {row.get('COMPANY', 'غير مسجلة')}")
            with col2:
                st.info(f"**الجنسية:** {row.get('NATIONALITY', '-')}")
                st.info(f"**الموقع:** {row.get('LOCATION', '-')}")
            
            # إحصائيات الحضور
            week_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
            presence = [int(row[day]) if pd.notna(row[day]) else 0 for day in week_days]
            total_present = sum(presence)
            attendance_percent = round((total_present / len(week_days)) * 100)

            st.metric("📈 نسبة الحضور الأسبوعي", f"{attendance_percent} %")
            if attendance_percent < 50:
                st.error("🚨 نسبة الحضور منخفضة جدًا!")
            elif attendance_percent < 80:
                st.warning("⚠️ الحضور أقل من المتوقع.")
            else:
                st.success("✅ حضور ممتاز هذا الأسبوع.")
    else:
        st.warning("🚫 لا توجد نتائج مطابقة.")
else:
    st.info("👈 ابدأ بإدخال رقم أو اسم الموظف من القائمة الجانبية.")
