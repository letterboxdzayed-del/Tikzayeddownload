import streamlit as st
import yt_dlp
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
    input {
        color: #ffffff !important;
        background-color: transparent !important;
    }

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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.tiktok.com/"
}

def extract_original_tiktok(tiktok_url):
    """استخراج رابط الفيديو والصوت المباشر من سيرفرات تيك توك الرسمية مباشرة"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo+bestaudio/best',
        'check_formats': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(tiktok_url, download=False)
        video_direct_url = info.get('url')
        
        # البحث عن ملف الصوت المستقل
        audio_direct_url = None
        formats = info.get('formats', [])
        for f in formats:
            if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                audio_direct_url = f.get('url')
                break
        
        if not audio_direct_url:
            audio_direct_url = video_direct_url

        return video_direct_url, audio_direct_url

# الواجهة الرئيسيّة
st.markdown('<div class="title-text">✨ محمل تيك توك الاحترافي</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">سحب مباشر من سيرفرات تيك توك الرسمية (سلاسة كاملة للمونتاج)</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو والصوت 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري سحب الملف الأصلي مباشرة من تيك توك... ⏳"):
            try:
                v_url, a_url = extract_original_tiktok(url)
                
                # جلب بتات الفيديو الخام
                v_res = requests.get(v_url, headers=HEADERS, timeout=30)
                if v_res.status_code == 200:
                    st.session_state['v_bytes'] = v_res.content
                    
                # جلب بتات الصوت
                a_res = requests.get(a_url, headers=HEADERS, timeout=30)
                if a_res.status_code == 200:
                    st.session_state['m_bytes'] = a_res.content
                    
                st.session_state['ready'] = True
            except Exception as e:
                st.error("تعذر سحب الفيديو الأصلي. تأكد من صحة الرابط أو جرب رابطاً آخر.")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

if st.session_state.get('ready'):
    st.success("تم سحب الملف الأصلي 100% بنجاح وبدون أي تقطيع! 🎉")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'v_bytes' in st.session_state:
            st.download_button(
                label="تحميل الفيديو الأصلي (MP4) 🎬",
                data=st.session_state['v_bytes'],
                file_name="tiktok_original.mp4",
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
