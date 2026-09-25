import streamlit as st
import yt_dlp
import requests
import tempfile
import os

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

def download_raw_video(url):
    """سحب الفيديو الخام مباشرة من السيرفرات الرسمية بدون ضغط"""
    temp_dir = tempfile.gettempdir()
    v_path = os.path.join(temp_dir, f"video_raw_{os.urandom(4).hex()}.mp4")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': v_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return v_path
    except Exception as e:
        return None

def fetch_audio_fallback(url):
    """جلب الصوت كملف منفصل"""
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, timeout=15).json()
        if res.get("code") == 0 and res["data"].get("music"):
            m_url = res["data"]["music"]
            m_res = requests.get(m_url, timeout=30)
            if m_res.status_code == 200:
                return m_res.content
    except:
        pass
    return None

st.markdown('<div class="title-text">🔥 محمل زايد (الصوت والفيديو الأصلي)</div>', unsafe_allow_html=True)

url_input = st.text_input("ضع رابط الفيديو هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الملفات 🚀"):
    if url_input:
        with st.spinner("جاري الاتصال بسيرفرات تيك توك وسحب الملف الخام (قد يستغرق بعض الوقت بناءً على حجم الفيديو)... ⏳"):
            st.session_state['v_path'] = None
            st.session_state['m_bytes'] = None
            st.session_state['ready'] = False
            
            # سحب الفيديو الخام
            v_path = download_raw_video(url_input)
            
            if v_path and os.path.exists(v_path):
                st.session_state['v_path'] = v_path
                
                # سحب الصوت
                st.session_state['m_bytes'] = fetch_audio_fallback(url_input)
                
                st.session_state['ready'] = True
                
                # التحقق من الحجم لضمان النتيجة
                file_size_mb = os.path.getsize(v_path) / (1024 * 1024)
                st.success(f"✅ تم سحب الملف الأصلي بنجاح! (حجم الملف الحقيقي: {file_size_mb:.2f} MB)")
            else:
                st.error("❌ حدث خطأ أثناء سحب الملف الخام، يرجى التأكد من الرابط.")
    else:
        st.warning("الرجاء إدخال الرابط.")

# أزرار التحميل
if st.session_state.get('ready'):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('v_path') and os.path.exists(st.session_state['v_path']):
            with open(st.session_state['v_path'], "rb") as file:
                st.download_button(
                    label="تحميل الفيديو 🎬 (MP4)",
                    data=file,
                    file_name="Zayed_Raw_HD.mp4",
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
