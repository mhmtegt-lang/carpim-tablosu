import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS VE ANİMASYONLAR) ---
st.markdown("""
<style>
    /* 1. GENEL AYARLAR */
    .stApp {
        background-color: #ffffff !important;
    }
    p, h1, h2, h3, h4, li, span, div, label {
        color: #1e293b !important;
    }
    h1 {
        color: #1e3a8a !important;
        text-align: center;
        font-family: sans-serif;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #64748b !important;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* BİLGİ KUTUSU */
    .info-box {
        background-color: #f0f9ff !important;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #bae6fd;
        margin-bottom: 25px;
    }

    /* NORMAL KART TASARIMI */
    .card {
        background-color: #ffffff !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .big-text {
        font-size: 45px;
        font-weight: bold;
        color: #1e293b !important;
    }

    /* --- YENİ ANİMASYONLU GİZLİ KART --- */
    
    /* Animasyon Tanımı: Yukarıdan aşağı süzülme ve netleşme */
    @keyframes slide-down-fade {
        0% {
            opacity: 0;
            transform: translateY(-30px) scale(0.95);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .hidden-card {
        /* Animasyonu uygula: 0.5 saniye sürsün */
        animation: slide-down-fade 0.5s ease-out forwards;
        
        background-color: #f8fafc !important;
        /* Perde hissi veren çapraz çizgiler */
        background-image: repeating-linear-gradient(
            45deg,
            #f1f5f9,
            #f1f5f9 10px,
            #f8fafc 10px,
            #f8fafc 20px
        );
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 3px dashed #cbd5e1;
        margin-bottom: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.05); /* İç gölge */
    }
    
    .hidden-text {
        font-size: 45px;
        font-weight: bold;
        color: #94a3b8 !important; /* Silik renk */
        text-shadow: 1px 1px 0 #fff;
    }

    /* BUTONLAR */
    /* Sol (Yeşil) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #22c55e !important;
        color: white !important;
        border: none !important;
        height: 150px;
        font-size: 22px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.4);
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button:hover {
        background-color: #16a34a !important;
        transform: scale(1.02);
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button p { color: white !important; }

    /* Sağ (Mor) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #a855f7 !important;
        color: white !important;
        border: none !important;
        height: 150px;
        font-size: 22px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(168, 85, 247, 0.4);
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        background-color: #9333ea !important;
        transform: scale(1.02);
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button p { color: white !important; }

    /* Navigasyon ve Seçenek Butonları */
    .stButton > button {
        background-color: white;
        color: #334155;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton > button:hover {
        border-color: #3b82f6;
        color: #3b82f6 !important;
        background-color: #eff6ff;
    }
    
    /* Geri butonunu küçült */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stButton"] > button {
        height: auto !important;
        padding: 10px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border-color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER ---
DIFFICULTY_LEVELS = {
    "Basit (2-5 Çarpanları)": [
        {"q": "2 x 2", "a": 4}, {"q": "2 x 3", "a": 6}, {"q": "2 x 4", "a": 8}, {"q": "2 x 5", "a": 10},
        {"q": "3 x 3", "a": 9}, {"q": "3 x 4", "a": 12}, {"q": "3 x 5", "a": 15},
        {"q": "4 x 4", "a": 16}, {"q": "4 x 5", "a": 20}, {"q": "5 x 5", "a": 25}
    ],
    "Orta (Karmaşık)": [
        {"q": "2 x 6", "a": 12}, {"q": "2 x 7", "a": 14}, {"q": "2 x 8", "a": 16}, {"q": "2 x 9", "a": 18},
        {"q": "3 x 6", "a": 18}, {"q": "3 x 7", "a": 21}, {"q": "3 x 8", "a": 24}, {"q": "3 x 9", "a": 27},
        {"q": "4 x 6", "a": 24}, {"q": "4 x 7", "a": 28}, {"q": "4 x 8", "a": 32}, {"q": "4 x 9", "a": 36}
    ],
    "Zor (6-9 Çarpanları)": [
        {"q": "6 x 6", "a": 36}, {"q": "6 x 7", "a": 42}, {"q": "6 x 8", "a": 48}, {"q": "6 x 9", "a": 54},
        {"q": "7 x 7", "a": 49}, {"q": "7 x 8", "a": 56}, {"q": "7 x 9", "a": 63},
        {"q": "8 x 8", "a": 64}, {"q": "8 x 9", "a": 72}, {"q": "9 x 9", "a": 81}
    ]
}

# --- 4. YÖNETİCİ SINIFI ---
class CCCManager:
    def __init__(self):
        if 'manager_initialized' not in st.session_state:
            self._reset_state()
            st.session_state['manager_initialized'] = True

    def _reset_state(self):
        st.session_state.update({
            'current_phase': 'MENU',
            'difficulty': 'Basit (2-5 Çarpanları)',
            'question_queue': [],
            'current_q_index': 0,
            'learning_step': 0,
            'feedback': None,
            'assessment_score': 0,
            'current_options': []
        })

    def generate_options(self, correct_ans):
        options = {correct_ans}
        while len(options) < 3:
            fake = correct_ans + random.randint(-5, 5)
            if fake > 0 and fake != correct_ans:
                options.add(fake)
        opt_list = list(options)
        random.shuffle(opt_list)
        st.session_state['current_options'] = opt_list

    def start_learning(self, difficulty):
        questions = DIFFICULTY_LEVELS[difficulty].copy()
        random.shuffle(questions)
        st.session_state.update({
            'difficulty': difficulty,
            'question_queue': questions,
            'current_q_index': 0,
            'learning_step': 0,
            'current_phase': 'LEARNING',
            'feedback': None
        })

    def start_assessment(self):
        all_q = [q for level in DIFFICULTY_LEVELS.values() for q in level]
        st.session_state.update({
            'question_queue': random.sample(all_q, 10),
            'current_q_index': 0,
            'assessment_score': 0,
            'current_phase': 'ASSESSMENT'
        })
        self.generate_options(st.session_state['question_queue'][0]['a'])

# --- 5. ANA UYGULAMA ---
def main():
    manager = CCCManager()
    phase = st.session_state['current_phase']

    # --- BAŞLIK ---
    st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Çarpım Tablosu Öğretimi</div>", unsafe_allow_html=True)

    # --- ANA MENÜ ---
    if phase == 'MENU':
        st.markdown("""
        <div class="info-box">
            <h3>Nasıl Çalışır?</h3>
            <ul>
                <li><b>1. Oku:</b> İşlemi ve cevabını dikkatlice incele.</li>
                <li><b>2. Kapat:</b> Butona basarak cevabı gizle.</li>
                <li><b>3. Yaz/Seç:</b> Doğru cevabı seçeneklerden bul.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖\nÖğretim Modu\n(Adım Adım)", use_container_width=True):
                manager.start_learning("Basit (2-5 Çarpanları)")
                st.rerun()

        with col2:
            if st.button("🚀\nDeğerlendirme\n(Kendini Test Et)", use_container_width=True):
                manager.start_assessment()
                st.rerun()

        st.write("")
        st.markdown("<div style='text-align: center; font-weight: bold;'>👇 Öğretim Seviyesi Seçimi 👇</div>", unsafe_allow_html=True)
        secim = st.selectbox("Seviye:", list(DIFFICULTY_LEVELS.keys()), label_visibility="collapsed")
        st.session_state['difficulty'] = secim

    # --- ÖĞRENME MODU ---
    elif phase == 'LEARNING':
        # Geri Butonu
        if st.button("⬅️ Ana Menüye Dön"):
            manager._reset_state()
            st.rerun()

        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        step = st.session_state['learning_step']

        st.progress((q_idx) / len(queue))
        st.caption(f"İlerleme: {q_idx + 1}/{len(queue)} - {st.session_state['difficulty']}")

        if step == 0: # GÖR
            st.markdown(f"""
            <div class="card">
                <div class="big-text">{current_q['q']} = {current_q['a']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.get('feedback') == 'WRONG':
                st.error("⚠️ Yanlış cevap! Başa döndük.")

            if st.button("🙈 Kapat ve Cevapla", use_container_width=True):
                manager.generate_options(current_q['a'])
                st.session_state['learning_step'] = 1
                st.rerun()

        elif step == 1: # KAPAT/SEÇ (ANİMASYONLU)
            # Burada 'hidden-card' class'ı CSS animasyonunu tetikler
            st.markdown(f"""
            <div class="hidden-card">
                <div style="font-size: 20px; margin-bottom: 10px;">🙈 KAPALI</div>
                <div class="hidden-text">{current_q['q']} = ?</div>
            </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, opt in enumerate(st.session_state['current_options']):
                if cols[i].button(str(opt), key=f"opt_{i}", use_container_width=True):
                    if opt == current_q['a']:
                        st.session_state['feedback'] = "CORRECT"
                        if q_idx < len(queue) - 1:
                            st.session_state['current_q_index'] += 1
                            st.session_state['learning_step'] = 0
                        else:
                            st.session_state['current_phase'] = 'COMPLETED_LEARNING'
                    else:
                        st.session_state['feedback'] = "WRONG"
                        st.session_state['learning_step'] = 0
                    st.rerun()

    # --- DEĞERLENDİRME MODU ---
    elif phase == 'ASSESSMENT':
        if st.button("⬅️ Sınavdan Çık"):
            manager._reset_state()
            st.rerun()

        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]

        st.subheader(f"Soru {q_idx + 1} / 10")
        
        st.markdown(f"""
        <div class="card" style="border-color: #a855f7;">
            <div class="big-text" style="color: #6b21a8 !important;">{current_q['q']} = ?</div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['current_options']):
            if cols[i].button(str(opt), key=f"assess_{i}", use_container_width=True):
                if opt == current_q['a']:
                    st.session_state['assessment_score'] += 1
                
                if q_idx < len(queue) - 1:
                    st.session_state['current_q_index'] += 1
                    manager.generate_options(queue[q_idx+1]['a'])
                else:
                    st.session_state['current_phase'] = 'COMPLETED_ASSESSMENT'
                st.rerun()

    # --- TAMAMLANMA ---
    elif phase == 'COMPLETED_LEARNING':
        st.balloons()
        st.success("Tebrikler! Seviye Tamamlandı.")
        if st.button("Ana Menü", use_container_width=True):
            manager._reset_state()
            st.rerun()

    elif phase == 'COMPLETED_ASSESSMENT':
        score = st.session_state['assessment_score']
        st.balloons()
        st.markdown(f"""
        <div class="card">
            <h2>Puanın</h2>
            <div style="font-size: 80px; color: #4338ca !important;">{score} / 10</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ana Menü", use_container_width=True):
            manager._reset_state()
            st.rerun()

if __name__ == "__main__":
    main()
