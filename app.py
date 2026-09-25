import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="محمل تيك توك الاحترافي", page_icon="✨", layout="centered")

# CSS وتصميم الواجهة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

    [data-testid="stAppViewContainer"] { background-color: #0a0a0a !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    #MainMenu, footer, header { visibility: hidden !important; height: 0px !important; }
    * { font-family: 'Tajawal', sans-serif !important; }

    .title-text {
        color: #D4AF37 !important;
        text-align: center;
        font-size: 34px !important;
        font-weight: 700 !important;
        margin-top: 10px;
        margin-bottom: 5px;
        text-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
    }
    .subtitle-text {
        color: #a0a0a0 !important;
        text-align: center;
        font-size: 15px !important;
        margin-bottom: 30px;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #e0e0e0 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="input"] {
        background-color: #141414 !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
    }
    input { color: #ffffff !important; background-color: transparent !important; }

    /* زر الاستخراج */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
        margin-top: 10px !important;
    }
    div.stButton > button:hover {
        background-color: #f1c40f !important;
        transform: translateY(-2px) !important;
    }

    /* أزرار التحميل */
    div.stDownloadButton > button {
        border: none !important;
        border-radius: 12px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        padding: 12px 15px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
    }
    
    div[data-testid="column"]:nth-child(1) div.stDownloadButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important;
    }

    div[data-testid="column"]:nth-child(2) div.stDownloadButton > button {
        background: #1f1f1f !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }

    .custom-footer {
        text-align: center;
        color: #444444 !important;
        font-size: 13px !important;
        margin-top: 60px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# جلسة متصفح وهمية لتجاوز الحظر
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
})

def get_tiktok_media(url):
    """طريقة مضمونة وتتحمل الضغط لسحب الصوت والفيديو الخالي من التقطيع"""
    # 1. المحاولة الأولى: TikWM API (رابط الفيديو الأصلي المباشر)
    try:
        res = session.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, timeout=12)
        data = res.json()
        if data.get("code") == 0:
            d = data["data"]
            # رابط 'play' يمثل فيديو تيك توك الأصلي الخام وبدون تقطيع فريمات
            v_url = d.get("play") or d.get("hdplay")
            if v_url and v_url.startswith("/"):
                v_url = f"https://www.tikwm.com{v_url}"
            m_url = d.get("music")
            if m_url and m_url.startswith("/"):
                m_url = f"https://www.tikwm.com{m_url}"
            return v_url, m_url
    except:
        pass

    # 2. المحاولة الثانية: TiklyDown
    try:
        res = session.get(f"https://api.tiklydown.eu.org/api/download?url={url}", timeout=12)
        if res.status_code == 200:
            data = res.json()
            v_url = data.get("video", {}).get("noWatermark")
            m_url = data.get("music", {}).get("url")
            return v_url, m_url
    except:
        pass

    return None, None

def download_file_bytes(download_url):
    if not download_url:
        return None
    try:
        r = session.get(download_url, timeout=25)
        if r.status_code == 200:
            return r.content
    except:
        pass
    return None

# الواجهة الرئيسيّة
st.markdown('<div class="title-text">✨ محمل تيك توك الاحترافي</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">سلس، بدون تقطيع فريمات، وبأعلى جودة للمونتاج</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو والصوت 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري استخراج الفيديو والصوت بدون تقطيع... ⏳"):
            v_url, m_url = get_tiktok_media(url)
            
            if v_url:
                v_bytes = download_file_bytes(v_url)
                m_bytes = download_file_bytes(m_url) if m_url else None
                
                if v_bytes:
                    st.session_state['v_bytes'] = v_bytes
                    st.session_state['m_bytes'] = m_bytes
                    st.session_state['ready'] = True
                else:
                    st.error("فشل تحميل بتات الفيديو. حاول مرة أخرى.")
            else:
                st.error("تعذر العثور على الفيديو. تأكد من أن الحساب ليس خاصاً.")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

if st.session_state.get('ready'):
    st.success("تم سحب الملفات بنجاح 100%! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('v_bytes'):
            st.download_button(
                label="تحميل الفيديو (MP4) 🎬",
                data=st.session_state['v_bytes'],
                file_name="tiktok_smooth_video.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
    with col2:
        if st.session_state.get('m_bytes'):
            st.download_button(
                label="تحميل الصوت (MP3) 🎵",
                data=st.session_state['m_bytes'],
                file_name="tiktok_audio.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

st.markdown('<div class="custom-footer">إنشاء زايد</div>', unsafe_allow_html=True)
