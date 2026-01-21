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
        st.session_state['current_options'] = []

    def start_learning_mode(self, difficulty: str):
        st.session_state['difficulty'] = difficulty
        questions = DIFFICULTY_LEVELS[difficulty].copy()
        random.shuffle(questions)
        st.session_state['question_queue'] = questions
        st.session_state['current_q_index'] = 0
        st.session_state['learning_step'] = 0
        st.session_state['current_phase'] = 'LEARNING'
        st.session_state['feedback'] = None

    def next_level(self):
        """Mevcut seviyeyi bulup bir sonrakine geçer."""
        levels = list(DIFFICULTY_LEVELS.keys())
        current_diff = st.session_state['difficulty']
        
        try:
            current_index = levels.index(current_diff)
            # Eğer son seviye değilse bir sonrakine geç
            if current_index + 1 < len(levels):
                next_diff = levels[current_index + 1]
                self.start_learning_mode(next_diff)
                st.rerun()
            else:
                self.go_home()
        except ValueError:
            self.go_home()

    def generate_options(self):
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

    def check_learning_answer(self, user_answer):
        current_q = st.session_state['question_queue'][st.session_state['current_q_index']]
        if int(user_answer) == current_q['a']:
            st.session_state['feedback'] = "CORRECT"
            if st.session_state['current_q_index'] < len(st.session_state['question_queue']) - 1:
                st.session_state['current_q_index'] += 1
                st.session_state['learning_step'] = 0
            else:
                st.session_state['current_phase'] = 'COMPLETED_LEARNING'
        else:
            st.session_state['feedback'] = "WRONG"
            st.session_state['learning_step'] = 0 

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
    phase = st.session_state
