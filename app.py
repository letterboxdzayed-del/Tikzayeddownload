import streamlit as st
import yt_dlp
import os
import tempfile

# إعدادات الصفحة
st.set_page_config(page_title="محمل تيك توك الاحترافي HD", page_icon="🔥", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #0a0a0a !important; }
    * { font-family: 'Tajawal', sans-serif !important; }
    .title-text {
        color: #D4AF37 !important; text-align: center; font-size: 32px !important; font-weight: 700 !important;
        text-shadow: 0 0 12px rgba(212, 175, 55, 0.25); margin-top: 15px; margin-bottom: 5px;
    }
    div[data-baseweb="input"] { background-color: #141414 !important; border-radius: 12px !important; }
    div[data-baseweb="input"]:focus-within { border-color: #D4AF37 !important; }
    input { color: #ffffff !important; }
    div.stButton > button {
        background-color: #D4AF37 !important; color: #000000 !important; border-radius: 12px !important;
        font-weight: 700 !important; padding: 12px 24px !important; width: 100% !important; margin-top: 10px !important;
    }
    div.stDownloadButton > button {
        border-radius: 12px !important; font-weight: 700 !important; width: 100% !important; margin-top: 10px !important;
    }
    div[data-testid="column"]:nth-child(1) div.stDownloadButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important; color: #000000 !important;
    }
    div[data-testid="column"]:nth-child(2) div.stDownloadButton > button {
        background: #1c1c1c !important; color: #D4AF37 !important; border: 1px solid #D4AF37 !important;
    }
</style>
""", unsafe_allow_html=True)

# دوال التحميل باستخدام yt-dlp
def download_media(url, media_type):
    temp_dir = tempfile.mkdtemp()
    
    if media_type == "video":
        # يسحب أعلى جودة متوفرة للفيديو والصوت ويدمجهم
        out_tmpl = os.path.join(temp_dir, 'video.%(ext)s')
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': out_tmpl,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }
    else:
        # يسحب أعلى جودة صوت ويحولها لـ MP3
        out_tmpl = os.path.join(temp_dir, 'audio.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': out_tmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if media_type == "video":
                file_path = os.path.join(temp_dir, 'video.mp4')
            else:
                file_path = os.path.join(temp_dir, 'audio.mp3')
                
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return f.read()
    except Exception as e:
        st.error(f"حدث خطأ أثناء سحب الملف: {e}")
        return None
    return None

# الواجهة
st.markdown('<div class="title-text">🔥 محمل تيك توك الخام (أعلى فريمات وجودة)</div>', unsafe_allow_html=True)

url_input = st.text_input("ضع رابط الفيديو هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الملف الأصلي 🚀"):
    if url_input:
        with st.spinner("جاري سحب الملف الأصلي من سيرفرات تيك توك بدون أي ضغط... ⏳"):
            # تصفير الجلسة
            st.session_state['v_bytes'] = None
            st.session_state['m_bytes'] = None
            
            # تحميل الفيديو
            v_data = download_media(url_input, "video")
            if v_data:
                st.session_state['v_bytes'] = v_data
                
            # تحميل الصوت
            m_data = download_media(url_input, "audio")
            if m_data:
                st.session_state['m_bytes'] = m_data
                
            if v_data or m_data:
                st.session_state['ready'] = True
            else:
                st.error("لم يتم العثور على وسائط صالحة أو الرابط غير صحيح.")
    else:
        st.warning("يرجى وضع رابط أولاً!")

# أزرار التحميل المباشرة
if st.session_state.get('ready'):
    st.success("تم سحب الملفات الأصلية بنجاح وبكامل سلاستها! 🎉")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('v_bytes'):
            st.download_button(
                label="تحميل الفيديو الخام 🎬",
                data=st.session_state['v_bytes'],
                file_name="Original_Video.mp4",
                mime="video/mp4",
                use_container_width=True
            )
            
    with col2:
        if st.session_state.get('m_bytes'):
            st.download_button(
                label="تحميل الصوت الأصلي 🎵",
                data=st.session_state['m_bytes'],
                file_name="Original_Audio.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )
