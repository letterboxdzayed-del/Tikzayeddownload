import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="محمل تيك توك", page_icon="✨", layout="centered")

# CSS لتصميم فخم وداكن مع أزرار التحميل
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0px !important;
    }

    * {
        font-family: 'Tajawal', 'GS Pro', sans-serif !important;
    }

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

    /* زر استخراج */
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
    
    /* زر تنزيل الفيديو MP4 */
    div[data-testid="column"]:nth-child(1) div.stDownloadButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important;
    }

    /* زر تنزيل الصوت MP3 */
    div[data-testid="column"]:nth-child(2) div.stDownloadButton > button {
        background: #1f1f1f !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }

    /* الحقوق */
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.tiktok.com/"
}

def expand_tiktok_url(url: str):
    if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
        try:
            res = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=10)
            return str(res.url)
        except:
            pass
    return url

def fetch_tiktok_data(url):
    full_url = expand_tiktok_url(url)
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": full_url, "hd": 1}, headers=HEADERS, timeout=15)
        data = res.json()
        if data.get("code") == 0:
            d = data["data"]
            # استخدام الرابط الأصلي المباشر لمنع تقطيع الإطارات
            video_url = d.get("play") or d.get("hdplay")
            if video_url and video_url.startswith("/"):
                video_url = f"https://www.tikwm.com{video_url}"
            
            music_url = d.get("music") or (d.get("music_info") or {}).get("play")
            if music_url and music_url.startswith("/"):
                music_url = f"https://www.tikwm.com{music_url}"
                
            return video_url, music_url
    except:
        pass
    
    # سيرفر احتياطي
    try:
        res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={full_url}", headers=HEADERS, timeout=15)
        data = res.json()
        video_url = data.get("video", {}).get("noWatermark")
        music_url = data.get("music", {}).get("url")
        return video_url, music_url
    except:
        pass

    return None, None

# الواجهة
st.markdown('<div class="title-text">✨ محمل تيك توك</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">أعلى جودة، بدون علامة مائية، وبدون تقطيع</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو والصوت 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري جلب الملف الأصلي وسلسلة الإطارات... ⏳"):
            video_url, music_url = fetch_tiktok_data(url)
            
            if video_url:
                try:
                    # جلب كائن الملف كاملاً بمرة واحدة لضمان سلاسة الحركة 100%
                    v_res = requests.get(video_url, headers=HEADERS, timeout=30)
                    if v_res.status_code == 200:
                        st.session_state['v_bytes'] = v_res.content
                    
                    if music_url:
                        m_res = requests.get(music_url, headers=HEADERS, timeout=30)
                        if m_res.status_code == 200:
                            st.session_state['m_bytes'] = m_res.content
                    
                    st.session_state['ready'] = True
                except Exception:
                    st.error("حدث خطأ أثناء تحميل الملفات. حاول مجدداً. ❌")
            else:
                st.error("عذراً، تعذر سحب الرابط أو الفيديو من حساب خاص. ❌")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

# إظهار خيارات التحميل للفيديو والصوت عند جاهزيتها
if st.session_state.get('ready'):
    st.success("تم تجهيز الفيديو والصوت بنجاح! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'v_bytes' in st.session_state:
            st.download_button(
                label="تحميل الفيديو (MP4) 🎬",
                data=st.session_state['v_bytes'],
                file_name="tiktok_video.mp4",
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
