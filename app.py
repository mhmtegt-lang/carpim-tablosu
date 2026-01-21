import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Çarpım Tablosu", page_icon="🎓", layout="centered")

# --- 2. TASARIM (CSS) ---
# Gönderdiğin görseldeki tasarımı (Yeşil/Mor butonlar, Bilgi Kutusu) oluşturan kod
st.markdown("""
<style>
    /* Genel Arka Plan */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Başlık Stili */
    h1 {
        color: #1e3a8a;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 20px;
        margin-bottom: 30px;
    }

    /* "Nasıl Çalışır" Kutusu (Açık Mavi) */
    .info-box {
        background-color: #f0fdf4; /* Açık yeşilimsi/mavi ton */
        background: linear-gradient(to right, #eff6ff, #f5f3ff);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e7ff;
        margin-bottom: 30px;
        color: #1e293b;
    }
    .info-box h3 {
        color: #4338ca;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .info-box li {
        margin-bottom: 8px;
        font-size: 16px;
    }

    /* KART BUTONLAR İÇİN ÖZEL AYARLAR */
    /* Sol Kolon (Öğretim Modu) Butonu -> YEŞİL */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #22c55e !important;
        color: white !important;
        height: 180px !important; /* Yükseklik */
        border-radius: 20px !important;
        border: none !important;
        font-size: 24px !important;
        font-weight: bold !important;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.3) !important;
        transition: transform 0.2s;
        white-space: pre-wrap; /* Alt satıra geçmeye izin ver */
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #16a34a !important;
    }

    /* Sağ Kolon (Değerlendirme) Butonu -> MOR */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #a855f7 !important;
        color: white !important;
        height: 180px !important;
        border-radius: 20px !important;
        border: none !important;
        font-size: 24px !important;
        font-weight: bold !important;
        box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.3) !important;
        transition: transform 0.2s;
        white-space: pre-wrap;
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #9333ea !important;
    }
    
    /* Soru Kartları */
    .card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .big-text {
        font-size: 50px;
        font-weight: bold;
        color: #1e293b;
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

# --- 4. YÖNETİCİ SINIFI (LOGIC) ---
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

# --- 5. ANA UYGULAMA (VIEW) ---
def main():
    manager = CCCManager()
    phase = st.session_state['current_phase']

    # Başlık Alanı
    st.markdown("<h1>Kapat-Kopyala-Karşılaştır</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Çarpım Tablosu Öğretimi</p>", unsafe_allow_html=True)

    if phase == 'MENU':
        # Bilgi Kutusu (Görseldeki Gibi)
        st.markdown("""
        <div class="info-box">
            <h3>Nasıl Çalışır?</h3>
            <ul>
                <li><b>1. Oku:</b> İşlemi ve cevabını dikkatlice oku.</li>
                <li><b>2. Kapat:</b> 'Kapat' butonuna basarak cevabı gizle.</li>
                <li><b>3. Yaz:</b> Cevabı aklından bul.</li>
                <li><b>4. Karşılaştır:</b> Seçeneklerden doğrusunu işaretle.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # İki Büyük Buton (CSS ile şekillendirildi)
        col1, col2 = st.columns(2)
        
        with col1:
            # Yeşil Buton
            if st.button("📖\nÖğretim Modu\n(Adım Adım Öğren)", use_container_width=True):
                # Varsayılan olarak Basit seviyeden başlatıyoruz, içeride değiştirebilir
                manager.start_learning("Basit (2-5 Çarpanları)")
                st.rerun()

        with col2:
            # Mor Buton
            if st.button("📋\nDeğerlendirme\n(Kendini Test Et)", use_container_width=True):
                manager.start_assessment()
                st.rerun()

        # Seviye Seçimi (Öğretim Modu İçin)
        st.write("")
        st.markdown("<div style='text-align: center; color: #64748b;'>👇 Öğretim Modu için Seviye Seçimi 👇</div>", unsafe_allow_html=True)
        secilen_seviye = st.selectbox("Seviye:", list(DIFFICULTY_LEVELS.keys()), label_visibility="collapsed")
        # Eğer kullanıcı seçim yaparsa session state'i güncelle
        st.session_state['difficulty'] = secilen_seviye


    elif phase == 'LEARNING':
        # Öğrenme Modu Ekranı
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        step = st.session_state['learning_step']

        # İlerleme Çubuğu
        st.progress((q_idx) / len(queue))
        st.caption(f"Soru {q_idx + 1} / {len(queue)} - Seviye: {st.session_state['difficulty']}")

        if step == 0: # GÖR / OKU
            st.markdown(f"""
            <div class="card">
                <div class="big-text">{current_q['q']} = {current_q['a']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("👁️ İyice ezberleyene kadar bak.")
            
            if st.session_state.get('feedback') == 'WRONG':
                st.error("⚠️ Yanlış cevap verdiğin için başa döndük. Tekrar odaklan!")

            if st.button("🙈 Kapat ve Yaz", use_container_width=True):
                manager.generate_options(current_q['a'])
                st.session_state['learning_step'] = 1
                st.rerun()

        elif step == 1: # KAPAT / SEÇ
            st.markdown(f"""
            <div class="card" style="background-color: #f1f5f9; border-style: dashed;">
                <div class="big-text" style="color: #94a3b8;">{current_q['q']} = ?</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("👇 Doğru cevabı seç.")
            
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
                        st.session_state['learning_step'] = 0 # Başa dön kuralı
                    st.rerun()

    elif phase == 'ASSESSMENT':
        # Değerlendirme Modu Ekranı
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]

        st.subheader(f"📝 Soru {q_idx + 1} / 10")
        
        st.markdown(f"""
        <div class="card" style="border-color: #a855f7;">
            <div class="big-text" style="color: #6b21a8;">{current_q['q']} = ?</div>
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

    elif phase == 'COMPLETED_LEARNING':
        st.balloons()
        st.success("🎉 Tebrikler! Bu seviyeyi tamamladın.")
        if st.button("Ana Menüye Dön", use_container_width=True):
            manager._reset_state()
            st.rerun()

    elif phase == 'COMPLETED_ASSESSMENT':
        score = st.session_state['assessment_score']
        st.balloons()
        st.markdown(f"""
        <div class="card">
            <h2>Sınav Sonucu</h2>
            <div style="font-size: 80px; color: #4338ca;">{score} / 10</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Tekrar Dene", use_container_width=True):
            manager._reset_state()
            st.rerun()

if __name__ == "__main__":
    main()
