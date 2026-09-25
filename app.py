import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="تنزيل تيك توك", page_icon="🦅")

# كود CSS للتصميم والألوان 
st.markdown("""
<style>
    .block-container {
        direction: rtl;
        text-align: right;
    }
    .stTextInput input {
        text-align: right;
        border-radius: 8px;
        background-color: #f0f2f6;
        padding: 12px;
    }
    .success-box {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
        border: 1px solid #c8e6c9;
        text-align: center;
    }
    .download-btn-normal {
        display: block;
        width: 100%;
        background-color: #111111;
        color: white !important;
        padding: 15px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 12px;
    }
    .download-btn-normal:hover {
        background-color: #333333;
    }
    .download-btn-hd {
        display: block;
        width: 100%;
        background-color: #ff0050;
        color: white !important;
        padding: 15px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 12px;
    }
    .download-btn-hd:hover {
        background-color: #e00045;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2>تنزيل فيديو تيك توك بدون علامه مائية وبأعلى جودة خاوة 🦅</h2>", unsafe_allow_html=True)

url = st.text_input("", placeholder=":انسخ رابط الفيديو هون")

if st.button("تنزيل الفيديو"):
    if url:
        with st.spinner("جاري استخراج المقطع..."):
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            try:
                response = requests.get(api_url).json()
                if response.get('code') == 0:
                    video_data = response.get('data', {})
                    
                    # استخراج الروابط
                    normal_link = video_data.get('play')
                    hd_link = video_data.get('hdplay')
                    
                    st.markdown("<div class='success-box'>!تم السحب خاوة</div>", unsafe_allow_html=True)
                    
                    # زر الجودة العادية (لحل مشكلة التقطيع)
                    if normal_link:
                        st.markdown(f'<a href="{normal_link}" target="_blank" class="download-btn-normal">تحميل الجودة العادية (بدون تقطيع بالمعرض)</a>', unsafe_allow_html=True)
                    
                    # زر الجودة الفائقة (ممكن تقطع)
                    if hd_link and hd_link != normal_link:
                        st.markdown(f'<a href="{hd_link}" target="_blank" class="download-btn-hd">تحميل جودة HD (قد تقطع في المعرض)</a>', unsafe_allow_html=True)
                        
                else:
                    st.error("تعذر العثور على المقطع. يرجى التأكد من صحة الرابط.")
            except Exception as e:
                st.error("حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.")
    else:
        st.warning("يرجى إدخال الرابط أولاً.")
