from io import StringIO
import streamlit as st
import hashlib
import datetime
import requests
import json

# App config
st.set_page_config(
    page_title="GPA/CGPA Calculator", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling with background image and mobile responsiveness
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
                        url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1600') center/cover no-repeat fixed;
        }
        
        @media (max-width: 768px) {
            .stApp {
                background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)),
                            url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800') center/cover no-repeat fixed;
            }
        }
        
        .hero-section {
            text-align: center;
            padding: 2rem 1rem;
            background: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            color: #333;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px solid #f0f0f0;
        }
        
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
            font-weight: 400;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .hero-title { font-size: 1.8rem; }
            .hero-subtitle { font-size: 0.95rem; }
            .hero-section { padding: 1.5rem 0.75rem; }
        }
        
        /* ACTION CARDS - The big clickable ones on landing */
        .action-card {
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 20px;
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.15);
            margin-bottom: 1rem;
            text-align: center;
            border: 2px solid #f0f0f0;
            transition: all 0.3s ease;
        }
        
        .action-card:hover {
            border-color: #667eea;
            box-shadow: 0 10px 35px rgba(102, 126, 234, 0.25);
            transform: translateY(-4px);
        }
        
        .action-card .card-icon {
            font-size: 3rem;
            margin-bottom: 0.75rem;
            display: block;
        }
        
        .action-card .card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.4rem;
        }
        
        .action-card .card-desc {
            font-size: 0.9rem;
            color: #777;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        @media (max-width: 768px) {
            .action-card { padding: 1.5rem 1rem; }
            .action-card .card-icon { font-size: 2.5rem; }
            .action-card .card-title { font-size: 1.2rem; }
        }

        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 4px solid #667eea;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        .feature-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .feature-title { font-size: 1.3rem; font-weight: 600; color: #333; margin-bottom: 0.5rem; }
        .feature-desc { font-size: 0.95rem; color: #666; line-height: 1.6; }
        
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 2rem;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        @media (max-width: 768px) {
            [data-testid="stMetricValue"] { font-size: 1.5rem; }
            [data-testid="stMetricLabel"] { font-size: 0.85rem; }
        }
        
        .success-box {
            padding: 1rem;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .tutorial-step {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        
        .step-number {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: 700;
            margin-right: 1rem;
            font-size: 1.2rem;
        }
        
        @media (max-width: 768px) {
            .feature-card { padding: 1rem; }
            .tutorial-step { padding: 1rem; }
            .step-number { width: 35px; height: 35px; line-height: 35px; font-size: 1rem; }
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: 600; }
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ==================== SUPABASE CONFIGURATION ====================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    SUPABASE_CONFIGURED = True
except:
    st.warning("⚠️ Database not configured. You can still use the calculator, but data won't be saved.")
    SUPABASE_CONFIGURED = False

if SUPABASE_CONFIGURED:
    HEADERS = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

# ==================== SUPABASE HELPER FUNCTIONS ====================
def supabase_request(method, endpoint, data=None, params=None):
    if not SUPABASE_CONFIGURED:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, headers=HEADERS, json=data, params=params, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json() if response.text else []
    except requests.exceptions.RequestException as e:
        st.error(f"Database error: {str(e)}")
        return None

# ==================== AUTHENTICATION FUNCTIONS ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    try:
        password_hash = hash_password(password)
        data = {"username": username, "email": email, "password_hash": password_hash}
        result = supabase_request("POST", "users", data)
        if result:
            return True, "Account created successfully!"
        else:
            return False, "Username or email already exists!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    try:
        password_hash = hash_password(password)
        params = {
            "username": f"eq.{username}",
            "password_hash": f"eq.{password_hash}",
            "select": "id,username,email"
        }
        result = supabase_request("GET", "users", params=params)
        if result and len(result) > 0:
            user = result[0]
            return (user['id'], user['username'], user['email'])
        return None
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None

# ==================== DATA STORAGE FUNCTIONS ====================
def save_semester_data(user_id, academic_year, semester_name, gpa, total_units, courses):
    try:
        semester_data = {
            "user_id": user_id,
            "academic_year": academic_year,
            "semester_name": semester_name,
            "gpa": float(gpa),
            "total_units": int(total_units)
        }
        semester_result = supabase_request("POST", "semesters", semester_data)
        if not semester_result or len(semester_result) == 0:
            return False, "Failed to save semester"
        semester_id = semester_result[0]['id']
        for course in courses:
            course_data = {
                "semester_id": semester_id,
                "course_name": course['name'],
                "course_code": course.get('code', ''),
                "grade": course['grade'],
                "units": int(course['unit']),
                "grade_point": float(course['point'])
            }
            supabase_request("POST", "courses", course_data)
        return True, "Semester data saved successfully!"
    except Exception as e:
        return False, f"Error saving data: {str(e)}"

def get_user_semesters(user_id):
    try:
        params = {
            "user_id": f"eq.{user_id}",
            "select": "id,academic_year,semester_name,gpa,total_units,created_at",
            "order": "academic_year,semester_name"
        }
        result = supabase_request("GET", "semesters", params=params)
        return result if result else []
    except Exception as e:
        st.error(f"Error fetching semesters: {str(e)}")
        return []

def get_semester_courses(semester_id):
    try:
        params = {
            "semester_id": f"eq.{semester_id}",
            "select": "course_name,course_code,grade,units,grade_point"
        }
        result = supabase_request("GET", "courses", params=params)
        return result if result else []
    except Exception as e:
        st.error(f"Error fetching courses: {str(e)}")
        return []

def calculate_overall_cgpa(user_id):
    try:
        semesters = get_user_semesters(user_id)
        if not semesters:
            return 0.0
        total_points = sum(sem['gpa'] * sem['total_units'] for sem in semesters)
        total_units = sum(sem['total_units'] for sem in semesters)
        return total_points / total_units if total_units > 0 else 0.0
    except Exception as e:
        st.error(f"Error calculating CGPA: {str(e)}")
        return 0.0

# ==================== SESSION STATE INITIALIZATION ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'show_tutorial' not in st.session_state:
    st.session_state.show_tutorial = False
# NEW: track which calculator to open directly
if 'start_tab' not in st.session_state:
    st.session_state.start_tab = None

# ==================== WELCOME PAGE (LANDING PAGE) ====================
def welcome_page():
    """Landing page — action cards go directly to GPA or CGPA calculator"""
    
    # Hero
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🎓 GPA & CGPA Calculator</div>
            <div class="hero-subtitle">Calculate your grades easily using the Nigerian grading system</div>
        </div>
    """, unsafe_allow_html=True)

    # ── TWO BIG ACTION CARDS ──────────────────────────────────────────
    st.markdown("### 👇 What do you want to calculate?")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="action-card">
                <span class="card-icon">📊</span>
                <div class="card-title">Single Semester GPA</div>
                <div class="card-desc">Enter your courses for one semester and get your GPA instantly</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate GPA →", key="btn_gpa", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.start_tab = "gpa"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="action-card">
                <span class="card-icon">📈</span>
                <div class="card-title">Multiple Semesters CGPA</div>
                <div class="card-desc">Enter grades from 2 or more semesters and get your overall CGPA</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Calculate CGPA →", key="btn_cgpa", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.start_tab = "cgpa"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Third smaller card: Goal Planning
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="action-card">
                <span class="card-icon">🎯</span>
                <div class="card-title">Goal Planning</div>
                <div class="card-desc">Find out what grades you need to hit your target CGPA</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Plan My Grades →", key="btn_goal", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.start_tab = "goal"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Tutorial button (smaller, secondary)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📚 How To Use", use_container_width=True):
            st.session_state.show_tutorial = True
            st.rerun()

    # Benefits section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Why Use This Calculator?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - ✅ **No signup required** — Start using immediately
        - ✅ **Save your progress** — Optional account to keep records
        - ✅ **Mobile friendly** — Works perfectly on phones
        """)
    with col2:
        st.markdown("""
        - ✅ **Nigerian system** — 5.0 and 4.0 grading scales
        - ✅ **Download reports** — Export your results
        - ✅ **Free forever** — No hidden charges
        """)

    # Optional signup
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("💾 Want to save your records permanently? Create an account"):
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="login_btn"):
                if login_username and login_password:
                    user = verify_user(login_username, login_password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = user[1]
                        st.session_state.user_id = user[0]
                        st.success(f"Welcome back, {user[1]}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                else:
                    st.warning("Please enter both username and password!")
        with tab2:
            signup_username = st.text_input("Choose Username", key="signup_username")
            signup_email = st.text_input("Email Address", key="signup_email")
            signup_password = st.text_input("Choose Password", type="password", key="signup_password")
            signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            if st.button("Sign Up", key="signup_btn"):
                if signup_username and signup_email and signup_password:
                    if signup_password != signup_password_confirm:
                        st.error("Passwords do not match!")
                    elif len(signup_password) < 6:
                        st.error("Password must be at least 6 characters!")
                    else:
                        success, message = create_user(signup_username, signup_email, signup_password)
                        if success:
                            st.success(message)
                            st.info("Please login with your new account!")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields!")

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p style='font-size: 0.9rem; margin-bottom: 10px;'>
                <strong>Built by Mathematics Students</strong><br>
                Department of Mathematics, University of Lagos 🎓<br>
                © 2024 | Crafted with 💙 for students
            </p>
            <p style='font-size: 0.85rem; margin-top: 15px;'>
                <strong>Developers:</strong><br>
                <a href='https://www.linkedin.com/in/datapsalm' target='_blank' style='color: #667eea; text-decoration: none;'>
                    🔗 Datapsalm (LinkedIn)
                </a> | 
                <a href='https://www.linkedin.com/in/victoria-xxxxxxx' target='_blank' style='color: #667eea; text-decoration: none;'>
                    🔗 Victoria (LinkedIn)
                </a>
            </p>
            <p style='font-size: 0.8rem; margin-top: 10px; color: #999;'>
                📧 Contact: datapsalm@gmail.com
            </p>
        </div>
    """, unsafe_allow_html=True)


# ==================== TUTORIAL PAGE ====================
def tutorial_page():
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">📚 How To Use This Calculator</div>
            <div class="hero-subtitle">A simple guide to get you started</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tutorial-step">
            <span class="step-number">1</span>
            <strong style="font-size: 1.2rem;">Choose Your Grading Scale</strong>
            <p style="margin-top: 0.5rem; color: #666;">
            Select between 5.0 scale (A=5.0) or 4.0 scale (A=4.0). Most Nigerian universities use 5.0 scale.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tutorial-step">
            <span class="step-number">2</span>
            <strong style="font-size: 1.2rem;">Enter Your Courses</strong>
            <p style="margin-top: 0.5rem; color: #666;">
            For each course, enter:<br>
            • Course code (e.g., "MAT101", "PHY102")<br>
            • Your grade (A, B, C, D, E, or F)<br>
            • Course units (usually 2–4 units per course)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tutorial-step">
            <span class="step-number">3</span>
            <strong style="font-size: 1.2rem;">Calculate GPA or CGPA</strong>
            <p style="margin-top: 0.5rem; color: #666;">
            • <strong>GPA</strong>: For one semester only<br>
            • <strong>CGPA</strong>: For multiple semesters (calculates your overall grade)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tutorial-step">
            <span class="step-number">4</span>
            <strong style="font-size: 1.2rem;">Plan Your Future Grades</strong>
            <p style="margin-top: 0.5rem; color: #666;">
            Use "Plan My Grades" to find out what GPA you need in upcoming semesters to reach your target CGPA.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tutorial-step">
            <span class="step-number">5</span>
            <strong style="font-size: 1.2rem;">Save Your Progress (Optional)</strong>
            <p style="margin-top: 0.5rem; color: #666;">
            Create a free account to save all your semesters and track your academic progress over time.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Example: How to Calculate Your GPA"):
        st.markdown("""
        **Scenario:** You took 5 courses this semester
        
        1. **MAT101** - Grade: A, Units: 3
        2. **PHY101** - Grade: B, Units: 4
        3. **CHM101** - Grade: A, Units: 3
        4. **ENG101** - Grade: C, Units: 2
        5. **CSC101** - Grade: B, Units: 4
        
        **On 5.0 scale:**
        - A = 5.0, B = 4.0, C = 3.0
        - Total Points = (5.0×3) + (4.0×4) + (5.0×3) + (3.0×2) + (4.0×4) = 72
        - Total Units = 3 + 4 + 3 + 2 + 4 = 16
        - **GPA = 72 ÷ 16 = 4.50**
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Got It! Let's Start Calculating", type="primary", use_container_width=True):
            st.session_state.show_tutorial = False
            st.session_state.logged_in = True
            st.rerun()
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.show_tutorial = False
            st.rerun()


# ==================== MAIN CALCULATOR PAGE ====================
def main_calculator():
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        st.markdown("### 🎓 GPA Calculator")
    with col3:
        if st.session_state.user_id:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_id = None
                st.session_state.start_tab = None
                st.rerun()
        else:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.start_tab = None
                st.rerun()

    if st.session_state.user_id:
        overall_cgpa = calculate_overall_cgpa(st.session_state.user_id)
        semesters = get_user_semesters(st.session_state.user_id)
        total_units = sum([sem['total_units'] for sem in semesters])
        st.markdown(f"**Welcome back, {st.session_state.username}!** 👋")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 CGPA", f"{overall_cgpa:.3f}")
        with col2:
            st.metric("📖 Units", total_units)
        with col3:
            st.metric("📅 Semesters", len(semesters))
        st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Calculate GPA/CGPA", "🎯 What Do I Need?", "📚 My Records", "ℹ️ Tutorial"])

    with tab1:
        calculate_gpa_cgpa()
    with tab2:
        what_do_i_need()
    with tab3:
        if st.session_state.user_id:
            view_records()
        else:
            st.info("📝 Create a free account to save and view your academic records!")
            show_signup_inline()
    with tab4:
        quick_tutorial()


# ==================== GPA/CGPA CALCULATOR ====================
def calculate_gpa_cgpa():
    st.markdown("### Calculate Your Grades")

    # If user came from a landing card, pre-select the right mode
    if st.session_state.start_tab == "gpa":
        default_calc = "📊 Single Semester GPA"
    elif st.session_state.start_tab == "cgpa":
        default_calc = "📈 Multiple Semesters CGPA"
    else:
        default_calc = "📊 Single Semester GPA"

    options = ["📊 Single Semester GPA", "📈 Multiple Semesters CGPA"]
    calc_type = st.radio(
        "What would you like to calculate?",
        options,
        index=options.index(default_calc),
        horizontal=True
    )

    scale = st.radio("Choose Grading Scale:", ("5.0 Scale", "4.0 Scale"), horizontal=True)

    if scale == "5.0 Scale":
        grade_map = {'A':5.0, 'B':4.0, 'C':3.0, 'D':2.0, 'E':1.0, 'F':0.0}
    else:
        grade_map = {'A':4.0, 'B':3.0, 'C':2.0, 'D':1.0, 'F':0.0}

    if calc_type == "📊 Single Semester GPA":
        calculate_single_gpa(grade_map)
    else:
        calculate_multi_semester_cgpa(grade_map)


def calculate_single_gpa(grade_map):
    st.markdown("#### Enter Your Semester Details")
    with st.expander("📝 Semester Information (Optional)"):
        col1, col2 = st.columns(2)
        with col1:
            academic_year = st.text_input("Academic Year", placeholder="e.g., 2023/2024")
        with col2:
            semester_name = st.selectbox("Semester", ["First Semester", "Second Semester"])

    num_courses = st.number_input("Number of courses:", min_value=1, max_value=20, value=5, step=1)
    st.markdown("---")
    st.markdown("#### Your Courses")

    semester_units = 0
    semester_points = 0
    courses_list = []

    for c in range(1, num_courses + 1):
        with st.container():
            st.markdown(f"**Course {c}**")
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                course_code = st.text_input("Course Code", key=f"code_{c}", placeholder="e.g., MAT101")
            with col2:
                grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_{c}")
            with col3:
                unit = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"unit_{c}")
            point = grade_map[grade_input]
            if course_code:
                semester_units += unit
                semester_points += point * unit
                courses_list.append({"name": course_code, "code": course_code, "grade": grade_input, "unit": unit, "point": point})

    if courses_list:
        semester_gpa = semester_points / semester_units if semester_units > 0 else 0
        st.markdown("---")
        st.markdown("### 📊 Your Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("GPA", f"{semester_gpa:.3f}")
        with col2:
            st.metric("Total Units", semester_units)
        with col3:
            st.metric("Total Points", f"{semester_points:.1f}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.user_id and academic_year:
                if st.button("💾 Save This Semester", type="primary", use_container_width=True):
                    success, message = save_semester_data(
                        st.session_state.user_id, academic_year, semester_name,
                        semester_gpa, semester_units, courses_list
                    )
                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
            elif not st.session_state.user_id:
                st.info("💡 Create account to save")
        with col2:
            report = generate_report(
                academic_year if 'academic_year' in locals() else "N/A",
                semester_name if 'semester_name' in locals() else "N/A",
                semester_gpa, semester_units, courses_list
            )
            st.download_button("📥 Download Report", report, "gpa_report.txt", "text/plain", use_container_width=True)
        with col3:
            if st.button("🔄 Calculate Another", use_container_width=True):
                st.rerun()


def calculate_multi_semester_cgpa(grade_map):
    st.markdown("#### Calculate Your Overall CGPA")
    st.info("💡 Enter grades for 2 or more semesters to calculate your cumulative GPA")

    num_semesters = st.number_input("How many semesters?", min_value=2, max_value=12, value=2, step=1)
    all_semesters_data = []
    total_all_points = 0
    total_all_units = 0

    for sem_num in range(1, num_semesters + 1):
        st.markdown(f"### 📅 Semester {sem_num}")
        with st.expander(f"Enter courses for Semester {sem_num}", expanded=(sem_num == 1)):
            col1, col2 = st.columns(2)
            with col1:
                academic_year = st.text_input("Academic Year", key=f"year_{sem_num}", placeholder="2023/2024")
            with col2:
                semester_name = st.selectbox("Semester", ["First Semester", "Second Semester"], key=f"semname_{sem_num}")

            num_courses = st.number_input(f"Number of courses in Semester {sem_num}:", min_value=1, max_value=15, value=5, step=1, key=f"numcourses_{sem_num}")
            semester_units = 0
            semester_points = 0
            courses_list = []

            for c in range(1, num_courses + 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    course_code = st.text_input("Course Code", key=f"sem{sem_num}_code_{c}", placeholder="e.g., MAT101")
                with col2:
                    grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"sem{sem_num}_grade_{c}")
                with col3:
                    unit = st.number_input("Units", min_value=1, max_value=6, value=3, step=1, key=f"sem{sem_num}_unit_{c}")
                point = grade_map[grade_input]
                if course_code:
                    semester_units += unit
                    semester_points += point * unit
                    courses_list.append({"name": course_code, "code": course_code, "grade": grade_input, "unit": unit, "point": point})

            if courses_list:
                semester_gpa = semester_points / semester_units if semester_units > 0 else 0
                st.success(f"✅ Semester {sem_num} GPA: **{semester_gpa:.3f}** ({semester_units} units)")
                total_all_points += semester_points
                total_all_units += semester_units
                all_semesters_data.append({"year": academic_year, "name": semester_name, "gpa": semester_gpa, "units": semester_units, "courses": courses_list})

    if total_all_units > 0:
        overall_cgpa = total_all_points / total_all_units
        st.markdown("---")
        st.markdown("### 🎓 Your Overall CGPA")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CGPA", f"{overall_cgpa:.3f}")
        with col2:
            st.metric("Total Units", total_all_units)
        with col3:
            st.metric("Semesters", len(all_semesters_data))

        with st.expander("📊 Semester Breakdown"):
            for idx, sem in enumerate(all_semesters_data, 1):
                st.write(f"**Semester {idx}**: {sem['year']} {sem['name']} - GPA: {sem['gpa']:.3f} ({sem['units']} units)")

        cgpa_report = generate_cgpa_report(all_semesters_data, overall_cgpa, total_all_units)
        st.download_button("📥 Download Full CGPA Report", cgpa_report, "cgpa_report.txt", "text/plain", use_container_width=True, type="primary")

        if st.session_state.user_id:
            if st.button("💾 Save All Semesters", use_container_width=True):
                success_count = 0
                for sem in all_semesters_data:
                    success, msg = save_semester_data(st.session_state.user_id, sem['year'], sem['name'], sem['gpa'], sem['units'], sem['courses'])
                    if success:
                        success_count += 1
                if success_count == len(all_semesters_data):
                    st.success(f"✅ All {success_count} semesters saved successfully!")
                    st.balloons()
                else:
                    st.warning(f"Saved {success_count} out of {len(all_semesters_data)} semesters")


# ==================== WHAT DO I NEED ====================
def what_do_i_need():
    st.markdown("### 🎯 Plan Your Future Grades")
    st.info("Find out what GPA you need in upcoming semesters to reach your target CGPA")

    if st.session_state.user_id:
        current_cgpa_auto = calculate_overall_cgpa(st.session_state.user_id)
        semesters = get_user_semesters(st.session_state.user_id)
        completed_credits_auto = sum([sem['total_units'] for sem in semesters])
        if current_cgpa_auto > 0:
            st.success(f"📊 Your current CGPA: **{current_cgpa_auto:.3f}** with **{completed_credits_auto}** completed units")
            use_auto = st.checkbox("Use my current data", value=True)
        else:
            use_auto = False
        if use_auto:
            current_cgpa = current_cgpa_auto
            completed_credits = completed_credits_auto
        else:
            col1, col2 = st.columns(2)
            with col1:
                current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=5.0, step=0.01, format="%.2f")
            with col2:
                completed_credits = st.number_input("Completed Units:", min_value=0, step=1)
    else:
        col1, col2 = st.columns(2)
        with col1:
            current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=5.0, step=0.01, format="%.2f")
        with col2:
            completed_credits = st.number_input("Completed Units:", min_value=0, step=1)

    st.markdown("#### Upcoming Semesters")
    col1, col2 = st.columns(2)
    with col1:
        sem1_credits = st.number_input("Semester 1 Units:", min_value=1, value=18, step=1)
    with col2:
        sem2_credits = st.number_input("Semester 2 Units:", min_value=1, value=18, step=1)

    target_cgpa = st.number_input("🎯 Target CGPA:", min_value=0.0, max_value=5.0, value=4.5, step=0.01, format="%.2f")

    if st.button("Calculate Required GPAs", type="primary", use_container_width=True):
        total_future_credits = sem1_credits + sem2_credits
        total_units_all = completed_credits + total_future_credits
        total_points_needed = target_cgpa * total_units_all
        points_remaining = total_points_needed - (current_cgpa * completed_credits)
        equal_gpa = points_remaining / total_future_credits

        sem1_lower = equal_gpa * 0.9
        sem2_higher = (points_remaining - sem1_lower * sem1_credits) / sem2_credits
        if sem2_higher > 5.0:
            sem2_higher = 5.0
            sem1_lower = (points_remaining - sem2_higher * sem2_credits) / sem1_credits

        sem1_higher = equal_gpa * 1.1
        sem2_lower = (points_remaining - sem1_higher * sem1_credits) / sem2_credits
        if sem1_higher > 5.0:
            sem1_higher = 5.0
            sem2_lower = (points_remaining - sem1_higher * sem1_credits) / sem2_credits

        st.markdown("---")
        st.markdown("### 📋 Your GPA Plans")

        if equal_gpa > 5.0:
            st.error("❌ This target is NOT achievable in 2 semesters")
            st.warning(f"Even with perfect 5.0 GPA in both semesters, you would only reach {((current_cgpa * completed_credits) + (5.0 * total_future_credits)) / total_units_all:.2f} CGPA")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Option 1: Equal**")
                st.metric("Sem 1", f"{equal_gpa:.2f}" if equal_gpa <= 5.0 else "Not Possible")
                st.metric("Sem 2", f"{equal_gpa:.2f}" if equal_gpa <= 5.0 else "Not Possible")
            with col2:
                st.markdown("**Option 2: Start Lower**")
                st.metric("Sem 1", f"{sem1_lower:.2f}" if sem1_lower <= 5.0 else "> 5.0 ❌")
                st.metric("Sem 2", f"{sem2_higher:.2f}" if sem2_higher <= 5.0 else "> 5.0 ❌")
            with col3:
                st.markdown("**Option 3: Start Higher**")
                st.metric("Sem 1", f"{sem1_higher:.2f}" if sem1_higher <= 5.0 else "> 5.0 ❌")
                st.metric("Sem 2", f"{sem2_lower:.2f}" if sem2_lower <= 5.0 else "> 5.0 ❌")

            st.markdown("---")
            if equal_gpa >= 4.8:
                st.warning("⚠️ Extremely challenging: You need nearly all A's in both semesters")
            elif equal_gpa >= 4.0:
                st.info("💪 High performance needed: Mostly A's and some B's")
            else:
                st.success("✅ Achievable with good performance")


# ==================== VIEW RECORDS ====================
def view_records():
    semesters = get_user_semesters(st.session_state.user_id)
    if not semesters:
        st.info("📚 You haven't saved any records yet. Add semesters to start tracking!")
        return

    overall_cgpa = calculate_overall_cgpa(st.session_state.user_id)
    total_units = sum([sem['total_units'] for sem in semesters])

    st.markdown("### 📊 Your Academic Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall CGPA", f"{overall_cgpa:.3f}")
    with col2:
        st.metric("Total Units", total_units)
    with col3:
        st.metric("Semesters", len(semesters))

    st.markdown("---")
    years = {}
    for sem in semesters:
        year = sem['academic_year']
        if year not in years:
            years[year] = []
        years[year].append(sem)

    for year, year_semesters in years.items():
        st.markdown(f"### 🎓 {year}")
        for sem in year_semesters:
            with st.expander(f"{sem['semester_name']} - GPA: {sem['gpa']:.3f} ({sem['total_units']} units)"):
                courses = get_semester_courses(sem['id'])
                for course in courses:
                    code = f"({course.get('course_code', '')})" if course.get('course_code') else ""
                    st.write(f"• **{course['course_name']}** {code} - Grade: {course['grade']}, Units: {course['units']}")

    if st.button("📥 Export All Records", use_container_width=True):
        report = generate_full_records_report(st.session_state.username, overall_cgpa, total_units, years)
        st.download_button("Download Complete Records", report, f"records_{st.session_state.username}.txt", "text/plain")


# ==================== QUICK TUTORIAL ====================
def quick_tutorial():
    st.markdown("### 📚 Quick Guide")
    with st.expander("📊 How to Calculate GPA", expanded=True):
        st.markdown("""
        1. Select **Single Semester GPA**
        2. Choose your grading scale (5.0 or 4.0)
        3. Enter each course code, grade, and units
        4. Your GPA is calculated automatically!
        """)
    with st.expander("📈 How to Calculate CGPA"):
        st.markdown("""
        1. Select **Multiple Semesters CGPA**
        2. Enter the number of semesters
        3. For each semester, add all courses
        4. Your overall CGPA is calculated!
        """)
    with st.expander("🎯 How to Use Goal Planning"):
        st.markdown("""
        1. Enter your current CGPA and completed units
        2. Enter units for your next 2 semesters
        3. Set your target CGPA
        4. See what grades you need to reach your goal!
        """)
    with st.expander("💾 How to Save Your Records"):
        st.markdown("""
        1. Create a free account
        2. Calculate your semester GPA/CGPA
        3. Click "Save This Semester"
        4. View all records in "My Records" tab
        """)


# ==================== HELPER FUNCTIONS ====================
def generate_report(year, semester, gpa, units, courses):
    report = StringIO()
    report.write("SEMESTER REPORT\n" + "="*50 + "\n\n")
    report.write(f"Academic Year: {year}\nSemester: {semester}\nGPA: {gpa:.3f}\nTotal Units: {units}\n\n")
    report.write("-"*50 + "\nCOURSES\n" + "-"*50 + "\n\n")
    for course in courses:
        code = f"({course.get('code', '')})" if course.get('code') else ""
        report.write(f"{course['name']} {code}\nGrade: {course['grade']} | Units: {course['unit']} | GP: {course['point']}\n\n")
    report.write("\n" + "="*50 + "\nGenerated by GPA/CGPA Calculator\nBuilt by Mathematics Students, University of Lagos (2024)\nDevelopers: Datapsalm & Victoria\nContact: datapsalm@gmail.com\n")
    return report.getvalue()

def generate_cgpa_report(semesters, cgpa, total_units):
    report = StringIO()
    report.write(f"CUMULATIVE GPA REPORT\n" + "="*60 + "\n\n")
    report.write(f"Overall CGPA: {cgpa:.3f}\nTotal Units: {total_units}\nTotal Semesters: {len(semesters)}\n\n" + "="*60 + "\n\n")
    for idx, sem in enumerate(semesters, 1):
        report.write(f"SEMESTER {idx}: {sem['year']} {sem['name']}\n" + "-"*60 + "\n")
        report.write(f"GPA: {sem['gpa']:.3f} | Units: {sem['units']}\n\n")
        for course in sem['courses']:
            code = f"({course.get('code', '')})" if course.get('code') else ""
            report.write(f"  {course['name']} {code}\n  Grade: {course['grade']} | Units: {course['unit']}\n\n")
        report.write("\n")
    report.write("="*60 + "\nGenerated by GPA/CGPA Calculator\nBuilt by Mathematics Students, University of Lagos (2024)\nDevelopers: Datapsalm & Victoria\n")
    return report.getvalue()

def generate_full_records_report(username, cgpa, total_units, years):
    report = StringIO()
    report.write(f"COMPLETE ACADEMIC RECORDS\nStudent: {username}\n" + "="*60 + "\n\n")
    report.write(f"Overall CGPA: {cgpa:.3f}\nTotal Units: {total_units}\n\n" + "="*60 + "\n\n")
    for year, semesters in years.items():
        report.write(f"ACADEMIC YEAR: {year}\n" + "-"*60 + "\n\n")
        for sem in semesters:
            report.write(f"{sem['semester_name']}\nGPA: {sem['gpa']:.3f} | Units: {sem['total_units']}\n\n")
            courses = get_semester_courses(sem['id'])
            for course in courses:
                code = f"({course.get('course_code', '')})" if course.get('course_code') else ""
                report.write(f"  {course['course_name']} {code}\n  Grade: {course['grade']} | Units: {course['units']}\n\n")
            report.write("\n")
    report.write("="*60 + "\nGenerated by GPA/CGPA Calculator\nBuilt by Mathematics Students, University of Lagos (2024)\n")
    return report.getvalue()

def show_signup_inline():
    with st.expander("Create Free Account"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", key="inline_username")
            email = st.text_input("Email", key="inline_email")
        with col2:
            password = st.text_input("Password", type="password", key="inline_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="inline_password_confirm")
        if st.button("Create Account", key="inline_signup"):
            if username and email and password:
                if password != password_confirm:
                    st.error("Passwords don't match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    success, message = create_user(username, email, password)
                    if success:
                        st.success(message)
                        st.info("Please refresh and login!")
                    else:
                        st.error(message)


# ==================== MAIN APP ROUTING ====================
if not st.session_state.logged_in:
    if st.session_state.show_tutorial:
        tutorial_page()
    else:
        welcome_page()
else:
    # If coming from goal planning card, switch to goal tab
    if st.session_state.start_tab == "goal":
        # Can't programmatically switch Streamlit tabs, so show a banner
        st.info("👆 Click on **🎯 What Do I Need?** tab above to plan your grades!")
        st.session_state.start_tab = None
    main_calculator()
