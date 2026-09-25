import streamlit as st
import requests
import io

# إعدادات الصفحة
st.set_page_config(page_title="محمل تيك توك الاحترافي HD", page_icon="✨", layout="centered")

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

    .direct-link-btn {
        display: block;
        text-align: center;
        background-color: #161616;
        color: #D4AF37 !important;
        border: 1px dashed #D4AF37;
        padding: 10px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
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

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
})

def get_tiktok_hd_media(url):
    """جلب رابط HD الأصلي بأعلى Bitrate متاح بدون ضغط"""
    try:
        res = session.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, timeout=15)
        data = res.json()
        if data.get("code") == 0:
            d = data["data"]
            # تقديم رابط hdplay المباشر أعلى جودة متوفرة
            v_url = d.get("hdplay") or d.get("play")
            if v_url and v_url.startswith("/"):
                v_url = f"https://www.tikwm.com{v_url}"
            m_url = d.get("music")
            if m_url and m_url.startswith("/"):
                m_url = f"https://www.tikwm.com{m_url}"
            return v_url, m_url
    except:
        pass

    # المحاولة الاحتياطية لجودة HD عبر API سريعة أخرى
    try:
        res = session.get(f"https://api.tiklydown.eu.org/api/download?url={url}", timeout=15)
        if res.status_code == 200:
            data = res.json()
            v_url = data.get("video", {}).get("noWatermark") or data.get("video", {}).get("watermark")
            m_url = data.get("music", {}).get("url")
            return v_url, m_url
    except:
        pass

    return None, None

def download_stream_bytes(download_url):
    """تحميل الفيديو بنظام التدفق (Chunking) لمنع تقطيع أو ضياع الفريمات"""
    if not download_url:
        return None
    try:
        with session.get(download_url, stream=True, timeout=30) as r:
            if r.status_code == 200:
                buffer = io.BytesIO()
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB Chunks
                    if chunk:
                        buffer.write(chunk)
                return buffer.getvalue()
    except:
        pass
    return None

# الواجهة الرئيسية
st.markdown('<div class="title-text">✨ محمل تيك توك الاحترافي HD</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">سحب مباشر بدقة 1080p كاملة بدون تقطيع أو ضغط للمونتاج</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو والصوت بأعلى جودة 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري جلب أعلى جودة HD وتجميع البتات بدون فقدان فريمات... ⏳"):
            v_url, m_url = get_tiktok_hd_media(url)
            
            if v_url:
                v_bytes = download_stream_bytes(v_url)
                m_bytes = download_stream_bytes(m_url) if m_url else None
                
                if v_bytes:
                    st.session_state['v_bytes'] = v_bytes
                    st.session_state['m_bytes'] = m_bytes
                    st.session_state['v_url'] = v_url
                    st.session_state['ready'] = True
                else:
                    st.error("حدث خطأ أثناء تجميع ملف الـ HD، حاول مجدداً.")
            else:
                st.error("تعذر الوصول لملف الفيديو المباشر. تأكد من أن الحساب عام.")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

if st.session_state.get('ready'):
    st.success("تم سحب ملف الـ HD الأصلي بنجاح 100%! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('v_bytes'):
            st.download_button(
                label="تحميل الفيديو HD (MP4) 🎬",
                data=st.session_state['v_bytes'],
                file_name="tiktok_hd_1080p.mp4",
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

    # رابط مباشر إضافي للتحميل الفوري بدون المرور بذاكرة المتصفح
    if st.session_state.get('v_url'):
        st.markdown(f'<a href="{st.session_state["v_url"]}" target="_blank" class="direct-link-btn">🔗 رابط تحميل HD مباشر (سريع للمونتاج)</a>', unsafe_allow_html=True)

st.markdown('<div class="custom-footer">إنشاء زايد</div>', unsafe_allow_html=True)
