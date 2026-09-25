import streamlit as st
import yt_dlp
import os
import tempfile

# إعدادات الواجهة
st.set_page_config(page_title="المحمل الخارق HD", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505 !important; }
    * { font-family: 'Tajawal', sans-serif !important; }
    .title-text {
        color: #00f2fe !important; text-align: center; font-size: 30px !important; font-weight: 700 !important;
        margin-top: 10px; margin-bottom: 20px; text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
    }
    div[data-baseweb="input"] { background-color: #111 !important; border-radius: 10px !important; }
    div[data-baseweb="input"]:focus-within { border-color: #00f2fe !important; }
    input { color: #fff !important; }
    div.stButton > button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important; 
        color: #000 !important; border-radius: 10px !important; font-weight: 700 !important; 
        padding: 10px !important; width: 100% !important; border: none !important; margin-top: 10px !important;
    }
    div.stDownloadButton > button {
        background: #111 !important; color: #00f2fe !important; border: 1px solid #00f2fe !important;
        border-radius: 10px !important; font-weight: 700 !important; width: 100% !important; margin-top: 15px !important;
    }
    div.stDownloadButton > button:hover { background: #00f2fe !important; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

def get_raw_tiktok(url):
    """سحب الملف الأصلي كقطعة واحدة بدون أي معالجة أو دمج لتفادي التقطيع"""
    temp_dir = tempfile.mkdtemp()
    out_tmpl = os.path.join(temp_dir, 'video.mp4')
    
    ydl_opts = {
        'format': 'best',  # السطر السحري: يجلب أفضل جودة متوفرة كملف واحد جاهز
        'outtmpl': out_tmpl,
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            if os.path.exists(out_tmpl):
                with open(out_tmpl, 'rb') as f:
                    return f.read()
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        return None
    return None

st.markdown('<div class="title-text">⚡ محمل تيك توك الخام (سلاسة أصلية)</div>', unsafe_allow_html=True)

url_input = st.text_input("ضع رابط الفيديو هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو الأصلي 🚀"):
    if url_input:
        with st.spinner("جاري سحب الملف الخام مباشرة... ⏳"):
            raw_video = get_raw_tiktok(url_input)
            
            if raw_video:
                st.session_state['raw_video'] = raw_video
                st.session_state['ready'] = True
                st.success("تم سحب الفيديو بنجاح! جاهز للتحميل بكامل سلاسته.")
            else:
                st.error("تأكد من الرابط أو أن الحساب عام.")
    else:
        st.warning("الرجاء إدخال الرابط.")

if st.session_state.get('ready') and st.session_state.get('raw_video'):
    st.download_button(
        label="تحميل الفيديو 🎬 (MP4)",
        data=st.session_state['raw_video'],
        file_name="TikTok_Raw_60fps.mp4",
        mime="video/mp4",
        use_container_width=True
    )
