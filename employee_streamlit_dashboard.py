# employee_streamlit_dashboard.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """تحميل البيانات من جميع الجداول مع معالجة الأخطاء"""
    sheets = {}
    sheet_names = [
        "Table 1", 
        "Table 2", 
        "Table 3", 
        "Table 4", 
        "Table 5", 
        "Table 6"
    ]
    
    for sheet in sheet_names:
        try:
            # تحميل البيانات مع تخطي العناوين غير الضرورية
            df = pd.read_excel(
                "DUTY ROSTER MAR 2025.V.2.xlsx",
                sheet_name=sheet,
                skiprows=6,
                engine='openpyxl'  # ضروري لقراءة ملفات Excel الحديثة
            )
            
            # تنظيف أسماء الأعمدة
            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
                .str.replace("#", "")
                .str.replace(" ", "")
                .str.replace("/", "_")
            )
            
            sheets[sheet] = df
            
        except Exception as e:
            st.warning(f"⚠️ تعذر تحميل الجدول '{sheet}': {str(e)}")
    
    return sheets

# إعداد واجهة المستخدم
st.set_page_config(layout="wide", page_title="نظام إدارة الموظفين")
st.title("🔍 نظام البحث عن الموظفين")

# حقل إدخال البحث
query = st.text_input("🧑‍💼 أدخل اسم الموظف أو رقمه أو أي بيانات أخرى")

if query:
    all_sheets = load_data()
    results_found = False
    
    for sheet_name, df in all_sheets.items():
        try:
            # البحث في جميع الأعمدة
            df_str = df.astype(str)
            mask = df_str.apply(
                lambda col: col.str.contains(query.strip(), case=False, na=False)
            ).any(axis=1)
            
            results = df[mask]
            
            if not results.empty:
                st.subheader(f"📋 النتائج من جدول: {sheet_name}")
                st.dataframe(results)
                results_found = True
                
        except Exception as e:
            st.error(f"❌ خطأ في معالجة الجدول '{sheet_name}': {str(e)}")
    
    if not results_found:
        st.warning("⚠️ لا توجد نتائج مطابقة في أي جدول")
else:
    st.info("🗒️ يرجى إدخال كلمة البحث في الحقل أعلاه")

# شريط جانبي للتعليمات
st.sidebar.markdown("""
### 🧭 دليل الاستخدام
1. **تأكد من**:
   - وجود الملف `DUTY ROSTER MAR 2025.V.2.xlsx` في نفس المجلد
   - تثبيت المكتبات المطلوبة (`pandas`, `streamlit`, `openpyxl`)

2. **خيارات البحث**:
   - يمكن البحث بأي جزء من البيانات (أسماء، أرقام، مواقع...)
   - البحث غير حساس لحالة الأحرف (Aa)

3. **معلومات تقنية**:
   - يدعم البحث في 6 جداول مختلفة
   - يعالج المشاكل الشائعة في تنسيق البيانات
""")

# إشعار حقوق النشر
st.sidebar.markdown("---")
st.sidebar.caption("""
تم تطويره بواسطة [اسمك] - 2024  
الإصدار 1.1.0 | [دليل الاستخدام الكامل](https://github.com/yourusername/employee-search-system)
""")
