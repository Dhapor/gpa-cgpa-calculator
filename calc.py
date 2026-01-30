from io import StringIO
import streamlit as st
import sqlite3
import hashlib
import datetime
import json
import requests

# App config
st.set_page_config(page_title="GPA/CGPA Calculator", layout="centered")

# Custom styling
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
        }
        .mobile-text {
            font-size: 16px;
            text-align: center;
            margin-top: 10px;
        }
        .success-box {
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            color: #155724;
        }
        .error-box {
            padding: 10px;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            color: #721c24;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== DATABASE SETUP ====================
def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Semesters table
    c.execute('''
        CREATE TABLE IF NOT EXISTS semesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            semester_name TEXT NOT NULL,
            gpa REAL NOT NULL,
            total_units INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Courses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            course_code TEXT,
            grade TEXT NOT NULL,
            units INTEGER NOT NULL,
            grade_point REAL NOT NULL,
            FOREIGN KEY (semester_id) REFERENCES semesters(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== AUTHENTICATION FUNCTIONS ====================
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    """Create a new user account"""
    try:
        conn = sqlite3.connect('cgpa_calculator.db')
        c = conn.cursor()
        password_hash = hash_password(password)
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                  (username, email, password_hash))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username or email already exists!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute('SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?',
              (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user

def get_user_id(username):
    """Get user ID from username"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# ==================== DATA STORAGE FUNCTIONS ====================
def save_semester_data(user_id, academic_year, semester_name, gpa, total_units, courses):
    """Save semester data to database"""
    try:
        conn = sqlite3.connect('cgpa_calculator.db')
        c = conn.cursor()
        
        # Insert semester
        c.execute('''
            INSERT INTO semesters (user_id, academic_year, semester_name, gpa, total_units)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, academic_year, semester_name, gpa, total_units))
        
        semester_id = c.lastrowid
        
        # Insert courses
        for course in courses:
            c.execute('''
                INSERT INTO courses (semester_id, course_name, course_code, grade, units, grade_point)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (semester_id, course['name'], course.get('code', ''), 
                  course['grade'], course['unit'], course['point']))
        
        conn.commit()
        conn.close()
        return True, "Semester data saved successfully!"
    except Exception as e:
        return False, f"Error saving data: {str(e)}"

def get_user_semesters(user_id):
    """Retrieve all semesters for a user"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, academic_year, semester_name, gpa, total_units, created_at
        FROM semesters
        WHERE user_id = ?
        ORDER BY academic_year, semester_name
    ''', (user_id,))
    semesters = c.fetchall()
    conn.close()
    return semesters

def get_semester_courses(semester_id):
    """Retrieve all courses for a semester"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    c.execute('''
        SELECT course_name, course_code, grade, units, grade_point
        FROM courses
        WHERE semester_id = ?
    ''', (semester_id,))
    courses = c.fetchall()
    conn.close()
    return courses

def calculate_overall_cgpa(user_id):
    """Calculate overall CGPA from all saved semesters"""
    conn = sqlite3.connect('cgpa_calculator.db')
    c = conn.cursor()
    c.execute('''
        SELECT SUM(gpa * total_units), SUM(total_units)
        FROM semesters
        WHERE user_id = ?
    ''', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result[0] and result[1]:
        return result[0] / result[1]
    return 0.0

# ==================== USAGE TRACKING (OPTIONAL) ====================
def log_activity(action, page):
    """
    Log user activity to Supabase for analytics
    This is completely optional and anonymous
    """
    try:
        # Check if Supabase credentials are configured
        if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
            return  # Skip logging if not configured
        
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        
        user_type = "guest" if st.session_state.get('guest_mode', False) else "registered"
        
        data = {
            "action": action,
            "user_type": user_type,
            "page": page,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        # Non-blocking request with timeout
        requests.post(
            f"{SUPABASE_URL}/rest/v1/usage_logs",
            json=data,
            headers=headers,
            timeout=2
        )
    except:
        # Silent fail - logging should never break the app
        pass

# ==================== SESSION STATE INITIALIZATION ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'guest_mode' not in st.session_state:
    st.session_state.guest_mode = False

# Initialize database
init_db()

# ==================== LOGIN/SIGNUP PAGE ====================
def auth_page():
    st.markdown("<h2 style='text-align: center;'>🎓 Welcome to CGPA Calculator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Calculate your GPA/CGPA easily with the Nigerian grading system</p>", unsafe_allow_html=True)
    
    # Guest Mode Option - Prominent
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Try it Now (Guest Mode)", type="primary", use_container_width=True):
            st.session_state.guest_mode = True
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.session_state.user_id = None
            log_activity("guest_mode_entered", "auth_page")
            st.rerun()
        
        st.caption("💡 Test the calculator without creating an account. Your data won't be saved.")
    
    st.markdown("---")
    st.markdown("<p style='text-align: center;'><strong>Want to save your records?</strong> Create an account below 👇</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to Your Account")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if login_username and login_password:
                user = verify_user(login_username, login_password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.guest_mode = False
                    st.session_state.username = user[1]
                    st.session_state.user_id = user[0]
                    log_activity("user_login", "auth_page")
                    st.success(f"Welcome back, {user[1]}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.warning("Please enter both username and password!")
    
    with tab2:
        st.subheader("Create New Account")
        signup_username = st.text_input("Choose Username", key="signup_username")
        signup_email = st.text_input("Email Address", key="signup_email")
        signup_password = st.text_input("Choose Password", type="password", key="signup_password")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
        
        if st.button("Sign Up", key="signup_btn"):
            if signup_username and signup_email and signup_password:
                if signup_password != signup_password_confirm:
                    st.error("Passwords do not match!")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    success, message = create_user(signup_username, signup_email, signup_password)
                    if success:
                        log_activity("user_signup", "auth_page")
                        st.success(message)
                        st.info("Please login with your new account!")
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields!")

# ==================== MAIN APP (AFTER LOGIN) ====================

# Navigation menu (only show if logged in)
if st.session_state.logged_in:
    # Sidebar with user info and logout
    with st.sidebar:
        if st.session_state.guest_mode:
            st.markdown("### 👤 Guest Mode")
            st.info("💡 You're using the app as a guest. Your data won't be saved.")
            st.markdown("**Want to save your records?**")
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.guest_mode = False
                st.rerun()
        else:
            st.markdown(f"### 👤 Welcome, {st.session_state.username}!")
            
            # Calculate and display overall CGPA
            overall_cgpa = calculate_overall_cgpa(st.session_state.user_id)
            st.metric("Your Overall CGPA", f"{overall_cgpa:.3f}")
            
            # Get total units
            semesters = get_user_semesters(st.session_state.user_id)
            total_units = sum([sem[4] for sem in semesters])
            st.metric("Total Units Completed", total_units)
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.guest_mode = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.rerun()
    
    # Menu options based on mode
    if st.session_state.guest_mode:
        menu = st.selectbox("Choose a page:", [
            "Homepage", 
            "GPA Calculator",
            "What Do I Need To Get?"
        ])
    else:
        menu = st.selectbox("Choose a page:", [
            "Homepage", 
            "Add New Semester", 
            "View My Records",
            "What Do I Need To Get?"
        ])

# --------------------------- HOME PAGE ----------------------------
def HomePage():
    st.markdown("<h5 style='text-align: center;'>Smart GPA & CGPA Calculator for University Students</h5>", unsafe_allow_html=True)
    st.markdown("<p class='mobile-text'>An interactive GPA & CGPA calculator using the Nigerian grading system. Built with Streamlit, it lets students compute GPA and CGPA easily across multiple sessions and semesters.</p>", unsafe_allow_html=True)
    
    # Try to load image, but don't break if it doesn't exist
    try:
        st.image("smiling-woman-with-afro-posing-pink-sweater.jpg", width=800)
    except:
        st.info("💡 Welcome! Use the menu above to add semesters or view your records.")
    
    # Show quick stats
    if st.session_state.logged_in:
        st.markdown("---")
        st.subheader("📊 Your Academic Summary")
        
        semesters = get_user_semesters(st.session_state.user_id)
        
        if semesters:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Semesters", len(semesters))
            with col2:
                total_units = sum([sem[4] for sem in semesters])
                st.metric("Total Units", total_units)
            with col3:
                overall_cgpa = calculate_overall_cgpa(st.session_state.user_id)
                st.metric("Overall CGPA", f"{overall_cgpa:.3f}")
        else:
            st.info("👋 You haven't added any semester data yet. Click 'Add New Semester' to get started!")
    
    st.markdown("<hr><p style='text-align: center;'>Built by Datapsalm & Victoria</p>", unsafe_allow_html=True)
    st.markdown("<hr><p style='text-align: center;'>datapsalm@gmail.com</p>", unsafe_allow_html=True)

# -------------------- GPA CALCULATOR (GUEST MODE) ---------------------
def GuestGPACalculator():
    try:
        st.image("SS.jpg", use_container_width=True)
    except:
        pass
    
    st.header("📝 GPA Calculator")
    st.markdown("Calculate your semester GPA quickly. Note: Your data won't be saved in guest mode.")

    # User Inputs
    scale = st.radio("Choose Grading Scale:", ("5.0 Scale", "4.0 Scale"))

    if scale == "5.0 Scale":
        grade_map = {'A':5.0, 'B':4.0, 'C':3.0, 'D':2.0, 'E':1.0, 'F':0.0}
        max_scale = 5.0
    else:
        grade_map = {'A':4.0, 'B':3.0, 'C':2.0, 'D':1.0, 'F':0.0}
        max_scale = 4.0

    num_courses = st.number_input("Number of courses:", min_value=1, max_value=15, step=1, key="num_courses_guest")
    
    semester_units = 0
    semester_points = 0
    courses_list = []

    for c in range(1, num_courses + 1):
        st.markdown(f"**Course {c}**")
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            course_name = st.text_input("Course name", key=f"name_guest_{c}", placeholder="e.g., Introduction to Programming")
        with col2:
            grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_guest_{c}")
        with col3:
            unit = st.number_input("Units", min_value=1, max_value=6, step=1, key=f"unit_guest_{c}")

        point = grade_map[grade_input]
        
        if course_name:
            semester_units += unit
            semester_points += point * unit
            courses_list.append({
                "name": course_name,
                "grade": grade_input,
                "unit": unit,
                "point": point
            })

    if courses_list:
        semester_gpa = semester_points / semester_units if semester_units > 0 else 0
        
        st.markdown("---")
        st.subheader(f"📊 Your GPA: {semester_gpa:.3f}")
        st.write(f"Total Units: {semester_units}")
        
        # Log this calculation
        log_activity("calculate_gpa", "guest_calculator")
        
        # Download option
        result_txt = StringIO()
        result_txt.write(f"GPA Calculation Report\n")
        result_txt.write("-"*50 + "\n\n")
        
        for course in courses_list:
            result_txt.write(f"{course['name']}\n")
            result_txt.write(f"Grade: {course['grade']} | Units: {course['unit']} | GP: {course['point']}\n\n")
        
        result_txt.write(f"\nGPA: {semester_gpa:.3f}\n")
        result_txt.write(f"Total Units: {semester_units}\n")
        result_txt.write("\nGenerated by: GPA/CGPA App by Datapsalm & Victoria\n")
        
        st.download_button(
            "📥 Download Report",
            result_txt.getvalue(),
            f"gpa_report.txt",
            "text/plain"
        )
        
        st.info("💡 Want to save this semester for future reference? Create an account to track all your semesters!")
def AddNewSemester():
    try:
        st.image("SS.jpg", use_container_width=True)
    except:
        pass
    
    st.header("📝 Add New Semester")
    st.markdown("Enter your semester details and courses. Your data will be automatically saved to your account.")

    # Semester info
    col1, col2 = st.columns(2)
    with col1:
        academic_year = st.text_input("Academic Year (e.g., 2023/2024)", key="academic_year")
    with col2:
        semester_name = st.selectbox("Semester", [
            "First Semester",
            "Second Semester"
        ], key="semester_name")

    # User Inputs
    scale = st.radio("Choose Grading Scale:", ("5.0 Scale", "4.0 Scale"))

    if scale == "5.0 Scale":
        grade_map = {'A':5.0, 'B':4.0, 'C':3.0, 'D':2.0, 'E':1.0, 'F':0.0}
        max_scale = 5.0
    else:
        grade_map = {'A':4.0, 'B':3.0, 'C':2.0, 'D':1.0, 'F':0.0}
        max_scale = 4.0

    num_courses = st.number_input("Number of courses:", min_value=1, max_value=15, step=1, key="num_courses")
    
    semester_units = 0
    semester_points = 0
    courses_list = []

    for c in range(1, num_courses + 1):
        st.markdown(f"**Course {c}**")
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        with col1:
            course_name = st.text_input("Course name", key=f"name_{c}", placeholder="e.g., Introduction to Programming")
        with col2:
            course_code = st.text_input("Course code (optional)", key=f"code_{c}", placeholder="e.g., CSC101")
        with col3:
            grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_{c}")
        with col4:
            unit = st.number_input("Units", min_value=1, max_value=6, step=1, key=f"unit_{c}")

        point = grade_map[grade_input]
        
        if course_name:  # Only add if course name is provided
            semester_units += unit
            semester_points += point * unit
            courses_list.append({
                "name": course_name,
                "code": course_code,
                "grade": grade_input,
                "unit": unit,
                "point": point
            })

    if courses_list:
        semester_gpa = semester_points / semester_units if semester_units > 0 else 0
        
        st.markdown("---")
        st.subheader(f"📊 Semester GPA: {semester_gpa:.3f}")
        st.write(f"Total Units: {semester_units}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Semester", type="primary"):
                if academic_year:
                    success, message = save_semester_data(
                        st.session_state.user_id,
                        academic_year,
                        semester_name,
                        semester_gpa,
                        semester_units,
                        courses_list
                    )
                    if success:
                        log_activity("save_semester", "add_semester")
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter the academic year!")
        
        with col2:
            # Download option
            result_txt = StringIO()
            result_txt.write(f"Semester Report - {academic_year} {semester_name}\n")
            result_txt.write("-"*50 + "\n\n")
            
            for course in courses_list:
                result_txt.write(f"{course['name']} ({course['code']})\n")
                result_txt.write(f"Grade: {course['grade']} | Units: {course['unit']} | GP: {course['point']}\n\n")
            
            result_txt.write(f"\nSemester GPA: {semester_gpa:.3f}\n")
            result_txt.write(f"Total Units: {semester_units}\n")
            result_txt.write("\nGenerated by: GPA/CGPA App by Datapsalm & Victoria\n")
            
            st.download_button(
                "📥 Download Report",
                result_txt.getvalue(),
                f"semester_report_{academic_year.replace('/', '_')}_{semester_name.replace(' ', '_')}.txt",
                "text/plain"
            )

# -------------------- VIEW RECORDS ---------------------
def ViewRecords():
    st.header("📚 My Academic Records")
    
    semesters = get_user_semesters(st.session_state.user_id)
    
    if not semesters:
        st.info("You haven't added any semester records yet. Go to 'Add New Semester' to start!")
        return
    
    # Overall stats
    overall_cgpa = calculate_overall_cgpa(st.session_state.user_id)
    total_units = sum([sem[4] for sem in semesters])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Overall CGPA", f"{overall_cgpa:.3f}")
    with col2:
        st.metric("📖 Total Units", total_units)
    with col3:
        st.metric("📅 Semesters", len(semesters))
    
    st.markdown("---")
    
    # Group semesters by academic year
    years = {}
    for sem in semesters:
        year = sem[1]  # academic_year
        if year not in years:
            years[year] = []
        years[year].append(sem)
    
    # Display by year
    for year, year_semesters in years.items():
        st.subheader(f"🎓 Academic Year: {year}")
        
        for sem in year_semesters:
            sem_id, acad_year, sem_name, gpa, units, created = sem
            
            with st.expander(f"{sem_name} - GPA: {gpa:.3f} ({units} units)"):
                courses = get_semester_courses(sem_id)
                
                if courses:
                    st.markdown("**Courses:**")
                    for course in courses:
                        course_name, course_code, grade, course_units, gp = course
                        code_display = f"({course_code})" if course_code else ""
                        st.write(f"• {course_name} {code_display} - Grade: {grade}, Units: {course_units}, GP: {gp}")
                
                st.caption(f"Added on: {created}")
        
        st.markdown("---")
    
    # Export all records
    if st.button("📥 Export All Records"):
        result_txt = StringIO()
        result_txt.write(f"Complete Academic Records - {st.session_state.username}\n")
        result_txt.write("="*60 + "\n\n")
        result_txt.write(f"Overall CGPA: {overall_cgpa:.3f}\n")
        result_txt.write(f"Total Units: {total_units}\n")
        result_txt.write(f"Total Semesters: {len(semesters)}\n\n")
        result_txt.write("="*60 + "\n\n")
        
        for year, year_semesters in years.items():
            result_txt.write(f"ACADEMIC YEAR: {year}\n")
            result_txt.write("-"*60 + "\n\n")
            
            for sem in year_semesters:
                sem_id, acad_year, sem_name, gpa, units, created = sem
                result_txt.write(f"{sem_name}\n")
                result_txt.write(f"GPA: {gpa:.3f} | Units: {units}\n\n")
                
                courses = get_semester_courses(sem_id)
                for course in courses:
                    course_name, course_code, grade, course_units, gp = course
                    code_display = f"({course_code})" if course_code else ""
                    result_txt.write(f"  {course_name} {code_display}\n")
                    result_txt.write(f"  Grade: {grade} | Units: {course_units} | GP: {gp}\n\n")
                
                result_txt.write("\n")
            result_txt.write("\n")
        
        result_txt.write("\nGenerated by: GPA/CGPA App by Datapsalm & Victoria\n")
        
        st.download_button(
            "Download Complete Records",
            result_txt.getvalue(),
            f"complete_records_{st.session_state.username}.txt",
            "text/plain"
        )

# -------------------- WHAT DO I NEED FEATURE ---------------------
def WhatDoINeed():
    try:
        st.image("RR.jpg", use_container_width=True)
    except:
        pass

    st.header("🎯 What Do I Need To Reach My Target CGPA?")
    st.markdown("Plan your grades for the upcoming semesters to reach your desired CGPA.")

    # Auto-fill current CGPA if user has records
    current_cgpa_auto = calculate_overall_cgpa(st.session_state.user_id)
    semesters = get_user_semesters(st.session_state.user_id)
    completed_credits_auto = sum([sem[4] for sem in semesters])
    
    if current_cgpa_auto > 0:
        st.info(f"📊 Your current CGPA is {current_cgpa_auto:.3f} with {completed_credits_auto} completed units")
        use_auto = st.checkbox("Use my current CGPA and units", value=True)
    else:
        use_auto = False
    
    if use_auto:
        current_cgpa = current_cgpa_auto
        completed_credits = completed_credits_auto
        st.write(f"Using: CGPA = {current_cgpa:.3f}, Units = {completed_credits}")
    else:
        current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=5.0, step=0.001, format="%.3f")
        completed_credits = st.number_input("Total completed Units:", min_value=0, step=1)
    
    st.markdown("**Upcoming Semester 1**")
    sem1_credits = st.number_input("Total Units for Semester 1:", min_value=1, step=1)
    
    st.markdown("**Upcoming Semester 2**")
    sem2_credits = st.number_input("Total Units for Semester 2:", min_value=1, step=1)
    
    target_cgpa = st.number_input("🎯 Target CGPA:", min_value=0.0, max_value=5.0, step=0.001, format="%.3f")

    if st.button("Calculate Required GPA", type="primary"):
        total_future_credits = sem1_credits + sem2_credits
        total_units_all = completed_credits + total_future_credits
        total_points_needed = target_cgpa * total_units_all
        points_remaining = total_points_needed - (current_cgpa * completed_credits)
        
        equal_gpa = points_remaining / total_future_credits
        
        # Scenario 1
        sem1_lower = equal_gpa * 0.9
        sem2_higher = (points_remaining - sem1_lower * sem1_credits) / sem2_credits
        
        # Scenario 2
        sem1_higher = equal_gpa * 1.1
        sem2_lower = (points_remaining - sem1_higher * sem1_credits) / sem2_credits
        
        st.markdown("---")
        st.subheader("📋 Suggested GPA Plans for Next 2 Semesters")

        st.markdown(f"**Option 1** (Equal GPA Both Semesters):")
        st.write(f"Semester 1: {equal_gpa:.3f}  |  Semester 2: {equal_gpa:.3f}")
        
        st.markdown(f"**Option 2** (Start Lower, Finish Higher):")
        st.write(f"Semester 1: {sem1_lower:.3f}  |  Semester 2: {sem2_higher:.3f}")
        
        st.markdown(f"**Option 3** (Start Higher, Finish Lower):")
        st.write(f"Semester 1: {sem1_higher:.3f}  |  Semester 2: {sem2_lower:.3f}")

        st.markdown("---")
        
        if equal_gpa > 5:
            st.error("❌ This target is not achievable in the next 2 semesters (required GPA > 5.0).")
        elif equal_gpa >= 4.8:
            st.warning("⚠️ Extremely challenging: You must score nearly all A's across both semesters.")
        elif equal_gpa >= 4.0:
            st.info("💪 High performance needed: Mostly A's and some B's.")
        else:
            st.success("✅ Achievable target with good performance.")

    st.markdown("<hr><p style='text-align: center;'>Built by Datapsalm & Victoria</p>", unsafe_allow_html=True)


# ------------------ ROUTING -----------------------
if not st.session_state.logged_in:
    auth_page()
else:
    if st.session_state.guest_mode:
        # Guest mode routing
        if menu == "Homepage":
            HomePage()
        elif menu == "GPA Calculator":
            GuestGPACalculator()
        elif menu == "What Do I Need To Get?":
            WhatDoINeed()
    else:
        # Logged-in user routing
        if menu == "Homepage":
            HomePage()
        elif menu == "Add New Semester":
            AddNewSemester()
        elif menu == "View My Records":
            ViewRecords()
        elif menu == "What Do I Need To Get?":
            WhatDoINeed()
