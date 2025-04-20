import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    sheets = {}
    columns_mapping = {
        ' رقم الموظف ': 'employee_id',
        ' الاسم ': 'name',
        ' الجنسية ': 'nationality',
        ' الموقع ': 'location',
        ' الوظيفة ': 'position',
        ' القسم ': 'department'
    }
    for sheet in ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6"]:
        try:
            df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx", sheet_name=sheet, skiprows=6, na_filter=False)
            
            # معالجة أسماء الأعمدة لإزالة المسافات الزائدة والرموز
            df.columns = df.columns.str.strip().str.replace('\n', ' ')
            
            # إعادة تسمية الأعمدة باستخدام columns_mapping
            df = df.rename(columns=columns_mapping).dropna(how='all')
            
            # ضمان فرادة أسماء الأعمدة
            df.columns = pd.io.parsers.base_parser.ParserBase.uniqueify_columns(df.columns)
            
            # معالجة القيم الخاصة (مثل NaN) قبل حفظ الجدول
            df = df.fillna('')
            
            sheets[sheet] = df
        except Exception as e:
            st.error(f"خطأ في تحميل {sheet}: {str(e)}")
    return sheets

st.set_page_config(layout="wide", page_title="نظام البحث عن الموظف")
st.title("🔍 نظام البحث عن الموظف")

query = st.text_input("🔍 أدخل اسم الموظف، رقم الموظف، أو أي بيانات أخرى", help="يمكنك البحث بأي جزء من المعلومات")

if query.strip():
    all_sheets = load_data()
    results_found = False
    with st.spinner("جاري البحث في السجلات ..."):
        for sheet_name, df in all_sheets.items():
            try:
                # تأكد من أن جميع الأعمدة تحتوي على قيم صالحة قبل البحث
                mask = df.apply(
                    lambda col: col.astype(str).str.contains(query, case=False, regex=False),
                    axis=0
                ).any(axis=1)
                matched_data = df[mask]
                if not matched_data.empty:
                    st.subheader(f"📑 النتائج من جدول: {sheet_name}")
                    # معالجة القيم الخاصة قبل تحويل الأعمدة إلى سلاسل نصية
                    matched_data = matched_data.fillna('').astype(str)
                    st.dataframe(matched_data, use_container_width=True)
                    results_found = True
            except Exception as e:
                st.error(f"خطأ عند معالجة الجدول {sheet_name}: {str(e)}")
    if not results_found:
        st.warning("⚠️ لم يتم العثور على نتائج مطابقة", icon="⚠️")
else:
    st.info("ℹ️ الرجاء إدخال كلمة البحث لبدء البحث", icon="ℹ️")

with st.sidebar:
    st.header("📘 دليل الاستخدام")
    st.markdown("""
    **طريقة الاستخدام:**
    - أدخل أي جزء من بيانات الموظف (الاسم، الرقم، الجنسية ...)
    - يبحث البرنامج تلقائيًا في جميع الجداول
    **المتطلبات:**
    - نفس تنسيق ملف Excel الموجود
    **الإصدار:** 1.2.0  
    **تم التطوير بواسطة:** الفريق التقني - 2024
    """)
