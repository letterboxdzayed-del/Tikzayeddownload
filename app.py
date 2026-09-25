import streamlit as st
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

def fetch_tiktok_urls(url):
    """جلب الروابط عبر سيرفرين لضمان أفضل جودة وفريمات"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    # المحاولة الأولى: سيرفر TiklyDown (يحافظ غالباً على 60fps)
    try:
        res1 = requests.get(f"https://api.tiklydown.eu.org/api/download?url={url}", headers=headers, timeout=15).json()
        if "video" in res1 and "noWatermark" in res1["video"]:
            return res1["video"]["noWatermark"], res1.get("music", {}).get("play_url")
    except:
        pass
        
    # المحاولة الثانية: سيرفر TikWM (احتياطي)
    try:
        res2 = requests.post("https://www.tikwm.com/api/", data={"url": url, "hd": 1}, headers=headers, timeout=15).json()
        if res2.get("code") == 0:
            v_url = res2["data"].get("hdplay") or res2["data"].get("play")
            return v_url, res2["data"].get("music")
    except:
        pass
        
    return None, None

def download_to_temp(url, is_video=True):
    """تحميل الملف وحفظه في مسار مؤقت لضمان عدم تلف الفريمات"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    
    if is_video:
        suffix = ".mp4"
    else:
        suffix = ".mp3"
        
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            temp_file.write(chunk)
    temp_file.close()
    return temp_file.name

st.markdown('<div class="title-text">🔥 محمل زايد (الصوت والفيديو الأصلي)</div>', unsafe_allow_html=True)

url_input = st.text_input("ضع رابط الفيديو هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الملفات 🚀"):
    if url_input:
        with st.spinner("جاري سحب الجودة الأصلية بكامل الفريمات... ⏳"):
            st.session_state['v_path'] = None
            st.session_state['m_path'] = None
            st.session_state['ready'] = False
            
            v_url, m_url = fetch_tiktok_urls(url_input)
            
            if v_url:
                try:
                    # سحب الفيديو
                    st.session_state['v_path'] = download_to_temp(v_url, is_video=True)
                    
                    # التحقق من حجم الفيديو
                    file_size = os.path.getsize(st.session_state['v_path'])
                    if file_size < 2000000:
                        st.warning("⚠️ الفيديو مسحوب بحجم صغير، السيرفرات حالياً تطبق ضغطاً إجبارياً على هذا المقطع.")
                    else:
                        st.success("✅ تم سحب الملفات بنجاح بكامل الفريمات وبدون تقطيع!")
                        
                    # سحب الصوت
                    if m_url:
                        st.session_state['m_path'] = download_to_temp(m_url, is_video=False)
                            
                    st.session_state['ready'] = True
                except Exception as e:
                    st.error("حدث خطأ أثناء تحميل البيانات، جرب مرة ثانية.")
            else:
                st.error("❌ تأكد من الرابط أو أن الحساب عام.")
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
                    file_name="Video_Raw_HD.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            
    with col2:
        if st.session_state.get('m_path') and os.path.exists(st.session_state['m_path']):
            with open(st.session_state['m_path'], "rb") as file:
                st.download_button(
                    label="تحميل الصوت 🎵 (MP3)",
                    data=file,
                    file_name="Audio_Original.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )
