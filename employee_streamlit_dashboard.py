import streamlit as st
import pandas as pd

def unique_columns(df):
    """معالجة أسماء الأعمدة المكررة بشكل يدوي"""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cnt = 1
        for idx in cols[cols == dup].index:
            cols[idx] = f"{dup}_{cnt}"
            cnt += 1
    return cols.values

@st.cache_data
def load_data():
    sheets = {}
    columns_mapping = {
        'رقم الموظف': 'employee_id',
        'الاسم': 'name',
        'الجنسية': 'nationality',
        'الموقع': 'location',
        'الوظيفة': 'position',
        'القسم': 'department'
    }
    
    for sheet in ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6"]:
        try:
            df = pd.read_excel(
                "DUTY ROSTER MAR 2025.V.2.xlsx",
                sheet_name=sheet,
                skiprows=6,
                na_filter=False,
                header=0
            )
            
            # تنظيف أسماء الأعمدة
            df.columns = df.columns.str.strip().str.replace('\n', ' ')
            
            # معالجة الأعمدة المكررة
            df.columns = unique_columns(df)
            
            # إعادة تسمية الأعمدة المعروفة
            df = df.rename(columns=lambda x: columns_mapping.get(x.strip(), x))
            
            # إزالة الصفوف الفارغة تماماً
            df = df.dropna(how='all')
            
            # تعبئة القيم الفارغة
            df = df.fillna('')
            
            sheets[sheet] = df
            
        except Exception as e:
            st.error(f"خطأ في تحميل {sheet}: {str(e)}")
    
    return sheets

# تكوين واجهة المستخدم
st.set_page_config(layout="wide", page_title="نظام البحث عن الموظف")
st.title("🔍 نظام البحث عن الموظف")

# شريط البحث
query = st.text_input("🔍 أدخل اسم الموظف، رقم الموظف، أو أي بيانات أخرى", 
                     help="يمكنك البحث بأي جزء من المعلومات")

if query.strip():
    all_sheets = load_data()
    results_found = False
    
    with st.spinner("جاري البحث في السجلات..."):
        for sheet_name, df in all_sheets.items():
            try:
                # البحث في جميع الأعمدة النصية
                mask = df.astype(str).apply(
                    lambda row: row.str.contains(query.strip(), case=False, na=False)
                ).any(axis=1)
                
                matched_data = df[mask]
                
                if not matched_data.empty:
                    st.subheader(f"📑 النتائج من جدول: {sheet_name}")
                    st.dataframe(
                        matched_data,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "employee_id": "رقم الموظف",
                            "name": "الاسم",
                            "nationality": "الجنسية"
                        }
                    )
                    results_found = True
            except Exception as e:
                st.error(f"خطأ في معالجة {sheet_name}: {str(e)}")
    
    if not results_found:
        st.warning("⚠️ لم يتم العثور على نتائج مطابقة", icon="⚠️")
else:
    st.info("ℹ️ الرجاء إدخال كلمة البحث لبدء البحث", icon="ℹ️")

# الشريط الجانبي
with st.sidebar:
    st.header("📘 دليل الاستخدام")
    st.markdown("""
    **طريقة الاستخدام:**
    1. أدخل أي جزء من بيانات الموظف (اسم، رقم، جنسية...)
    2. سيتم البحث تلقائيًا في جميع الجداول
    
    **المتطلبات:**
    - يجب أن يكون ملف Excel بنفس التنسيق المحدد
    - التأكد من وجود الجداول من Table 1 إلى Table 6
    
    **الإصدار:** 2.1.0  
    **آخر تحديث:** 2024
    """)
    st.divider()
    st.markdown("**التطوير:** الفريق التقني")
