import streamlit as st
import random
import time

# --- VERİLER (DATA) ---
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
        st.session_state['current_options'] = [] # Şıklar için yeni hafıza

    def start_learning_mode(self, difficulty: str):
        st.session_state['difficulty'] = difficulty
        questions = DIFFICULTY_LEVELS[difficulty].copy()
        random.shuffle(questions)
        st.session_state['question_queue'] = questions
        st.session_state['current_q_index'] = 0
        st.session_state['learning_step'] = 0
        st.session_state['current_phase'] = 'LEARNING'
        st.session_state['feedback'] = None

    def generate_options(self):
        """Doğru cevabın yanına 2 tane mantıklı yanlış cevap üretir."""
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        correct_ans = current_q['a']
        
        # Yanlış cevapları üret (Cevaba yakın sayılar seçelim)
        options = {correct_ans} # Küme kullanarak tekrarı önle
        while len(options) < 3:
            # Cevabın biraz altı veya biraz üstü rastgele sayılar
            fake = correct_ans + random.randint(-5, 5)
            if fake > 0 and fake != correct_ans:
                options.add(fake)
        
        # Şıkları listeye çevir ve karıştır
        opt_list = list(options)
        random.shuffle(opt_list)
        st.session_state['current_options'] = opt_list

    def check_learning_answer(self, user_answer):
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        
        if int(user_answer) == current_q['a']:
            st.session_state['feedback'] = "CORRECT"
            if st.session_state['current_q_index'] < len(st.session_state['question_queue']) - 1:
                st.session_state['current_q_index'] += 1
                st.session_state['learning_step'] = 0 # Başa sar (Bak)
            else:
                st.session_state['current_phase'] = 'COMPLETED_LEARNING'
        else:
            st.session_state['feedback'] = "WRONG"
            # KURAL: Yanlışta başa dön (Bak-Kapat-Seç)
            st.session_state['learning_step'] = 0 

    # ... Diğer metodlar aynı kalacak (Assessment logic vb.) ...
    def start_assessment_mode(self):
        all_questions = []
        for level in DIFFICULTY_LEVELS.values():
            all_questions.extend(level)
        selected_questions = random.sample(all_questions, 10)
        st.session_state['question_queue'] = selected_questions
        st.session_state['current_phase'] = 'ASSESSMENT'
        st.session_state['assessment_answers'] = {}

    def submit_assessment(self, user_answers_dict):
        score = 0
        results = []
        for idx, q in enumerate(st.session_state['question_queue']):
            u_ans = user_answers_dict.get(idx)
            is_correct = False
            try:
                if u_ans is not None and int(u_ans) == q['a']:
                    score += 1
                    is_correct = True
            except:
                pass
            results.append({"q": q, "user": u_ans, "correct": is_correct})
        st.session_state['assessment_results'] = results
        st.session_state['assessment_score'] = score
        st.session_state['current_phase'] = 'COMPLETED_ASSESSMENT'

    def go_home(self):
        self._reset_state()

# --- ARAYÜZ (UI) ---
st.set_page_config(page_title="KKK Matematik", page_icon="✖️", layout="centered")

st.markdown("""
<style>
    .big-font { font-size:40px !important; font-weight:bold; text-align:center; color:#333; }
    .card { background-color: #f0f2f6; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .hidden-card { background-color: #e3f2fd; color: #1565c0; padding: 30px; border-radius: 15px; text-align: center; border: 3px solid #90caf9; user-select: none;}
    /* Butonları büyütmek için CSS */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    manager = CCCManager()
    phase = st.session_state['current_phase']

    st.title("🎓 Çarpım Tablosu")
    
    if phase == 'MENU':
        st.info("Çarpım tablosunu ezberlemek için bir mod seçin.")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📚 Öğrenme Modu")
            diff = st.selectbox("Seviye:", list(DIFFICULTY_LEVELS.keys()))
            if st.button("Başla (Öğrenme)", use_container_width=True):
                manager.start_learning_mode(diff)
                st.rerun()
        with col2:
            st.subheader("📝 Sınav Modu")
            st.write("Karışık 10 soru ile kendini dene.")
            if st.button("Başla (Sınav)", type="primary", use_container_width=True):
                manager.start_assessment_mode()
                st.rerun()

    elif phase == 'LEARNING':
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        step = st.session_state['learning_step']
        
        st.progress((q_idx) / len(queue), text=f"İlerleme: {q_idx}/{len(queue)}")
        
        if step == 0: # GÖR (SHOW)
            st.markdown(f"<div class='card'><div class='big-font'>{current_q['q']} = {current_q['a']}</div></div>", unsafe_allow_html=True)
            st.info("👁️ İşleme BAK. Ezberleyince 'Kapat' de.")
            
            if st.session_state.get('feedback') == 'WRONG':
                st.error("⚠️ Yanlış cevap! Başa döndük, tekrar incele.")
            
            if st.button("🙈 Kapat ve Seç", use_container_width=True):
                manager.generate_options() # Şıkları oluştur
                st.session_state['learning_step'] = 1
                st.rerun()
                
        elif step == 1: # KAPAT & SEÇ (COVER & SELECT)
            st.markdown(f"<div class='hidden-card'><div class='big-font'>{current_q['q']} = ?</div></div>", unsafe_allow_html=True)
            st.warning("👇 Doğru cevabı seç.")
            
            # ŞIKLARI GÖSTER (3 Buton Yan Yana)
            cols = st.columns(3)
            options = st.session_state['current_options']
            
            for i, opt in enumerate(options):
                if cols[i].button(str(opt), use_container_width=True):
                    manager.check_learning_answer(opt)
                    st.rerun()

    elif phase == 'COMPLETED_LEARNING':
        st.balloons()
        st.success("Tebrikler! Bu seviyeyi bitirdin.")
        if st.button("Başa Dön"):
            manager.go_home()
            st.rerun()

    elif phase == 'ASSESSMENT':
        st.subheader("Yoklama Kağıdı")
        st.caption("Sınavda klasik usul yazarak cevaplıyoruz.")
        with st.form("exam"):
            answers = {}
            cols = st.columns(2)
            for i, q in enumerate(st.session_state['question_queue']):
                with cols[i % 2]:
                    answers[i] = st.number_input(f"{q['q']} = ?", key=f"e_{i}", step=1)
            if st.form_submit_button("Sınavı Bitir"):
                manager.submit_assessment(answers)
                st.rerun()

    elif phase == 'COMPLETED_ASSESSMENT':
        score = st.session_state['assessment_score']
        st.metric("Puanın", f"{score} / 10")
        
        if score == 10: 
            st.balloons()
            st.success("Mükemmel! 🌟")
        elif score >= 7:
            st.info("Gayet iyi! 👍")
        else:
            st.warning("Biraz daha pratik yapmalısın. 💪")

        if st.button("Tamam"):
            manager.go_home()
            st.rerun()

if __name__ == "__main__":
    main()
