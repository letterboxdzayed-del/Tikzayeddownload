import streamlit as st
import requests

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="محمل تيك توك | زايد", page_icon="✨", layout="centered")

# كود CSS إجباري لكسر إعدادات ستريملت الافتراضية
st.markdown("""
<style>
    /* استدعاء خط تجوال الرسمي من جوجل */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    
    /* إجبار الخلفية على اللون الأسود الليلي المخملي */
    [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    /* إجبار جميع النصوص على استخدام تجوال أو GS Pro */
    html, body, [class*="css"], div, p, span, h1, h2, h3, input, button {
        font-family: 'GE SS Two', 'GS Pro', 'Tajawal', sans-serif !important;
    }
    
    /* إخفاء القائمة العلوية وعلامة ستريملت المائية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تصميم العنوان الفخم باللون الذهبي الحقيقي */
    .title-text {
        color: #D4AF37 !important;
        text-align: center;
        font-size: 40px !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        color: #888888 !important;
        text-align: center;
        font-size: 16px !important;
        margin-bottom: 40px;
    }
    
    /* تصميم زر التحميل الذهبي */
    .gold-btn {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        padding: 15px 35px;
        border-radius: 10px;
        text-align: center;
        display: block;
        font-size: 22px !important;
        font-weight: bold !important;
        text-decoration: none;
        margin: 20px auto;
        width: fit-content;
        border: 2px solid #D4AF37;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease-in-out;
    }
    .gold-btn:hover {
        background-color: transparent !important;
        color: #D4AF37 !important;
        box-shadow: 0 6px 25px rgba(212, 175, 55, 0.6);
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# دوال سحب الفيديو
def expand_tiktok_url(url: str):
    if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
        try:
            res = requests.head(url, allow_redirects=True, timeout=10)
            return str(res.url)
        except:
            pass
    return url

def get_tiktok_video_url(url):
    full_url = expand_tiktok_url(url)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.post("https://www.tikwm.com/api/", data={"url": full_url, "hd": 1}, headers=headers, timeout=15)
        data = res.json()
        if data.get("code") == 0:
            play = data["data"].get("hdplay") or data["data"].get("play")
            if play:
                return f"https://www.tikwm.com{play}" if play.startswith("/") else play
    except:
        pass
        
    try:
        res = requests.get(f"https://api.tiklydown.eu.org/api/download?url={full_url}", timeout=15)
        data = res.json()
        if "video" in data:
            return data["video"]["noWatermark"]
    except:
        pass
    return None

# واجهة المستخدم
st.markdown('<div class="title-text">✨ محمل تيك توك الملكي</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">أعلى جودة، بدون علامة مائية، وبدون حدود للحجم - برمجة زايد</div>', unsafe_allow_html=True)

url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://vm.tiktok.com/...")

if st.button("استخراج الفيديو 🚀", use_container_width=True):
    if url and "tiktok" in url.lower():
        with st.spinner("جاري سحب الفيديو بأعلى جودة... ⏳"):
            video_url = get_tiktok_video_url(url)
            
            if video_url:
                st.success("تم تجهيز الفيديو بنجاح! 🎉")
                st.markdown(f'<a href="{video_url}" target="_blank" class="gold-btn">تحميل الفيديو الآن 📥</a>', unsafe_allow_html=True)
            else:
                st.error("عذراً، السيرفر يرفض الرابط أو الحساب خاص. ❌")
    else:
        st.warning("الرجاء إدخال رابط تيك توك صحيح! 🔗")
