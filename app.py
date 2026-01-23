import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS) ---
st.markdown("""
<style>
    /* GENEL AYARLAR */
    .stApp { background-color: #f8faff !important; }
    h1, h2 { color: #2e3b8e !important; text-align: center; font-weight: 800; font-family: sans-serif; }
    p, div, span { font-family: sans-serif; }

    /* --- ANA MENÜ BUTONLARI --- */
    /* Sol (Yeşil - Öğretim) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #22c55e !important; color: white !important; border: none; height: 140px; border-radius: 15px; box-shadow: 0 4px 10px rgba(34, 197, 94, 0.3);
    }
    /* Sağ (Mor - Sınav) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #a855f7 !important; color: white !important; border: none; height: 140px; border-radius: 15px; box-shadow: 0 4px 10px rgba(168, 85, 247, 0.3);
    }

    /* --- SEVİYE SEÇİM EKRANI ÖZEL BUTONLARI --- */
    
    /* Bu ekrandaki butonların genel yapısı */
    .level-btn-container button {
        width: 100%;
        border: none;
        border-radius: 15px;
        color: white !important;
        margin-bottom: 15px;
        transition: transform 0.2s;
        /* İçindeki metni düzenlemek için */
        white-space: pre-wrap !important; 
        line-height: 1.5 !important;
    }
    
    .level-btn-container button:hover {
        transform: scale(1.02);
        opacity: 0.95;
    }

    /* 1. Buton: KOLAY (Yeşil) - Sıra: Geri butonundan sonra gelir */
    /* Streamlit'te butonlar sırayla div.row-widget olarak gelir. */
    /* Geri butonu 1. sıradadır. Kolay 2., Orta 3., Zor 4. sıradadır. */

    div.row-widget.stButton:nth-of-type(2) button {
        background-color: #22c55e !important;
        height: 110px !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }
    
    div.row-widget.stButton:nth-of-type(3) button {
        background-color: #eab308 !important; /* Turuncu/Sarı */
        height: 110px !important;
        box-shadow: 0 4px 15px rgba(234, 179, 8, 0.3);
    }

    div.row-widget.stButton:nth-of-type(4) button {
        background-color: #ef4444 !important; /* Kırmızı */
        height: 110px !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }

    /* METİN BÜYÜKLÜĞÜ AYARI (Sihirli Kısım) */
    /* Buton içindeki ilk satırı (Başlığı) büyütür, kalanı küçük bırakır */
    div.row-widget.stButton button p::first-line {
        font-size: 26px !important;
        font-weight: 800 !important;
    }
    div.row-widget.stButton button p {
        font-size: 16px !important;
        font-weight: normal !important;
    }

    /* GERİ BUTONU ÖZELLEŞTİRMESİ */
    div.row-widget.stButton:nth-of-type(1) button {
        background-color: #e2e8f0 !important;
        color: #475569 !important;
        height: auto !important;
        padding: 8px 15px !important;
        width: auto !important;
        box-shadow: none !important;
    }
    div.row-widget.stButton:nth-of-type(1) button p::first-line {
        font-size: 16px !important; /* Geri butonu yazısı küçük kalsın */
        font-weight: normal !important;
    }

    /* KART STİLLERİ */
    .card { background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e0e7ff; margin-bottom: 20px; }
    .big-text { font-size: 50px; font-weight: bold; color: #1e293b; }
    
    .covered-box {
        background-color: #f1f5f9;
        background-image: repeating-linear-gradient(45deg, #e2e8f0, #e2e8f0 10px, #f1f5f9 10px, #f1f5f9 20px);
        padding: 20px; border-radius: 15px; border: 2px dashed #cbd5e1;
        text-align: center; margin-bottom: 20px; color: #94a3b8; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER ---
DIFFICULTY_LEVELS = {
    "Kolay": {
        "items": [
            {"q": "2 x 2", "a": 4}, {"q": "2 x 3", "a": 6}, {"q": "2 x 4", "a": 8}, {"q": "2 x 5", "a": 10},
            {"q": "3 x 3", "a": 9}, {"q": "3 x 4", "a": 12}, {"q": "3 x 5", "a": 15},
            {"q": "4 x 4", "a": 16}, {"q": "4 x 5", "a": 20}, {"q": "5 x 5", "a": 25}
        ],
        "desc": "2, 3, 4, 5 sayılarının birbirleriyle çarpımı"
    },
    "Orta": {
        "items": [
            {"q": "2 x 6", "a": 12}, {"q": "2 x 7", "a": 14}, {"q": "2 x 8", "a": 16}, {"q": "2 x 9", "a": 18},
            {"q": "3 x 6", "a": 18}, {"q": "3 x 7", "a": 21}, {"q": "3 x 8", "a": 24}, {"q": "3 x 9", "a": 27},
            {"q": "4 x 6", "a": 24}, {"q": "4 x 7", "a": 28}, {"q": "4 x 8", "a": 32}, {"q": "4 x 9", "a": 36}
        ],
        "desc": "2, 3, 4, 5 sayılarının 6, 7, 8, 9 ile çarpımı"
    },
    "Zor": {
        "items": [
            {"q": "6 x 6", "a": 36}, {"q": "6 x 7", "a": 42}, {"q": "6 x 8", "a": 48}, {"q": "6 x 9", "a": 54},
            {"q": "7 x 7", "a": 49}, {"q": "7 x 8", "a": 56}, {"q": "7 x 9", "a": 63},
            {"q": "8 x 8", "a": 64}, {"q": "8 x 9", "a": 72}, {"q": "9 x 9", "a": 81}
        ],
        "desc": "6, 7, 8, 9 sayılarının birbirleriyle çarpımı"
    }
}

# --- 4. YÖNETİCİ SINIFI ---
class CCCManager:
    def __init__(self):
        if 'init' not in st.session_state:
            self._reset_state()
            st.session_state['init'] = True

    def _reset_state(self):
        st.session_state.update({
            'phase': 'MENU',
            'difficulty': 'Kolay',
            'questions': [],
            'idx': 0,
            'step': 0,
            'score': 0,
            'opts': [],
            'error': False
        })

    def set_difficulty(self, level):
        q_list = DIFFICULTY_LEVELS[level]["items"].copy()
        random.shuffle(q_list)
        st.session_state.update({
            'difficulty': level,
            'questions': q_list,
            'idx': 0,
            'step': 0,
            'phase': 'LEARNING',
            'error': False
        })

    def gen_opts(self):
        current_q = st.session_state['questions'][st.session_state['idx']]
        correct = current_q['a']
        opts = {correct}
        while len(opts) < 3:
            fake = correct + random.randint(-5, 5)
            if fake > 0 and fake != correct: opts.add(fake)
        opt_list = list(opts)
        random.shuffle(opt_list)
        st.session_state['opts'] = opt_list

# --- 5. ANA UYGULAMA ---
def main():
    manager = CCCManager()
    phase = st.session_state['phase']

    # --- MENÜ ---
    if phase == 'MENU':
        st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b;'>Çarpım Tablosu Öğretimi</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="card"><h3>Hoş Geldin!</h3><p>Yapmak istediğin çalışmayı seç.</p></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📘\nÖğretim Modu\n(Adım Adım)", use_container_width=True):
                st.session_state['phase'] = 'LEVEL_SELECT'
                st.rerun()
        with c2:
            if st.button("🚀\nDeğerlendirme\n(Kendini Test Et)", use_container_width=True):
                all_q = [q for l in DIFFICULTY_LEVELS.values() for q in l["items"]]
                st.session_state.update({
                    'questions': random.sample(all_q, 10),
                    'idx': 0, 'score': 0, 'phase': 'ASSESSMENT'
                })
                manager.gen_opts()
                st.rerun()

    # --- SEVİYE SEÇİM EKRANI (GÖRSELDEKİ GİBİ) ---
    elif phase == 'LEVEL_SELECT':
        if st.button("← Ana Menü"):
            manager._reset_state()
            st.rerun()

        st.markdown("<h2>Zorluk Seviyesi Seç</h2>", unsafe_allow_html=True)
        st.write("") # Boşluk

        # Butonlar: Kolay, Orta, Zor
        # CSS'de nth-of-type ile renklendirildi
        
        if st.button(f"Kolay\n{DIFFICULTY_LEVELS['Kolay']['desc']}"):
            manager.set_difficulty("Kolay")
            st.rerun()
            
        if st.button(f"Orta\n{DIFFICULTY_LEVELS['Orta']['desc']}"):
            manager.set_difficulty("Orta")
            st.rerun()
            
        if st.button(f"Zor\n{DIFFICULTY_LEVELS['Zor']['desc']}"):
            manager.set_difficulty("Zor")
            st.rerun()

    # --- ÖĞRENME MODU ---
    elif phase == 'LEARNING':
        if st.button("← Seviye Seçimi"):
            st.session_state['phase'] = 'LEVEL_SELECT'
            st.rerun()

        # Hata Ekranı
        if st.session_state.get('error'):
            st.markdown("""
            <div class="card" style="border-color: #ef4444; background-color: #fef2f2;">
                <h2 style="color: #ef4444 !important;">❌ Yanlış Cevap</h2>
                <p>Kural gereği işlemi baştan incelemelisin.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Başa Dön ve Tekrar Dene", type="primary"):
                st.session_state['step'] = 0
                st.session_state['error'] = False
                st.rerun()
        
        # Normal Akış
        else:
            q = st.session_state['questions'][st.session_state['idx']]
            st.progress((st.session_state['idx']) / len(st.session_state['questions']))
            
            if st.session_state['step'] == 0: # GÖR
                st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = {q["a"]}</div></div>', unsafe_allow_html=True)
                if st.button("🙈 Kapat ve Cevapla", use_container_width=True):
                    manager.gen_opts()
                    st.session_state['step'] = 1
                    st.rerun()
            
            else: # KAPAT & SEÇ
                st.markdown('<div class="covered-box">🙈 CEVAP GİZLENDİ</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
                
                cols = st.columns(3)
                for i, opt in enumerate(st.session_state['opts']):
                    # Seçenek butonları için özel key kullanımı
                    if cols[i].button(str(opt), key=f"opt_{i}", use_container_width=True):
                        if opt == q['a']:
                            if st.session_state['idx'] < len(st.session_state['questions']) - 1:
                                st.session_state['idx'] += 1
                                st.session_state['step'] = 0
                            else:
                                st.session_state['phase'] = 'COMPLETED'
                        else:
                            st.session_state['error'] = True
                        st.rerun()

    # --- SINAV MODU ---
    elif phase == 'ASSESSMENT':
        if st.button("← Sınavdan Çık"):
            manager._reset_state()
            st.rerun()
            
        q = st.session_state['questions'][st.session_state['idx']]
        st.markdown(f"### Soru {st.session_state['idx'] + 1} / 10")
        st.markdown(f'<div class="card"><div class="big-text">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['opts']):
            if cols[i].button(str(opt), key=f"exam_{i}", use_container_width=True):
                if opt == q['a']: st.session_state['score'] += 1
                
                if st.session_state['idx'] < 9:
                    st.session_state['idx'] += 1
                    manager.gen_opts()
                else:
                    st.session_state['phase'] = 'COMPLETED'
                st.rerun()

    # --- TAMAMLANDI ---
    elif phase == 'COMPLETED':
        st.balloons()
        score = st.session_state.get('score', 0)
        
        # Sınav mı bitti, Öğrenme mi?
        if 'score' in st.session_state and st.session_state.get('phase_was_exam'):
             msg = f"Sınav Puanın: {score} / 10"
        else:
             msg = "Tebrikler! Seviyeyi tamamladın."

        st.markdown(f'<div class="card"><h2>🎉 Harika İş!</h2><h3>{msg}</h3></div>', unsafe_allow_html=True)
        
        if st.button("🏠 Ana Menüye Dön", use_container_width=True):
            manager._reset_state()
            st.rerun()

if __name__ == "__main__":
    main()
