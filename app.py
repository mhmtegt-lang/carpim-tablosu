import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS) ---
# Görseldeki (image_ca9308.png) buton tasarımını ve aydınlık temayı zorunlu kılan CSS
st.markdown("""
<style>
    /* Ana Arka Planı Beyaz Yap */
    .stApp { background-color: #f8faff !important; }
    
    /* Tüm Yazıları Okunabilir Kıl */
    h1, h2, h3, p, span, div { color: #1e293b !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1 { text-align: center; font-weight: 800; color: #312e81 !important; }

    /* --- BUTONLARIN GÖRSELDEKİ GİBİ OLMASI İÇİN ÖZEL CSS --- */
    
    /* Tüm butonların temel yapısı */
    div.stButton > button {
        width: 100% !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        font-weight: bold !important;
        display: block !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        margin-bottom: 15px !important;
        padding: 20px !important;
        white-space: pre-wrap !important; /* Alt satıra geçmeye izin ver */
    }

    div.stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Buton Başlık ve Açıklama Boyutları */
    div.stButton > button p {
        font-size: 28px !important; /* Başlık boyutu */
        margin: 0 !important;
        color: white !important;
        line-height: 1.2 !important;
    }
    div.stButton > button p::after {
        content: attr(data-desc); /* Not: Bu simülasyon amaçlıdır, asıl metin \n ile ayrılır */
        font-size: 16px !important;
        font-weight: normal !important;
        display: block;
        margin-top: 5px;
    }

    /* --- RENK ATAMALARI (image_ca9308.png) --- */
    
    /* Kolay (Yeşil) */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) div.stButton > button {
        background-color: #22c55e !important; /* Vibrant Green */
    }
    
    /* Orta (Sarı/Turuncu) */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) div.stButton > button {
        background-color: #eab308 !important; /* Vibrant Yellow */
    }
    
    /* Zor (Kırmızı) */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton > button {
        background-color: #ef4444 !important; /* Vibrant Red */
    }

    /* Geri Butonu (Küçük ve Gri) */
    div.stButton > button[key="back"] {
        background-color: #e2e8f0 !important;
        color: #475569 !important;
        height: auto !important;
        width: auto !important;
        padding: 8px 15px !important;
        font-size: 14px !important;
    }

    /* --- KART VE GİZLİ ALAN --- */
    .card { background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .big-text { font-size: 50px; font-weight: bold; color: #1e1b4b; }
    .covered-area { background-color: #f1f5f9; padding: 30px; border-radius: 20px; border: 3px dashed #cbd5e1; text-align: center; margin-bottom: 20px; color: #94a3b8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER (KAYNAK: TABLO 3.1) ---
DIFFICULTY_LEVELS = {
    "Kolay": {
        "q": [
            {"q": "2 x 2", "a": 4}, {"q": "2 x 3", "a": 6}, {"q": "2 x 4", "a": 8}, {"q": "2 x 5", "a": 10},
            {"q": "3 x 3", "a": 9}, {"q": "3 x 4", "a": 12}, {"q": "3 x 5", "a": 15},
            {"q": "4 x 4", "a": 16}, {"q": "4 x 5", "a": 20}, {"q": "5 x 5", "a": 25}
        ],
        "desc": "2, 3, 4, 5 sayılarının birbirleriyle çarpımı"
    },
    "Orta": {
        "q": [
            {"q": "2 x 6", "a": 12}, {"q": "2 x 7", "a": 14}, {"q": "2 x 8", "a": 16}, {"q": "2 x 9", "a": 18},
            {"q": "3 x 6", "a": 18}, {"q": "3 x 7", "a": 21}, {"q": "3 x 8", "a": 24}, {"q": "3 x 9", "a": 27},
            {"q": "4 x 6", "a": 24}, {"q": "4 x 7", "a": 28}, {"q": "4 x 8", "a": 32}, {"q": "4 x 9", "a": 36}
        ],
        "desc": "2, 3, 4, 5 sayılarının 6, 7, 8, 9 ile çarpımı"
    },
    "Zor": {
        "q": [
            {"q": "6 x 6", "a": 36}, {"q": "6 x 7", "a": 42}, {"q": "6 x 8", "a": 48}, {"q": "6 x 9", "a": 54},
            {"q": "7 x 7", "a": 49}, {"q": "7 x 8", "a": 56}, {"q": "7 x 9", "a": 63},
            {"q": "8 x 8", "a": 64}, {"q": "8 x 9", "a": 72}, {"q": "9 x 9", "a": 81}
        ],
        "desc": "6, 7, 8, 9 sayılarının birbirleriyle çarpımı"
    }
}

# --- 4. LOGIC MANAGER ---
class CCCLogic:
    def __init__(self):
        if 'init_state' not in st.session_state:
            self._reset()
            st.session_state['init_state'] = True

    def _reset(self):
        st.session_state.update({
            'phase': 'MENU', # MENU, LV_SELECT, LEARNING, ASSESSMENT, COMPLETED
            'difficulty': 'Kolay',
            'questions': [],
            'idx': 0,
            'step': 0, # 0: Look, 1: Cover/Write
            'score': 0,
            'options': [],
            'wrong_ans': False
        })

    def start_level(self, level):
        qs = DIFFICULTY_LEVELS[level]['q'].copy()
        random.shuffle(qs)
        st.session_state.update({
            'difficulty': level,
            'questions': qs,
            'idx': 0, 'step': 0, 'phase': 'LEARNING', 'wrong_ans': False
        })

    def generate_options(self, correct):
        opts = {correct}
        while len(opts) < 3:
            f = correct + random.randint(-5, 5)
            if f > 0 and f != correct: opts.add(f)
        opt_list = list(opts)
        random.shuffle(opt_list)
        st.session_state['options'] = opt_list

# --- 5. ANA UYGULAMA ---
def main():
    app = CCCLogic()
    p = st.session_state['phase']

    # --- ANA MENÜ ---
    if p == 'MENU':
        st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>Başlamak İçin Bir Mod Seç</h3></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📘 Öğretim Modu"): 
                st.session_state['phase'] = 'LV_SELECT'
                st.rerun()
        with c2:
            if st.button("🚀 Sınav Modu"):
                all_q = [q for l in DIFFICULTY_LEVELS.values() for q in l['q']]
                st.session_state.update({
                    'questions': random.sample(all_q, 10),
                    'idx': 0, 'score': 0, 'phase': 'ASSESSMENT'
                })
                app.generate_options(st.session_state['questions'][0]['a'])
                st.rerun()

    # --- SEVİYE SEÇİMİ (ZORUNLU GÖRÜNÜM) ---
    elif p == 'LV_SELECT':
        st.button("← Ana Menü", key="back", on_click=lambda: app._reset())
        st.markdown("<h2 style='text-align: center;'>Zorluk Seviyesi Seç</h2>", unsafe_allow_html=True)
        
        # image_ca9308.png tasarımı
        if st.button(f"Kolay\n{DIFFICULTY_LEVELS['Kolay']['desc']}", key="btn_k"):
            app.start_level("Kolay")
            st.rerun()
        if st.button(f"Orta\n{DIFFICULTY_LEVELS['Orta']['desc']}", key="btn_o"):
            app.start_level("Orta")
            st.rerun()
        if st.button(f"Zor\n{DIFFICULTY_LEVELS['Zor']['desc']}", key="btn_z"):
            app.start_level("Zor")
            st.rerun()

    # --- ÖĞRENME MODU (KKK STRATEJİSİ) ---
    elif p == 'LEARNING':
        st.button("← Seviyeler", key="back", on_click=lambda: st.session_state.update({'phase': 'LV_SELECT'}))
        q = st.session_state['questions'][st.session_state['idx']]
        st.progress(st.session_state['idx'] / len(st.session_state['questions']))

        if st.session_state['step'] == 0: # BAK VE OKU [cite: 6, 13]
            st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = {q["a"]}</div></div>', unsafe_allow_html=True)
            if st.session_state['wrong_ans']: st.error("⚠️ Yanlış cevap! Başa döndük, tekrar oku. ")
            if st.button("🙈 Kapat ve Cevapla", use_container_width=True):
                app.generate_options(q['a'])
                st.session_state['step'] = 1
                st.rerun()
        else: # KAPAT VE YAZ [cite: 7, 8, 14]
            st.markdown('<div class="covered-area">🙈 CEVAP GİZLENDİ</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, opt in enumerate(st.session_state['options']):
                if cols[i].button(str(opt), key=f"opt_{i}"):
                    if opt == q['a']: # KARŞILAŞTIR (DOĞRU) [cite: 9, 15, 16]
                        if st.session_state['idx'] < len(st.session_state['questions']) - 1:
                            st.session_state['idx'] += 1
                            st.session_state['step'] = 0
                            st.session_state['wrong_ans'] = False
                        else: st.session_state['phase'] = 'COMPLETED'
                    else: # KARŞILAŞTIR (YANLIŞ) -> BAŞA DÖN 
                        st.session_state['step'] = 0
                        st.session_state['wrong_ans'] = True
                    st.rerun()

    # --- SINAV VE TAMAMLANMA ---
    elif p == 'ASSESSMENT':
        st.button("← Çıkış", key="back", on_click=lambda: app._reset())
        q = st.session_state['questions'][st.session_state['idx']]
        st.markdown(f"### Soru {st.session_state['idx'] + 1} / 10")
        st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['options']):
            if cols[i].button(str(opt), key=f"ex_{i}"):
                if opt == q['a']: st.session_state['score'] += 1
                if st.session_state['idx'] < 9:
                    st.session_state['idx'] += 1
                    app.generate_options(st.session_state['questions'][st.session_state['idx']]['a'])
                else: st.session_state['phase'] = 'COMPLETED'
                st.rerun()

    elif p == 'COMPLETED':
        st.balloons()
        st.markdown('<div class="card"><h2>🎉 Harika! Bitirdik.</h2></div>', unsafe_allow_html=True)
        if st.button("🏠 Ana Menüye Dön", use_container_width=True): app._reset(); st.rerun()

if __name__ == "__main__":
    main()
