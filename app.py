import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS) ---
st.markdown("""
<style>
    /* GENEL AYARLAR - Arka planı ve yazıları zorla beyaz/koyu yap */
    .stApp { background-color: #f8faff !important; }
    h1, h2, h3, p, span, div { font-family: 'Segoe UI', sans-serif; color: #1e293b; }
    h1 { color: #1e3a8a !important; text-align: center; font-weight: 800; }

    /* --- BUTON GENEL YAPISI --- */
    div.stButton > button {
        width: 100% !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        font-weight: bold !important;
        display: block !important;
        margin-bottom: 15px !important;
        padding: 20px !important;
        white-space: pre-wrap !important; /* Alt satıra geçmeye izin ver */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s !important;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02) !important;
        opacity: 0.95 !important;
    }

    /* --- BUTON İÇİ YAZI BOYUTLARI --- */
    /* İlk satırı (Örn: Kolay) BÜYÜK yap */
    div.stButton > button p {
        font-size: 28px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        color: white !important;
    }
    /* İkinci satırı (Açıklama) KÜÇÜK yap - Bu bir CSS hilesidir */
    div.stButton > button p::first-line {
        font-weight: 800 !important;
        font-size: 32px !important;
    }

    /* --- SEVİYE SEÇİM EKRANI RENKLERİ --- */
    
    /* 1. Buton: Geri Butonu (Gri) */
    /* Streamlit butonları sırayla dizer. Bu sayfadaki ilk buton 'Ana Menü' butonudur. */
    div.row-widget.stButton:nth-of-type(1) button {
        background-color: #e2e8f0 !important;
        color: #475569 !important;
        height: auto !important;
        width: auto !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
    }
    div.row-widget.stButton:nth-of-type(1) button p {
        color: #475569 !important;
        font-size: 16px !important;
    }
    div.row-widget.stButton:nth-of-type(1) button p::first-line {
        font-size: 16px !important;
        font-weight: bold !important;
    }

    /* 2. Buton: KOLAY (YEŞİL) */
    div.row-widget.stButton:nth-of-type(2) button {
        background-color: #22c55e !important; /* Canlı Yeşil */
        height: 120px !important;
        box-shadow: 0 10px 20px rgba(34, 197, 94, 0.3) !important;
    }

    /* 3. Buton: ORTA (SARI/TURUNCU) */
    div.row-widget.stButton:nth-of-type(3) button {
        background-color: #eab308 !important; /* Canlı Sarı */
        height: 120px !important;
        box-shadow: 0 10px 20px rgba(234, 179, 8, 0.3) !important;
    }

    /* 4. Buton: ZOR (KIRMIZI) */
    div.row-widget.stButton:nth-of-type(4) button {
        background-color: #ef4444 !important; /* Canlı Kırmızı */
        height: 120px !important;
        box-shadow: 0 10px 20px rgba(239, 68, 68, 0.3) !important;
    }

    /* --- ANA MENÜ ÖZEL AYARLARI (İki Kolonlu Yapı) --- */
    /* Sol Kolon Butonu (Öğretim) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #3b82f6 !important; /* Mavi */
        height: 150px !important;
    }
    /* Sağ Kolon Butonu (Sınav) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #8b5cf6 !important; /* Mor */
        height: 150px !important;
    }

    /* KART TASARIMI */
    .card { background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .big-text { font-size: 50px; font-weight: bold; color: #1e1b4b; }
    .covered-box { background-color: #f1f5f9; padding: 20px; border-radius: 15px; border: 2px dashed #cbd5e1; text-align: center; margin-bottom: 20px; color: #94a3b8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER ---
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
class CCCManager:
    def __init__(self):
        if 'init' not in st.session_state:
            self._reset()
            st.session_state['init'] = True

    def _reset(self):
        st.session_state.update({
            'phase': 'MENU',
            'difficulty': 'Kolay',
            'questions': [],
            'idx': 0, 'step': 0, 'score': 0, 'opts': [], 'error': False
        })

    def start_level(self, level):
        qs = DIFFICULTY_LEVELS[level]['q'].copy()
        random.shuffle(qs)
        st.session_state.update({
            'difficulty': level,
            'questions': qs,
            'idx': 0, 'step': 0, 'phase': 'LEARNING', 'error': False
        })

    def generate_options(self, correct):
        opts = {correct}
        while len(opts) < 3:
            f = correct + random.randint(-5, 5)
            if f > 0 and f != correct: opts.add(f)
        opt_list = list(opts)
        random.shuffle(opt_list)
        st.session_state['opts'] = opt_list

# --- 5. ANA UYGULAMA ---
def main():
    manager = CCCManager()
    phase = st.session_state['phase']

    # --- ANA MENÜ ---
    if phase == 'MENU':
        st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Çarpım Tablosu Öğretimi</p>", unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>Hoş Geldin!</h3><p>Yapmak istediğin çalışmayı seç.</p></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📘\nÖğretim Modu\n(Adım Adım)"): 
                st.session_state['phase'] = 'LV_SELECT'
                st.rerun()
        with c2:
            if st.button("🚀\nSınav Modu\n(Kendini Test Et)"):
                all_q = [q for l in DIFFICULTY_LEVELS.values() for q in l['q']]
                st.session_state.update({'questions': random.sample(all_q, 10), 'idx': 0, 'score': 0, 'phase': 'ASSESSMENT'})
                manager.generate_options(st.session_state['questions'][0]['a'])
                st.rerun()

    # --- SEVİYE SEÇİM EKRANI (RENKLİ BUTONLAR) ---
    elif phase == 'LV_SELECT':
        # 1. Buton: Geri
        if st.button("← Ana Menü"):
            manager._reset()
            st.rerun()

        st.markdown("<h2>Zorluk Seviyesi Seç</h2>", unsafe_allow_html=True)
        st.write("") # Boşluk

        # 2. Buton: Kolay (Yeşil)
        if st.button(f"Kolay\n{DIFFICULTY_LEVELS['Kolay']['desc']}"):
            manager.start_level("Kolay")
            st.rerun()
            
        # 3. Buton: Orta (Sarı)
        if st.button(f"Orta\n{DIFFICULTY_LEVELS['Orta']['desc']}"):
            manager.start_level("Orta")
            st.rerun()
            
        # 4. Buton: Zor (Kırmızı)
        if st.button(f"Zor\n{DIFFICULTY_LEVELS['Zor']['desc']}"):
            manager.start_level("Zor")
            st.rerun()

    # --- ÖĞRENME MODU ---
    elif phase == 'LEARNING':
        # Geri Butonu
        if st.button("← Seviye Seçimi"):
            st.session_state['phase'] = 'LV_SELECT'
            st.rerun()

        if st.session_state.get('error'):
            st.markdown('<div class="card" style="border-color: #ef4444; background-color: #fef2f2;"><h2 style="color: #ef4444 !important;">❌ Yanlış Cevap</h2><p>İşlemi baştan incelemelisin.</p></div>', unsafe_allow_html=True)
            if st.button("🔄 Başa Dön"):
                st.session_state['step'] = 0
                st.session_state['error'] = False
                st.rerun()
        else:
            q = st.session_state['questions'][st.session_state['idx']]
            st.progress((st.session_state['idx']) / len(st.session_state['questions']))

            if st.session_state['step'] == 0: # GÖR
                st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = {q["a"]}</div></div>', unsafe_allow_html=True)
                if st.button("🙈 Kapat ve Cevapla"):
                    manager.generate_options(q['a'])
                    st.session_state['step'] = 1
                    st.rerun()
            else: # KAPAT & SEÇ
                st.markdown('<div class="covered-box">🙈 CEVAP GİZLENDİ</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
                cols = st.columns(3)
                for i, opt in enumerate(st.session_state['opts']):
                    if cols[i].button(str(opt), key=f"op_{i}"):
                        if opt == q['a']:
                            if st.session_state['idx'] < len(st.session_state['questions']) - 1:
                                st.session_state['idx'] += 1
                                st.session_state['step'] = 0
                            else: st.session_state['phase'] = 'COMPLETED'
                        else: st.session_state['error'] = True
                        st.rerun()

    # --- SINAV MODU ---
    elif phase == 'ASSESSMENT':
        if st.button("← Sınavdan Çık"):
            manager._reset()
            st.rerun()
        q = st.session_state['questions'][st.session_state['idx']]
        st.markdown(f"### Soru {st.session_state['idx'] + 1} / 10")
        st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['opts']):
            if cols[i].button(str(opt), key=f"ex_{i}"):
                if opt == q['a']: st.session_state['score'] += 1
                if st.session_state['idx'] < 9:
                    st.session_state['idx'] += 1
                    manager.generate_options(st.session_state['questions'][st.session_state['idx']]['a'])
                else: st.session_state['phase'] = 'COMPLETED'
                st.rerun()

    # --- TAMAMLANDI ---
    elif phase == 'COMPLETED':
        st.balloons()
        st.markdown('<div class="card"><h2>🎉 Tebrikler!</h2><p>Harika bir iş çıkardın.</p></div>', unsafe_allow_html=True)
        if st.button("🏠 Ana Menüye Dön"):
            manager._reset()
            st.rerun()

if __name__ == "__main__":
    main()
