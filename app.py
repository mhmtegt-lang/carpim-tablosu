import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu Öğretimi", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS) ---
# Görseldeki (image_1d836f.png) renkleri ve buton büyüklüklerini birebir yansıtır.
st.markdown("""
<style>
    .stApp { background-color: #f8faff; }
    h1, h2 { color: #2e3b8e !important; text-align: center; font-weight: 800; }
    
    /* Seviye Seçim Butonları Tasarımı */
    .level-container { margin-bottom: 20px; }
    
    /* Genel Buton Ayarları */
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        border: none;
        color: white !important;
        font-weight: bold;
        display: block;
        transition: transform 0.2s;
        margin-bottom: 10px;
    }
    div.stButton > button:hover { transform: scale(1.02); }
    div.stButton > button p { font-size: 24px !important; margin-bottom: 0px; color: white !important; }
    .btn-desc { font-size: 16px; font-weight: normal; opacity: 0.9; }

    /* Kolay (Yeşil) */
    .kolay-btn button { background-color: #24c85f !important; height: 120px !important; box-shadow: 0 4px 15px rgba(36, 200, 95, 0.3); }
    /* Orta (Turuncu) */
    .orta-btn button { background-color: #f1b305 !important; height: 120px !important; box-shadow: 0 4px 15px rgba(241, 179, 5, 0.3); }
    /* Zor (Kırmızı) */
    .zor-btn button { background-color: #f14444 !important; height: 120px !important; box-shadow: 0 4px 15px rgba(241, 68, 68, 0.3); }

    /* KKK Kart Stilleri */
    .card { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e0e7ff; margin-bottom: 20px; }
    .big-font { font-size: 48px !important; font-weight: bold; color: #1e293b; }
    .covered-box { background-color: #e0f2fe; padding: 20px; border-radius: 15px; border: 2px dashed #7dd3fc; text-align: center; margin-bottom: 20px; }
    
    /* Geri Butonu Stili */
    .back-btn button { background-color: #f1f5f9 !important; color: #475569 !important; border: 1px solid #cbd5e1 !important; height: 40px !important; font-size: 14px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER (KAYNAK: TABLO 3.1) ---
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

# --- 4. LOGIC MANAGER ---
class CCCApp:
    def __init__(self):
        if 'init' not in st.session_state:
            self._reset_state()
            st.session_state['init'] = True

    def _reset_state(self):
        st.session_state.update({
            'phase': 'MENU', # MENU, LEVEL_SELECT, LEARNING, ASSESSMENT, ERROR, COMPLETED
            'difficulty': 'Kolay',
            'questions': [],
            'idx': 0,
            'step': 0, # 0: Read, 1: Cover/Compare
            'score': 0,
            'opts': []
        })

    def set_difficulty(self, level):
        q_list = DIFFICULTY_LEVELS[level]["items"].copy()
        random.shuffle(q_list)
        st.session_state.update({
            'difficulty': level,
            'questions': q_list,
            'idx': 0,
            'step': 0,
            'phase': 'LEARNING'
        })

    def gen_opts(self):
        correct = st.session_state['questions'][st.session_state['idx']]['a']
        opts = {correct}
        while len(opts) < 3:
            fake = correct + random.randint(-5, 5)
            if fake > 0 and fake != correct: opts.add(fake)
        opt_list = list(opts)
        random.shuffle(opt_list)
        st.session_state['opts'] = opt_list

# --- 5. MAIN APP FLOW ---
def main():
    app = CCCApp()
    phase = st.session_state['phase']

    # --- MENU PHASE ---
    if phase == 'MENU':
        st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Matematiksel Akıcılık ve Otomatikleşme Eğitimi</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="card"><h3>Hoş Geldin!</h3><p>Lütfen yapmak istediğin çalışmayı seç.</p></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📘 Öğretim Modu\n(Adım Adım Öğren)", use_container_width=True):
                st.session_state['phase'] = 'LEVEL_SELECT'
                st.rerun()
        with c2:
            if st.button("📝 Sınav Modu\n(Kendini Test Et)", use_container_width=True):
                all_q = [q for l in DIFFICULTY_LEVELS.values() for q in l["items"]]
                st.session_state.update({
                    'questions': random.sample(all_q, 10),
                    'idx': 0, 'score': 0, 'phase': 'ASSESSMENT'
                })
                app.gen_opts()
                st.rerun()

    # --- LEVEL SELECTION PHASE (image_1d836f.png) ---
    elif phase == 'LEVEL_SELECT':
        if st.button("← Ana Menü", key="back_menu"):
            app._reset_state()
            st.rerun()
            
        st.markdown("<h2>Zorluk Seviyesi Seç</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="kolay-btn">', unsafe_allow_html=True)
        if st.button(f"Kolay\n{DIFFICULTY_LEVELS['Kolay']['desc']}", key="btn_kolay"):
            app.set_difficulty("Kolay")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="orta-btn">', unsafe_allow_html=True)
        if st.button(f"Orta\n{DIFFICULTY_LEVELS['Orta']['desc']}", key="btn_orta"):
            app.set_difficulty("Orta")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="zor-btn">', unsafe_allow_html=True)
        if st.button(f"Zor\n{DIFFICULTY_LEVELS['Zor']['desc']}", key="btn_zor"):
            app.set_difficulty("Zor")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LEARNING PHASE (CCC Strategy) ---
    elif phase == 'LEARNING':
        if st.button("← Seviye Seçimi", key="back_lv"):
            st.session_state['phase'] = 'LEVEL_SELECT'
            st.rerun()
            
        q = st.session_state['questions'][st.session_state['idx']]
        st.progress((st.session_state['idx']) / len(st.session_state['questions']))

        if st.session_state['step'] == 0: # STEP 1: READ [cite: 6, 13]
            st.markdown(f'<div class="card"><div class="big-font">{q["q"]} = {q["a"]}</div></div>', unsafe_allow_html=True)
            st.info("👁️ İşlemi ve cevabı oku, sonra 'Kapat' butonuna bas.")
            if st.button("🙈 Kapat ve Cevapla", use_container_width=True):
                app.gen_opts()
                st.session_state['step'] = 1
                st.rerun()
        else: # STEP 2-3: COVER & COMPARE [cite: 7, 14, 15]
            st.markdown('<div class="covered-box">🙈 CEVAP GİZLENDİ</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><div class="big-font">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, opt in enumerate(st.session_state['opts']):
                if cols[i].button(str(opt), key=f"learn_opt_{i}"):
                    if opt == q['a']:
                        if st.session_state['idx'] < len(st.session_state['questions']) - 1:
                            st.session_state['idx'] += 1
                            st.session_state['step'] = 0
                        else: st.session_state['phase'] = 'COMPLETED'
                    else: st.session_state['phase'] = 'ERROR'
                    st.rerun()

    # --- ERROR PHASE (Manual Reset)  ---
    elif phase == 'ERROR':
        st.markdown('<div class="card" style="border-color: #ef4444;">'
                    '<h2 style="color: #ef4444 !important;">❌ Yanlış Cevap</h2>'
                    '<p>Strateji gereği işlemi tekrar incelemelisin.</p></div>', unsafe_allow_html=True)
        if st.button("🔄 Tekrar Dene (Başa Dön)", type="primary", use_container_width=True):
            st.session_state['step'] = 0
            st.session_state['phase'] = 'LEARNING'
            st.rerun()

    # --- ASSESSMENT PHASE ---
    elif phase == 'ASSESSMENT':
        if st.button("← Sınavdan Çık", key="exit_exam"):
            app._reset_state()
            st.rerun()
            
        q = st.session_state['questions'][st.session_state['idx']]
        st.markdown(f"### Soru {st.session_state['idx'] + 1} / 10")
        st.markdown(f'<div class="card"><div class="big-font">{q["q"]} = ?</div></div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['opts']):
            if cols[i].button(str(opt), key=f"exam_opt_{i}"):
                if opt == q['a']: st.session_state['score'] += 1
                if st.session_state['idx'] < 9:
                    st.session_state['idx'] += 1
                    app.gen_opts()
                else: st.session_state['phase'] = 'COMPLETED'
                st.rerun()

    # --- COMPLETED PHASE ---
    elif phase == 'COMPLETED':
        st.balloons()
        st.markdown('<div class="card"><h2>🎉 Tebrikler!</h2><p>Çalışmayı başarıyla tamamladın.</p></div>', unsafe_allow_html=True)
        if 'score' in st.session_state and st.session_state['questions']:
             st.metric("Sınav Puanın", f"{st.session_state['score']} / 10")
        
        if st.button("🏠 Ana Menüye Dön", use_container_width=True):
            app._reset_state()
            st.rerun()

if __name__ == "__main__":
    main()
