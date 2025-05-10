import os
import base64
import requests
import streamlit as st
from io import StringIO



# App config
st.set_page_config(page_title="🎓 GPA/CGPA Calculator", layout="centered")

# Load secrets
GITHUB_TOKEN = st.secrets["github"]["token"]
USERNAME = st.secrets["github"]["username"]
REPO_NAME = st.secrets["github"]["repo"]
FILE_PATH = st.secrets["github"]["file_path"]


# Function to get current user count from GitHub
def get_user_count():
    url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode('utf-8')
        return int(decoded_content.strip())
    else:
        # If file doesn't exist, treat it as 0
        return 0

# Function to increment and update user count in GitHub
def increment_user_count():
    current_count = get_user_count()
    updated_count = current_count + 1

    url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    response = requests.get(url, headers=headers)
    sha = response.json().get('sha') if response.status_code == 200 else None

    # Encode new count
    encoded_content = base64.b64encode(str(updated_count).encode()).decode()

    data = {
        'message': 'Update user count',
        'content': encoded_content,
        'branch': 'main'
    }

    if sha:
        data['sha'] = sha  # Include SHA only if file exists

    update_response = requests.put(url, headers=headers, json=data)

    if update_response.status_code in [200, 201]:
        return updated_count
    else:
        st.error(f"❌ Failed to update user count: {update_response.status_code}\n{update_response.text}")
        return current_count

# Only increment once per user session
if 'user_tracked' not in st.session_state:
    count = increment_user_count()
    st.session_state['user_tracked'] = True
else:
    count = get_user_count()

# Display at bottom of the app
st.markdown("---")
st.markdown(f"<p style='text-align:center; color:gray;'>👥 <strong>Total Users:</strong> {count}</p>", unsafe_allow_html=True)

# Rest of your app code below...



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
    </style>
""", unsafe_allow_html=True)

# Navigation menu
menu = st.selectbox("Choose a page:", ["Home", "4.0 GPA/CGPA Calculator", "5.0 GPA/CGPA Calculator"])

# --------------------------- HOME PAGE ----------------------------
def HomePage():
    st.markdown("<h5 style='text-align: center;'>Smart GPA & CGPA Calculator for University Students</h5>", unsafe_allow_html=True)
    st.markdown("<p class='mobile-text'>An interactive GPA & CGPA calculator using the Nigerian grading system. Built with Streamlit, it lets students compute GPA and CGPA easily across multiple sessions and semesters.</p>", unsafe_allow_html=True)
    st.image("smiling-woman-with-afro-posing-pink-sweater.jpg", width=800)
    st.markdown("<hr><p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria</p>", unsafe_allow_html=True)

# -------------------- GPA/CGPA CALCULATOR FUNCTION ---------------------
def GPACalculator(scale_name, grade_map):
    st.header(f"🎓 {scale_name} GPA & CGPA Calculator")

    total_units_all = 0
    total_weighted_points_all = 0
    total_semesters = 0
    total_courses = 0
    session_data = []

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.subheader(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")
        total_semesters += semesters

        for sem in range(1, semesters + 1):
            st.markdown(f"### 📗 Semester {sem}")
            num_courses = st.number_input("Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            total_courses += num_courses

            total_units = 0
            total_weighted_points = 0
            semester_courses = []

            for c in range(1, num_courses + 1):
                st.markdown(f"#### 📚 Course {c}")
                course_name = st.text_input("Course name:", key=f"name_{s}_{sem}_{c}")

                col1, col2 = st.columns(2)
                with col1:
                    grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_{s}_{sem}_{c}")
                with col2:
                    unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{s}_{sem}_{c}")

                point = grade_map[grade_input]
                st.write(f"{course_name} → Grade: {grade_input}, GP: {point}")
                total_units += unit
                total_weighted_points += point * unit

                semester_courses.append({
                    "name": course_name,
                    "grade": grade_input,
                    "unit": unit,
                    "point": point
                })

            if total_units > 0:
                semester_gpa = total_weighted_points / total_units
                st.success(f"📊 GPA for Session {s}, Semester {sem}: {round(semester_gpa, 2)}")
                total_units_all += total_units
                total_weighted_points_all += total_weighted_points
            else:
                st.error("❌ No valid course entries for this semester.")

            session_data.append({
                "session": s,
                "semester": sem,
                "total_units": total_units,
                "total_weighted_points": total_weighted_points,
                "courses": semester_courses
            })

    # ------------------ FINAL SUMMARY ------------------
    if total_units_all > 0:
        cgpa = total_weighted_points_all / total_units_all
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {total_semesters}")
        st.markdown(f"**Total Courses:** {total_courses}")
        st.markdown(f"**Total Units:** {total_units_all}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")

    # ------------------ DOWNLOAD REPORT ------------------
    if session_data:
        result_txt = StringIO()
        result_txt.write("📘 GPA & CGPA Report\n" + "-" * 30 + "\n")

        for semester in session_data:
            result_txt.write(f"\nSession {semester['session']} - Semester {semester['semester']}\n")
            result_txt.write("-" * 30 + "\n")
            for course in semester["courses"]:
                result_txt.write(f"{course['name']} | Grade: {course['grade']} | Unit: {course['unit']} | GP: {course['point']}\n")
            gpa = semester["total_weighted_points"] / semester["total_units"] if semester["total_units"] else 0
            result_txt.write(f"Semester GPA: {round(gpa, 2)}\n")

        result_txt.write("\n🎯 Final Summary\n" + "-" * 30 + "\n")
        result_txt.write(f"Total Sessions: {sessions}\n")
        result_txt.write(f"Total Semesters: {total_semesters}\n")
        result_txt.write(f"Total Courses: {total_courses}\n")
        result_txt.write(f"Total Units: {total_units_all}\n")
        result_txt.write(f"Final CGPA: {round(cgpa, 2)}\n")
        result_txt.write("-" * 30 + "\n")
        result_txt.write("Generated by: GPA/CGPA App by Datapsalm & Victoria\n")

        st.download_button("📄 Download Readable Report (TXT)", result_txt.getvalue(), "gpa_report.txt", "text/plain")

    st.markdown("<hr><p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria</p>", unsafe_allow_html=True)

# ------------------ ROUTING -----------------------
if menu == "Home":
    HomePage()
elif menu == "4.0 GPA/CGPA Calculator":
    grade_map_4 = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    GPACalculator("4.0", grade_map_4)
elif menu == "5.0 GPA/CGPA Calculator":
    grade_map_5 = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0}
    GPACalculator("5.0", grade_map_5)
