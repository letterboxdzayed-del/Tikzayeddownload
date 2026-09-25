import streamlit as st
import requests

st.set_page_config(page_title="تنزيل تيك توك HD", page_icon="🔥")

st.title("سحب فيديوهات التيك توك بأعلى جودة خاوة 🦅")
url = st.text_input("انسخ رابط الفيديو هون:")

if st.button("تنزيل الفيديو"):
    if url:
        with st.spinner("جاري سحب الجودة الأصلية..."):
            # استخدام API لجلب جودة HD المخفية
            api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
            try:
                response = requests.get(api_url).json()
                if response.get('code') == 0:
                    # سحب رابط HD إذا توفر، أو الرابط العادي كبديل
                    hd_link = response['data'].get('hdplay') or response['data'].get('play')
                    st.success("تم السحب خاوة!")
                    
                    # عرض الفيديو 
                    st.video(hd_link)
                    
                    # زر للتحميل
                    st.markdown(f"""
                    <a href="{hd_link}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #ff0050; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">اضغط هنا لتحميل الفيديو</a>
                    """, unsafe_allow_html=True)
                else:
                    st.error("تأكد من الرابط أو إن الفيديو مش خاص (Private).")
            except Exception as e:
                st.error("صار خطأ بالاتصال، جرب كمان مرة.")
    else:
        st.warning("حط الرابط أول يا غالي!")
