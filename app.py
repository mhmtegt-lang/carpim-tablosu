import streamlit as st
import random

# --- 1. SAYFA YAPILANDIRMASI (İLK SATIRDA OLMALI) ---
st.set_page_config(page_title="KKK Matematik", page_icon="🎓", layout="centered")

# --- 2. VERİLER (KAYNAK: TABLO 3.1) ---
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

# --- 3. TASARIM (AYDINLIK TEMA VE KUTU YAPISI) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; }
    h1, h2, h3 { color: #4338ca !important; text-align: center; }
    .card {
        background-color: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center;
        margin-bottom: 20px; border: 1px solid #e0e7ff;
    }
    .big-font { font-size: 48px !important; font-weight: bold; color: #1e1b4b; }
    .hidden-card {
        background-color: #eef2ff; color: #4338ca; padding: 30px;
        border-radius: 20px; text-align: center; border: 2px dashed #c7d2fe;
    }
    div.stButton > button {
        width: 100%; height: 65px; font-size: 22px; font-weight: bold;
        border-radius: 12px; transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. İŞ MANTIĞI (LOGIC) ---
class CCCManager:
    def __init__(self):
        if 'manager_initialized' not in st.session_state:
            self._reset_state()
            st.session_state['manager_initialized'] = True

    def _reset_state(self):
        st.session_state.update({
            'current_phase': 'MENU', 'difficulty': 'Basit (2-5 Çarpanları)',
            'question_queue': [], 'current_q_index': 0, 'learning_step': 0,
            'feedback': None, 'assessment_score': 0, 'current_options': []
        })

    def generate_options(self, correct_ans):
        options = {correct_ans}
        while len(options) < 3:
            fake = correct_ans + random.randint(-5, 5)
            if fake > 0 and fake != correct_ans: options.add(fake)
        opt_list = list(options)
        random.shuffle(opt_list)
        st.session_state['current_options'] = opt_list

    def start_learning(self, difficulty):
        questions = DIFFICULTY_LEVELS[difficulty].copy()
        random.shuffle(questions)
        st.session_state.update({
            'difficulty': difficulty, 'question_queue': questions,
            'current_q_index': 0, 'learning_step': 0, 'current_phase': 'LEARNING', 'feedback': None
        })

    def start_assessment(self):
        all_q = [q for level in DIFFICULTY_LEVELS.values() for q in level]
        st.session_state.update({
            'question_queue': random.sample(all_q, 10), 'current_q_index': 0,
            'assessment_score': 0, 'current_phase': 'ASSESSMENT'
        })
        self.generate_options(st.session_state['question_queue'][0]['a'])

# --- 5. ARAYÜZ (VIEW) ---
def main():
    manager = CCCManager()
    phase = st.session_state['current_phase']

    st.title("🎓 Kapat - Kopyala - Karşılaştır")

    if phase == 'MENU':
        st.markdown('<div class="card"><h3>Hoşgeldin!</h3><p>Önce öğren, sonra kendini test et.</p></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div style="text-align:center;"><b>Öğrenme Modu</b></div>', unsafe_allow_html=True)
            diff = st.selectbox("Seviye Seç:", list(DIFFICULTY_LEVELS.keys()), label_visibility="collapsed")
            if st.button("📘 Başla", use_container_width=True):
                manager.start_learning(diff)
                st.rerun()
        with col2:
            st.markdown('<div style="text-align:center;"><b>Sınav Modu</b></div>', unsafe_allow_html=True)
            st.write("")
            if st.button("📝 Sınav Ol", type="primary", use_container_width=True):
                manager.start_assessment()
                st.rerun()

    elif phase == 'LEARNING':
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]
        step = st.session_state['learning_step']

        st.progress((q_idx) / len(queue))
        
        if step == 0: # GÖR
            st.markdown(f'<div class="card"><div class="big-font">{current_q["q"]} = {current_q["a"]}</div></div>', unsafe_allow_html=True)
            if st.session_state.get('feedback') == 'WRONG': st.error("⚠️ Yanlış cevap! Başa döndük.")
            if st.button("🙈 Kapat ve Seç", use_container_width=True):
                manager.generate_options(current_q['a'])
                st.session_state['learning_step'] = 1
                st.rerun()
        else: # SEÇ
            st.markdown(f'<div class="hidden-card"><div class="big-font">{current_q["q"]} = ?</div></div>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, opt in enumerate(st.session_state['current_options']):
                if cols[i].button(str(opt), key=f"L_{q_idx}_{i}"):
                    if opt == current_q['a']:
                        st.session_state['feedback'] = "CORRECT"
                        if q_idx < len(queue) - 1:
                            st.session_state['current_q_index'] += 1
                            st.session_state['learning_step'] = 0
                        else: st.session_state['current_phase'] = 'COMPLETED_LEARNING'
                    else:
                        st.session_state['feedback'] = "WRONG"
                        st.session_state['learning_step'] = 0
                    st.rerun()

    elif phase == 'ASSESSMENT':
        q_idx = st.session_state['current_q_index']
        queue = st.session_state['question_queue']
        current_q = queue[q_idx]

        st.markdown(f"### Soru {q_idx + 1} / 10")
        st.markdown(f'<div class="card" style="border-color:#fbbf24;"><div class="big-font" style="color:#b45309;">{current_q["q"]} = ?</div></div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(st.session_state['current_options']):
            if cols[i].button(str(opt), key=f"A_{q_idx}_{i}"):
                if opt == current_q['a']: st.session_state['assessment_score'] += 1
                if q_idx < len(queue) - 1:
                    st.session_state['current_q_index'] += 1
                    manager.generate_options(queue[q_idx+1]['a'])
                else: st.session_state['current_phase'] = 'COMPLETED_ASSESSMENT'
                st.rerun()

    elif phase.startswith('COMPLETED'):
        st.balloons()
        score_text = f"Puanın: {st.session_state['assessment_score']} / 10" if 'ASSESSMENT' in phase else "Seviye Tamamlandı!"
        st.markdown(f'<div class="card"><h2>🎉 Tebrikler!</h2><h3>{score_text}</h3></div>', unsafe_allow_html=True)
        if st.button("🏠 Ana Menüye Dön", use_container_width=True):
            manager._reset_state()
            st.rerun()

if __name__ == "__main__":
    main()
