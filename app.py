import streamlit as st
import random
import time

# --- SAYFA AYARLARI (EN BAŞTA OLMALI) ---
st.set_page_config(page_title="KKK Matematik", page_icon="🎓", layout="centered")

# --- VERİLER ---
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

# --- TASARIM (CSS) ---
# Burası gönderdiğin görseldeki "Aydınlık Tema"yı zorunlu kılar.
st.markdown("""
<style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #f4f6f9;
    }
    
    /* Başlıklar ve Yazılar */
    h1, h2, h3, p {
        color: #1e3a8a !important;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Kart Tasarımı (Beyaz Kutular) */
    .card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #e0e7ff;
    }
    
    /* Soru Metni */
    .big-font {
        font-size: 50px !important;
        font-weight: 800;
        color: #2563eb;
    }
    
    /* Butonlar */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 24px;
        font-weight: 600;
        border-radius: 15px;
        background-color: #ffffff;
        color: #1e3a8a;
        border: 2px solid #cbd5e1;
        transition: all 0.3s ease;
    }
    
    /* Butonun üzerine gelince */
    div.stButton > button:hover {
        background-color: #eff6ff;
        border-color: #2563eb;
        color: #2563eb;
        transform: translateY(-2px);
    }

    /* Gizli Kart */
    .hidden-card {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 2px dashed #7dd3fc;
    }
</style>
""", unsafe_allow_html=True)

# --- İŞ MANTIĞI ---
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
                st.session_state['learning_step'] = 0
            else:
                st.session_state['current_phase'] = 'COMPLETED_LEARNING'
        else:
            st.session_state['feedback'] = "WRONG"
            st.session_state['learning_step'] = 0

    def next_level(self):
        levels = list(DIFFICULTY_LEVELS.keys())
        current_diff = st.session_state['difficulty']
        try:
