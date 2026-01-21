import streamlit as st
import random
import time

# --- VERİLER (DATA) ---
# Doküman Tablo 3.1 ve Ek 6/8 referans alınarak zorluk seviyeleri belirlenmiştir [cite: 25]
DIFFICULTY_LEVELS = {
    "Basit (2-5 Çarpanları)": [
        {"q": "2 x 2", "a": 4}, {"q": "2 x 3", "a": 6}, {"q": "2 x 4", "a": 8}, {"q": "2 x 5", "a": 10},
        {"q": "3 x 3", "a": 9}, {"q": "3 x 4", "a": 12}, {"q": "3 x 5", "a": 15},
        {"q": "4 x 4", "a": 16}, {"q": "4 x 5", "a": 20}, {"q": "5 x 5", "a": 25}
    ],
    "Orta (Karmaşık)": [
        {"q": "2 x 6", "a": 12}, {"q": "2 x 7", "a": 14}, {"q": "2 x 8", "a": 16}, {"q": "2 x 9", "a": 18},
        {"q": "3 x 6", "a": 18}, {"q": "3 x 7", "a": 21}, {"q": "3 x 8", "a": 24}, {"q": "3 x 9", "a": 27},
        {"q": "4 x 6", "a": 24}, {"q": "4 x 7", "a": 28}, {"q": "4 x 8", "a": 32}, {"q": "4 x 9", "a": 36},
        {"q": "5 x 6", "a": 30}, {"q": "5 x 7", "a": 35}, {"q": "5 x 8", "a": 40}, {"q": "5 x 9", "a": 45}
    ],
    "Zor (6-9 Çarpanları)": [
        {"q": "6 x 6", "a": 36}, {"q": "6 x 7", "a": 42}, {"q": "6 x 8", "a": 48}, {"q": "6 x 9", "a": 54},
        {"q": "7 x 7", "a": 49}, {"q": "7 x 8", "a": 56}, {"q": "7 x 9", "a": 63},
        {"q": "8 x 8", "a": 64}, {"q": "8 x 9", "a": 72}, {"q": "9 x 9", "a": 81}
    ]
}

# --- İŞ MANTIĞI (LOGIC) ---
class CCCManager:
    def __init__(self):
        # Uygulama durumu (state) yönetimi
        if 'manager_initialized' not in st.session_state:
            self._reset_state()
            st.session_state['manager_initialized'] = True

    def _reset_state(self):
        st.session_state['current_phase'] = 'MENU'
        st.session_state['difficulty'] = list(DIFFICULTY_LEVELS.keys())[0]
        st.session_state['question_queue'] = []
        st.session_state['current_q_index'] = 0
        st.session_state['learning_step'] = 0 
        st.session_state['feedback'] = None
        st.session_state['assessment_score'] = 0
        st.session_state['current_options'] = []

    def generate_options(self):
        """Mevcut soru için doğru cevap ve 2 yanlış çeldirici üretir."""
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        correct_ans = current_q['a']
        options = {correct_ans}
        while len(options) < 3:
            fake = correct_ans + random.randint(-5, 5)
            if fake > 0 and fake != correct_ans:
                options.add(fake)
        opt_list = list(options)
        random.shuffle(opt_list)
        st.session_state['current_options'] = opt_list

    # --- ÖĞRENME MODU ---
    def start_learning_mode(self, difficulty: str):
        st.session_state['difficulty'] = difficulty
        questions = DIFFICULTY_LEVELS[difficulty].copy()
        random.shuffle(questions)
        st.session_state['question_queue'] = questions
        st.session_state['current_q_index'] = 0
        st.session_state['learning_step'] = 0
        st.session_state['current_phase'] = 'LEARNING'
        st.session_state['feedback'] = None

    def check_learning_answer(self, user_answer):
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        if int(user_answer) == current_q['a']:
            st.session_state['feedback'] = "CORRECT"
            if st.session_state['current_q_index'] < len(st.session_state['question_queue']) - 1:
                st.session_state['current_q_index'] += 1
                st.session_state['learning_step'] = 0 # Bir sonraki işlem için 'Bak' aşamasına dön [cite: 16]
            else:
                st.session_state['current_phase'] = 'COMPLETED_LEARNING'
        else:
            st.session_state['feedback'] = "WRONG"
            st.session_state['learning_step'] = 0 # Yanlışta öğretim döngüsünü başa sar 

    def next_level(self):
        levels = list(DIFFICULTY_LEVELS.keys())
        current_diff = st.session_state['difficulty']
        try:
            current_index = levels.index(current_diff)
            if current_index + 1 < len(levels):
                next_diff = levels[current_index + 1]
                self.start_learning_mode(next_diff)
                st.rerun()
            else:
                self.go_home()
        except ValueError:
            self.go_home()

    # --- SINAV (YOKLAMA) MODU ---
    def start_assessment_mode(self):
        # Havuzdan rastgele 10 yoklama sorusu seç [cite: 10]
        all_questions = []
        for level in DIFFICULTY_LEVELS.values():
            all_questions.extend(level)
        selected_questions = random.sample(all_questions, 10)
        
        st.session_state['question_queue'] = selected_questions
        st.session_state['current_q_index'] = 0
        st.session_state['assessment_score'] = 0
        st.session_state['current_phase'] = 'ASSESSMENT'
        self.generate_options()

    def check_assessment_answer(self, user_answer):
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        if int(user_answer) == current_q['a']:
            st.session_state['assessment_score'] += 1
        
        if st.session_state['current_q_index'] < len(st.session_state['question_queue']) - 1:
            st.session_state['current_q_index'] += 1
            self.generate_options()
        else:
            st.session_state['current_phase'] = 'COMPLETED_ASSESSMENT'

    def go_home(self):
        self._reset_state()

# --- ARAYÜZ (UI) TASARIMI ---
st.set_page_config(page_title="KKK Matematik", page_icon="✖️", layout="centered")

# Görsel iyileştirmeler için özel CSS
st.markdown("""
<style>
    .big-font { font-size:42px !important; font-weight:bold; text-align:center; color:#1e3a8a; }
    .card { background-color: #f8fafc; padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #e2e8f0; margin-bottom: 20px;}
    .hidden-card { background-color: #f1f5f9; color: #475569; padding: 40px; border-radius: 20px; text-align: center; border: 3px dashed #cbd5e1; user-select: none;}
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 26px;
        font-weight: bold;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    manager = CCCManager()
    phase = st.session_state['current_phase']

    st.title("🎓 Çarpım Tablosu")
    
    # 1. ANA MENÜ
    if phase == 'MENU':
        st.info("Bilimsel KKK stratejisi ile çarpım tablosunu eğlenerek öğren.")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📚 Öğrenme Modu")
            diff = st.selectbox("Çalışma Seviyesi:", list(DIFFICULTY_LEVELS.keys()))
            if st.button("Öğrenmeye Başla", use_container_width=True):
                manager.start_learning_mode(diff)
                st.rerun()
        with col2:
            st.subheader("📝 Sınav Modu")
            st.write("Sırayla sorulan 10 soruda kendini dene.")
            if st.button("Sınavı Başlat", type="primary", use_container_width=True):
                manager.start_assessment_mode()
                st.rerun()

    # 2. ÖĞRENME MODU (SEQUENTIAL)
    elif phase == 'LEARNING':
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        step = st.session_state['learning_step']
        
        st.progress((q_idx) / len(queue), text=f"İlerleme: {q_idx}/{len(queue)}")
        
        if step == 0: # BAK/OKU AŞAMASI [cite: 6]
            st.markdown(f"<div class='card'><div class='big-font'>{current_q['q']} = {current_q['a']}</div></div>", unsafe_allow_html=True)
            st.info("👁️ İşleme ve sonuca dikkatlice bak. Ezberleyince 'Kapat' butonuna bas.")
            if st.session_state.get('feedback') == 'WRONG':
                st.error("⚠️ Önceki cevabın yanlıştı. Lütfen tekrar dikkatle incele!")
            if st.button("🙈 Kapat ve Yaz", use_container_width=True):
                manager.generate_options()
                st.session_state['learning_step'] = 1
                st.rerun()
                
        elif step == 1: # KAPAT/KARŞILAŞTIR AŞAMASI [cite: 7, 8, 9]
            st.markdown(f"<div class='hidden-card'><div class='big-font'>{current_q['q']} = ?</div></div>", unsafe_allow_html=True)
            st.warning("👇 Doğru sonucu seç.")
            cols = st.columns(3)
            options = st.session_state['current_options']
            for i, opt in enumerate(options):
                if cols[i].button(str(opt), key=f"learn_opt_{i}", use_container_width=True):
                    manager.check_learning_answer(opt)
                    st.rerun()

    # 3. SEVİYE TAMAMLANDI
    elif phase == 'COMPLETED_LEARNING':
        st.balloons()
        current_diff = st.session_state['difficulty']
        st.success(f"Tebrikler! '{current_diff}' seviyesini başarıyla tamamladın! 🌟")
        levels = list(DIFFICULTY_LEVELS.keys())
        idx = levels.index(current_diff)
        if idx + 1 < len(levels):
            if st.button(f"⏩ Sonraki Seviyeye Geç ({levels[idx+1]})", type="primary", use_container_width=True):
                manager.next_level()
        else:
            st.info("🏆 Muhteşem! Tüm çarpım tablosu seviyelerini bitirdin.")
            if st.button("Ana Menüye Dön", use_container_width=True):
                manager.go_home()
                st.rerun()

    # 4. SINAV MODU (Sırayla ve Şıklı)
    elif phase == 'ASSESSMENT':
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        st.subheader(f"Yoklama Sorusu {q_idx + 1} / 10")
        st.markdown(f"<div class='card' style='border-color:#fbbf24;'><div class='big-font' style='color:#d97706;'>{current_q['q']} = ?</div></div>", unsafe_allow_html=True)
        st.write("")
        cols = st.columns(3)
        options = st.session_state['current_options']
        for i, opt in enumerate(options):
            if cols[i].button(str(opt), key=f"assess_opt_{q_idx}_{i}", use_container_width=True):
                manager.check_assessment_answer(opt)
                st.rerun()

    # 5. SINAV SONUCU
    elif phase == 'COMPLETED_ASSESSMENT':
        score = st.session_state['assessment_score']
        st.metric("Sınav Başarı Puanın", f"{score} / 10")
        if score == 10: 
            st.balloons()
            st.success("Harika! Hepsini doğru bildin! 🌟")
        elif score >= 7:
            st.info("Güzel bir sonuç! 👍")
        else:
            st.warning("Biraz daha pratik yapman gerekebilir. 💪")
        if st.button("Ana Menüye Dön", use_container_width=True):
            manager.go_home()
            st.rerun()

if __name__ == "__main__":
    main()
