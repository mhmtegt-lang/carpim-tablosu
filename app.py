import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS VE ANİMASYONLAR) ---
st.markdown("""
<style>
    /* 1. GENEL AYARLAR */
    .stApp { background-color: #ffffff !important; }
    p, h1, h2, h3, h4, li, span, div, label { color: #1e293b !important; }
    h1 { color: #1e3a8a !important; text-align: center; font-family: sans-serif; font-weight: 800; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #64748b !important; font-size: 18px; margin-bottom: 30px; }

    /* BİLGİ KUTUSU */
    .info-box { background-color: #f0f9ff !important; padding: 20px; border-radius: 15px; border: 1px solid #bae6fd; margin-bottom: 25px; }

    /* KART TASARIMI */
    .card { background-color: #ffffff !important; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); text-align: center; border: 2px solid #e2e8f0; margin-bottom: 20px; }
    .big-text { font-size: 45px; font-weight: bold; color: #1e293b !important; }

    /* KAPALI KUTU */
    @keyframes slide-down { 0% { transform: scaleY(0); transform-origin: top; } 100% { transform: scaleY(1); transform-origin: top; } }
    .covered-box {
        animation: slide-down 0.4s ease-out forwards;
        background-color: #f1f5f9 !important;
        background-image: repeating-linear-gradient(45deg, #e2e8f0, #e2e8f0 10px, #f1f5f9 10px, #f1f5f9 20px);
        padding: 20px; border-radius: 15px; text-align: center; border: 2px dashed #cbd5e1; margin-bottom: 20px;
        color: #94a3b8 !important; font-weight: bold; font-size: 18px;
    }

    /* SORU KUTUSU */
    .question-box { background-color: #eff6ff !important; border: 2px solid #3b82f6; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15); }
    .question-text { font-size: 50px; font-weight: 800; color: #1d4ed8 !important; }

    /* HATA KUTUSU */
    .error-box { background-color: #fef2f2 !important; border: 2px solid #ef4444; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
    .error-text { font-size: 30px; font-weight: bold; color: #b91c1c !important; }

    /* --- ANA MENÜ BUTONLARI (YEŞİL VE MOR) --- */
    /* Sol Kolon (Yeşil) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #22c55e !important; color: white !important; border: none !important; height: 150px; font-size: 22px !important; border-radius: 15px !important; box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.4);
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button:hover { background-color: #16a34a !important; transform: scale(1.02); }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button p { color: white !important; }

    /* Sağ Kolon (Mor) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #a855f7 !important; color: white !important; border: none !important; height: 150px; font-size: 22px !important; border-radius: 15px !important; box-shadow: 0 4px 6px -1px rgba(168, 85, 247, 0.4);
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover { background-color: #9333ea !important; transform: scale(1.02); }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button p { color: white !important; }

    /* STANDART BUTONLAR */
    .stButton > button { background-color: white; color: #334155; border: 2px solid #cbd5e1; border-radius: 12px; height: 60px; font-size: 20px; font-weight: bold; }
    .stButton > button:hover { border-color: #3b82f6; color: #3b82f6 !important; background-color: #eff6ff; }
    
    /* Geri butonlarını küçült */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stButton"] > button { height: auto !important; padding: 10px !important; font-size: 16px !important; }

    /* --- SEVİYE SEÇİM EKRANI STİLİ --- */
    /* Kolay Butonu (Yeşil) - CSS ile hedefleme */
    /* Bu stiller Level Selection ekranında özel olarak kullanılır */
</style>
""", unsafe_allow_html=True)

# --- 3. VERİLER ---
DIFFICULTY_LEVELS = {
    "Basit": [
        {"q": "2 x 2", "a": 4}, {"q": "2 x 3", "a": 6}, {"q": "2 x 4", "a": 8}, {"q": "2 x 5", "a": 10},
        {"q": "3 x 3", "a": 9}, {"q": "3 x 4", "a": 12}, {"q": "3 x 5", "a": 15},
        {"q": "4 x 4", "a": 16}, {"q": "4 x 5", "a": 20}, {"q": "5 x 5", "a": 25}
    ],
    "Orta": [
        {"q": "2 x 6", "a": 12}, {"q": "2 x 7", "a": 14}, {"q": "2 x 8", "a": 16}, {"q": "2 x 9", "a": 18},
        {"q": "3 x 6", "a": 18}, {"q": "3 x 7", "a": 21}, {"q": "3 x 8", "a": 24}, {"q": "3 x 9", "a": 27},
        {"q": "4 x 6", "a": 24}, {"q": "4 x 7", "a": 28}, {"q": "4 x 8", "a": 32}, {"q": "4 x 9", "a": 36}
    ],
    "Zor": [
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
            'difficulty': 'Basit',
            'question_queue': [],
            'current_q_index': 0,
            'learning_step': 0,
            'assessment_score': 0,
            'current_options': [],
            'show_error_screen': False
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
            'show_error_screen': False
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

    # --- BAŞLIK HER SAYFADA SABİT OLMASIN, SADECE MENÜDE OLSUN ---
    if phase == 'MENU':
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
                <li><b>3. Seç:</b> Doğru cevabı seçeneklerden bul.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖\nÖğretim Modu\n(Adım Adım)", use_container_width=True):
                st.session_state['current_phase'] = 'LEVEL_SELECTION'
                st.rerun()

        with col2:
            if st.button("🚀\nDeğerlendirme\n(Kendini Test Et)", use_container_width=True):
                manager.start_assessment()
                st.rerun()

    # --- SEVİYE SEÇİM EKRANI (YENİ) ---
    elif phase == 'LEVEL_SELECTION':
        # Sol üst geri butonu
        if st.button("⬅️ Ana Menü"):
            manager._reset_state()
            st.rerun()

        st.markdown("<h2 style='text-align: center; color: #334155;'>Zorluk Seviyesi Seç</h2>", unsafe_allow_html=True)
        st.write("")

        # Butonlar için özel stiller
        st.markdown("""
        <style>
            /* 1. Buton (Kolay) - Yeşil */
            div.row-widget.stButton:nth-of-type(2) button {
                background-color: #22c55e !important; color: white !important; border: none; height: 100px;
            }
            div.row-widget.stButton:nth-of-type(2) button:hover { background-color: #16a34a !important; transform: scale(1.02); }
            div.row-widget.stButton:nth-of-type(2) button p { color: white !important; font-size: 24px; font-weight: bold; }
            
            /* 2. Buton (Orta) - Turuncu */
            div.row-widget.stButton:nth-of-type(3) button {
                background-color: #eab308 !important; color: white !important; border: none; height: 100px;
            }
            div.row-widget.stButton:nth-of-type(3) button:hover { background-color: #ca8a04 !important; transform: scale(1.02); }
            div.row-widget.stButton:nth-of-type(3) button p { color: white !important; font-size: 24px; font-weight: bold; }
            
            /* 3. Buton (Zor) - Kırmızı */
            div.row-widget.stButton:nth-of-type(4) button {
                background-color: #ef4444 !important; color: white !important; border: none; height: 100px;
            }
            div.row-widget.stButton:nth-of-type(4) button:hover { background-color: #dc2626 !important; transform: scale(1.02); }
            div.row-widget.stButton:nth-of-type(4) button p { color: white !important; font-size: 24px; font-weight: bold; }
            
            .desc { font-size: 14px; color: white; display: block; margin-top: 5px; opacity: 0.9; }
        </style>
        """, unsafe_allow_html=True)

        # 1. Kolay Buton
        if st.button("Kolay\n2, 3, 4, 5 sayılarının birbirleriyle çarpımı", use_container_width=True):
            manager.start_learning("Basit")
            st.rerun()

        # 2. Orta Buton
        if st.button("Orta\n2, 3, 4, 5 sayılarının 6, 7, 8, 9 ile çarpımı", use_container_width=True):
            manager.start_learning("Orta")
            st.rerun()

        # 3. Zor Buton
        if st.button("Zor\n6, 7, 8, 9 sayılarının birbirleriyle çarpımı", use_container_width=True):
            manager.start_learning("Zor")
            st.rerun()

    # --- ÖĞRENME MODU ---
    elif phase == 'LEARNING':
        if st.button("⬅️ Seviye Seçimi"):
            st.session_state['current_phase'] = 'LEVEL_SELECTION'
            st.rerun()

        # HATA EKRANI KONTROLÜ
        if st.session_state.get('show_error_screen'):
            st.markdown("""
            <div class="error-box">
                <div class="error-text">❌ Yanlış Cevap!</div>
                <p>Üzülme, işlemi tekrar incelememiz gerekiyor.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Tekrar Dene (Başa Dön)", type="primary", use_container_width=True):
                st.session_state['show_error_screen'] = False
                st.session_state['learning_step'] = 0
                st.rerun()
                
        else:
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

                if st.button("🙈 Kapat ve Cevapla", use_container_width=True):
                    manager.generate_options(current_q['a'])
                    st.session_state['learning_step'] = 1
                    st.rerun()

            elif step == 1: # KAPAT/SEÇ
                # Üstte Kapalı Kutu
                st.markdown("""
                <div class="covered-box">
                    🙈 CEVAP GİZLENDİ
                </div>
                """, unsafe_allow_html=True)

                # Altta Soru
                st.markdown(f"""
                <div class="question-box">
                    <div class="question-text">{current_q['q']} = ?</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Seçenekler
                cols = st.columns(3)
                for i, opt in enumerate(st.session_state['current_options']):
                    if cols[i].button(str(opt), key=f"opt_{i}", use_container_width=True):
                        if opt == current_q['a']:
                            if q_idx < len(queue) - 1:
                                st.session_state['current_q_index'] += 1
                                st.session_state['learning_step'] = 0
                            else:
                                st.session_state['current_phase'] = 'COMPLETED_LEARNING'
                        else:
                            st.session_state['show_error_screen'] = True
                        st.rerun()
                        
                # Unuttum Butonu
                st.write("")
                if st.button("👀 Unuttum, Cevaba Bak"):
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
        if st.button("Seviye Seçimine Dön", use_container_width=True):
            st.session_state['current_phase'] = 'LEVEL_SELECTION'
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
