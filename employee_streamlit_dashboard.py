import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # تحميل البيانات مع معالجة الأعمدة
    df = pd.read_excel("duty_roster_mar_2025.xlsx", engine="openpyxl")
    
    # تحويل الأعمدة النصية إلى strings وتنظيفها
    text_columns = ['ID#', 'Name']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    return df

def search_employee(df, query, by="id"):
    query = str(query).strip().lower()
    
    try:
        if by == "id":
            # البحث في عمود ID بعد التحويل إلى string
            return df[df["ID#"].astype(str).str.lower().str.contains(query, na=False)]
        else:
            # البحث في عمود الاسم بعد التحويل إلى string
            return df[df["Name"].astype(str).str.lower().str.contains(query, na=False)]
    except Exception as e:
        st.error(f"خطأ في البحث: {str(e)}")
        return pd.DataFrame()

# واجهة المستخدم
st.title("🔍 نظام البحث عن الموظف")

search_type = st.radio("نوع البحث", ["بالاسم", "برقم الموظف"], horizontal=True)
query = st.text_input("👤 أدخل اسم الموظف أو رقم الموظف", help="يمكنك استخدام أي جزء من المعلومات")

if query:
    df = load_data()
    
    with st.spinner("جاري البحث في السجلات..."):
        if search_type == "بالاسم":
            result = search_employee(df, query, by="name")
        else:
            result = search_employee(df, query, by="id")

    if not result.empty:
        st.success(f"✅ تم العثور على {len(result)} نتيجة مطابقة")
        # عرض النتائج مع تهيئة الأعمدة
        st.dataframe(
            result[['ID#', 'Name', 'Department']],
            use_container_width=True,
            column_config={
                "ID#": "رقم الموظف",
                "Name": "الاسم",
                "Department": "القسم"
            }
        )
    else:
        st.warning("⚠️ لا توجد نتائج مطابقة")

# دليل الاستخدام في الشريط الجانبي
with st.sidebar:
    st.header("📘 دليل الاستخدام")
    st.markdown("""
    **طريقة الاستخدام:**
    1. اختر نوع البحث (بالاسم أو بالرقم)
    2. أدخل أي جزء من المعلومات
    3. سيتم عرض النتائج تلقائيًا

    **ملاحظات:**
    - يجب أن يكون ملف Excel بنفس التنسيق المحدد
    - يدعم البحث الجزئي (يمكنك إدخال جزء من الاسم أو الرقم)
    - البحث غير حساس لحالة الأحرف
    
    **الإصدار:** 2.2.0
    """)
