import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="محمل تيك توك", page_icon="✨", layout="centered")

# تنسيق CSS احترافي باللون الذهبي والداكن
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

    /* خلفية الصفحة الأساسية */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* إخفاء قوائم ستريملت */
    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* توحيد الخط لكافة العناصر */
    * {
        font-family: 'Tajawal', 'GS Pro', sans-serif !important;
    }

    /* العنوان الرئيسي */
    .title-text {
        color: #D4AF37 !important;
        text-align: center;
        font-size: 34px !important;
        font-weight: 700 !important;
        margin-top: 10px;
        margin-bottom: 5px;
        text-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
    }

    /* الوصف الفرعي */
    .subtitle-text {
        color: #a0a0a0 !important;
        text-align: center;
        font-size: 15px !important;
        margin-bottom: 30px;
    }

    /* نص خانة الإدخال */
    label[data-testid="stWidgetLabel"] p {
        color: #e0e0e0 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    /* مربع إدخال الرابط */
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

    /* زر استخراج الفيديو */
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
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }

    /* زر تحميل الفيديو المباشر الذهبي */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #000000 !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.25) !important;
        transition: all 0.3s ease !important;
        margin-top: 15px !important;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(212, 175, 55, 0.45) !important;
        color: #000000 !important;
    }

    /* الحقوق في الأسفل */
    .custom-footer {
        text-align: center;
        color: #444444 !important;
        font-size: 13px !important;
        margin-top: 60px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ترويسة محاكاة المتصفح لمنع تقليص الجودة والتقطيع
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

def get_tiktok_video_url(url):
    full_url = expand_tiktok_url(url)
    
    # السحب بجودة HD عالية
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": full_url, "hd": 1}, headers=HEADERS, timeout=15)
        data = res.json()
        if data.get("code") == 0:
            play = data["data"].get("hdplay") or data["data"].get("play")
            if play:
                return f"https://www.tikwm.com{play}" if play.startswith("/") else play
    except:
        pass
        
    # سيرفر احتياطي لجودة عالية
    try:
        res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={full_url}", headers=HEADERS, timeout=15)
        data = res.json()
        if "video" in data:
            return data["video"].get("noWatermark") or data["video"].get("watermark")
    except:
        pass
    return None

# الواجهة
st.markdown('<div class="title-text">✨ محمل تيك توك</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">أعلى جودة، بدون علامة مائية، وبدون حدود للحجم</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو 🚀"):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري جلب الفيديو بأعلى جودة وتثبيت الصوت... ⏳"):
            video_url = get_tiktok_video_url(url)
            if video_url:
                try:
                    # تجميع أجزاء الفيديو لمنع التعليق وتزامن الصوت
                    video_res = requests.get(video_url, headers=HEADERS, stream=True, timeout=40)
                    if video_res.status_code == 200:
                        video_bytes = bytearray()
                        for chunk in video_res.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_bytes.extend(chunk)
                        
                        st.session_state['video_data'] = bytes(video_bytes)
                        st.session_state['ready'] = True
                    else:
                        st.error("تعذر تحميل ملف الفيديو من سيرفر المصدر. ❌")
                except Exception:
                    st.error("حدث خطأ أثناء الاتصال بالسيرفر. حاول مجدداً. ❌")
            else:
                st.error("عذراً، السيرفر يرفض الرابط أو الحساب خاص. ❌")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")

# زر التنزيل عند اكتمال جلب كافة أجزاء الفيديو بنجاح
if st.session_state.get('ready'):
    st.success("تم تجهيز الفيديو بنجاح! 🎉")
    st.download_button(
        label="تحميل الفيديو الآن 📥",
        data=st.session_state['video_data'],
        file_name="tiktok_hd_video.mp4",
        mime="video/mp4",
        use_container_width=True
    )

# الحقوق في الأسفل
st.markdown('<div class="custom-footer">إنشاء زايد</div>', unsafe_allow_html=True)
