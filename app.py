import streamlit as st
import requests

# إعدادات الواجهة
st.set_page_config(page_title="محمل زايد الاحترافي HD", page_icon="🔥", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505 !important; }
    * { font-family: 'Tajawal', sans-serif !important; }
    .title-text {
        color: #D4AF37 !important; text-align: center; font-size: 32px !important; font-weight: 700 !important;
        margin-bottom: 20px; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }
    div[data-baseweb="input"] { background-color: #111 !important; border-radius: 10px !important; }
    div[data-baseweb="input"]:focus-within { border-color: #D4AF37 !important; }
    input { color: #fff !important; }
    div.stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #AA7C11 100%) !important; 
        color: #000 !important; border-radius: 10px !important; font-weight: 700 !important; 
        width: 100% !important; margin-top: 10px !important;
    }
    div.stDownloadButton > button {
        border-radius: 10px !important; font-weight: 700 !important; width: 100% !important; margin-top: 15px !important;
    }
    div[data-testid="column"]:nth-child(1) div.stDownloadButton > button {
        background: #D4AF37 !important; color: #000 !important; border: none !important;
    }
    div[data-testid="column"]:nth-child(2) div.stDownloadButton > button {
        background: #111 !important; color: #D4AF37 !important; border: 1px solid #D4AF37 !important;
    }
</style>
""", unsafe_allow_html=True)

def fetch_tiktok_urls(url):
    """سحب الروابط الأصلية الخام من السيرفر مباشرة"""
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, timeout=15).json()
        if res.get("code") == 0:
            v_url = res["data"].get("hdplay") or res["data"].get("play")
            m_url = res["data"].get("music")
            return v_url, m_url
    except:
        pass
    return None, None

st.markdown('<div class="title-text">🔥 محمل زايد (الصوت والفيديو الأصلي)</div>', unsafe_allow_html=True)

url_input = st.text_input("ضع رابط الفيديو هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الملفات 🚀"):
    if url_input:
        with st.spinner("جاري سحب الملفات الخام بدون أي ضغط... ⏳"):
            # تصفير الجلسة القديمة
            st.session_state['v_bytes'] = None
            st.session_state['m_bytes'] = None
            st.session_state['ready'] = False
            
            v_url, m_url = fetch_tiktok_urls(url_input)
            
            if v_url:
                try:
                    # تحميل بايتات الفيديو بالكامل لضمان عدم التقطيع أثناء الحفظ
                    v_response = requests.get(v_url, timeout=20)
                    if v_response.status_code == 200:
                        st.session_state['v_bytes'] = v_response.content
                    
                    if m_url:
                        m_response = requests.get(m_url, timeout=20)
                        if m_response.status_code == 200:
                            st.session_state['m_bytes'] = m_response.content
                            
                    st.session_state['ready'] = True
                    st.success("تم سحب الملفات الأصلية! جاهزة للتحميل بكامل فريماتها.")
                except Exception as e:
                    st.error("حدث خطأ أثناء تحميل حزم البيانات، حاول مجدداً.")
            else:
                st.error("تأكد من الرابط أو أن الحساب عام.")
    else:
        st.warning("الرجاء إدخال الرابط.")

# أزرار التحميل
if st.session_state.get('ready'):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('v_bytes'):
            st.download_button(
                label="تحميل الفيديو 🎬 (MP4)",
                data=st.session_state['v_bytes'],
                file_name="Video_Raw_HD.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
    with col2:
        if st.session_state.get('m_bytes'):
            st.download_button(
                label="تحميل الصوت 🎵 (MP3)",
                data=st.session_state['m_bytes'],
                file_name="Audio_Original.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )
