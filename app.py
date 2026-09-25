import streamlit as st
import requests

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="أداة تنزيل المقاطع", page_icon="📥")

st.title("أداة تنزيل مقاطع الفيديو بجودة أصلية")
url = st.text_input("الرجاء إدخال رابط المقطع هنا:")

if st.button("بدء التنزيل"):
    if url:
        with st.spinner("جاري استخراج المقطع..."):
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            try:
                response = requests.get(api_url).json()
                if response.get('code') == 0:
                    video_data = response.get('data', {})
                    hd_link = video_data.get('hdplay') or video_data.get('play')
                    
                    st.success("تم استخراج الرابط بنجاح.")
                    
                    # زر تحميل مباشر بتصميم احترافي ورسمي
                    st.markdown(f"""
                    <a href="{hd_link}" target="_blank" style="display: block; width: 100%; text-align: center; padding: 12px; background-color: #0056b3; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-family: Arial, sans-serif;">
                        اضغط هنا لتحميل المقطع
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.error("تعذر العثور على المقطع. يرجى التأكد من صحة الرابط وأن الحساب ليس خاصاً.")
            except Exception as e:
                st.error("حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.")
    else:
        st.warning("يرجى إدخال الرابط أولاً قبل الضغط على زر التنزيل.")
