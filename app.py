import streamlit as st
import requests

st.set_page_config(page_title="محمل تيك توك", page_icon="✨", layout="centered")

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
    input {
        color: #ffffff !important;
        background-color: transparent !important;
    }
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

def fetch_tiktok_data(url):
    # الاعتماد الأساسي: سيرفر يسحب الرابط الخام بدون إعادة ضغط لتجنب فقدان الفريمات
    try:
        res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={url}", headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if "video" in data:
                v_url = data["video"].get("noWatermark")
                m_url = data.get("music", {}).get("url")
                return v_url, m_url
    except:
        pass
    
    # سيرفر احتياطي
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, headers=HEADERS, timeout=15)
        data = res.json()
        if data.get("code") == 0:
            d = data["data"]
            v_url = d.get("hdplay") or d.get("play")
            if v_url and v_url.startswith("/"):
                v_url = f"https://www.tikwm.com{v_url}"
            m_url = d.get("music")
            return v_url, m_url
    except:
        pass

    return None, None

def safe_download_bytes(url):
    """تحميل الملف على دفعات متتالية لتأمين كل الإطارات (Frames) ومنع التقطيع"""
    try:
        res = requests.get(url, stream=True, headers=HEADERS, timeout=30)
        res.raise_for_status()
        
        content = bytearray()
        # تقسيم التحميل لحزم صغيرة لضمان عدم ضياع أي بيانات أثناء النقل
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:
                content.extend(chunk)
        return bytes(content)
    except Exception:
        return None

st.markdown('<div class="title-text">✨ محمل تيك توك</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">جودة خام 60fps، بدون علامة مائية، جاهز للمونتاج</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو والصوت 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري سحب الملف الخام وتأمين الإطارات... ⏳"):
            video_url, music_url = fetch_tiktok_data(url)
            
            if video_url:
                v_bytes = safe_download_bytes(video_url)
                if v_bytes:
                    st.session_state['v_bytes'] = v_bytes
                    
                    if music_url:
                        m_bytes = safe_download_bytes(music_url)
                        if m_bytes:
                            st.session_state['m_bytes'] = m_bytes
                    
                    st.session_state['ready'] = True
                else:
                    st.error("حدث خطأ أثناء تأمين نقل الفيديو. ❌")
            else:
                st.error("عذراً، تعذر سحب الرابط أو الفيديو من حساب خاص. ❌")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

if st.session_state.get('ready'):
    st.success("تم تجهيز الفيديو والصوت بجودة خام بنجاح! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'v_bytes' in st.session_state:
            st.download_button(
                label="تحميل الفيديو (MP4) 🎬",
                data=st.session_state['v_bytes'],
                file_name="tiktok_raw_video.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
    with col2:
        if 'm_bytes' in st.session_state:
            st.download_button(
                label="تحميل الصوت (MP3) 🎵",
                data=st.session_state['m_bytes'],
                file_name="tiktok_audio.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

st.markdown('<div class="custom-footer">إنشاء زايد</div>', unsafe_allow_html=True)
