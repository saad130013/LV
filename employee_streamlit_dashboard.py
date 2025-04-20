import streamlit as st
import pandas as pd

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
            # تحميل البيانات مع تخطي الصفوف الفارغة ومعالجة الأعمدة المكررة
            df = pd.read_excel(
                "DUTY ROSTER MAR 2025.V.2.xlsx",
                sheet_name=sheet,
                skiprows=6,
                na_filter=False,
                header=0
            ).rename(columns=lambda x: x.strip() if isinstance(x, str) else x)
            
            # تنظيف الأعمدة وإعادة تسميتها
            df = df.loc[:, ~df.columns.duplicated()]  # إزالة الأعمدة المكررة
            df.columns = df.columns.str.strip().str.replace('\n', ' ')
            df = df.rename(columns=columns_mapping).dropna(how='all')
            
            sheets[sheet] = df.fillna('')
        except Exception as e:
            st.error(f"خطأ في تحميل {sheet}: {str(e)}")
    return sheets

# تكوين واجهة المستخدم
st.set_page_config(layout="wide", page_title="نظام البحث عن الموظف")
st.title("🔍 نظام البحث عن الموظف")

# شريط البحث
query = st.text_input("🔎 أدخل اسم الموظف، رقم الموظف، أو أي بيانات أخرى", help="يمكنك البحث بأي جزء من المعلومات")

if query.strip():
    all_sheets = load_data()
    results_found = False
    
    with st.spinner("جاري البحث في السجلات..."):
        for sheet_name, df in all_sheets.items():
            try:
                # البحث في جميع الأعمدة النصية
                mask = df.astype(str).apply(
                    lambda col: col.str.contains(query.strip(), case=False, regex=False)
                ).any(axis=1)
                
                matched_data = df[mask]
                
                if not matched_data.empty:
                    st.subheader(f"📑 النتائج من جدول: {sheet_name}")
                    st.dataframe(
                        matched_data,
                        use_container_width=True,
                        column_config={
                            "employee_id": "رقم الموظف",
                            "name": "الاسم الكامل",
                            "nationality": "الجنسية",
                            "position": "المسمى الوظيفي"
                        }
                    )
                    results_found = True
            except KeyError as ke:
                st.error(f"عمود غير موجود: {ke} - يرجى التحقق من تنسيق الملف")
            except Exception as e:
                st.error(f"خطأ أثناء البحث في {sheet_name}: {str(e)}")

    if not results_found:
        st.warning("⚠️ لم يتم العثور على نتائج مطابقة", icon="⚠️")
else:
    st.info("ℹ️ الرجاء إدخال كلمة البحث لبدء البحث", icon="ℹ️")

# إضافة دليل الاستخدام في الشريط الجانبي
with st.sidebar:
    st.header("دليل الاستخدام")
    st.markdown("""
    1. **طريقة البحث**:
        - ابحث باستخدام أي جزء من البيانات (الاسم، الرقم الوظيفي، الموقع...)
        - البحث غير حساس لحالة الأحرف
        
    2. **المتطلبات**:
        - ملف Excel بنفس الهيكلية المحددة
        - تثبيت الحزم: `streamlit`, `pandas`, `openpyxl`
        
    3. **معلومات تقنية**:
        - يدعم البحث في 6 جداول مختلفة
        - يعالج المشاكل الشائعة في تنسيق البيانات
    """)
    
    st.divider()
    st.markdown("**الإصدار: 2.0.0**")
    st.caption("تم التطوير بواسطة الفريق التقني - 2024")
