# 💄 1. Custom CSS for Styling
import streamlit as st

st.set_page_config(page_title="GPA/CGPA Calculator", layout="centered")

# Adding custom CSS for mobile-friendly font size
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

menu = st.selectbox(
    "Choose a page:",
    ["Home", "4.0 GPA/CGPA Calculator", "5.0 GPA/CGPA Calculator"]
)

def HomePage():
    st.markdown("<h5 style = 'text-align: center; font-family:montserrat'>Smart GPA & CGPA Calculator for University Students</h5>", unsafe_allow_html=True)
    st.markdown("<p class='mobile-text'>A simple, interactive GPA & CGPA calculator for university students using the Nigerian grading system. Built with Streamlit, it lets students input grades across multiple semesters and sessions to instantly compute GPA and CGPA.</p>", unsafe_allow_html=True)
    st.image('smiling-woman-with-afro-posing-pink-sweater.jpg', width=800)
    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)

if menu == "Home":
    HomePage()

elif menu == "4.0 GPA/CGPA Calculator":
    st.header("🎓 4.0 GPA & CGPA Calculator")

    grade_map = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }

    total_units_all = 0
    total_weighted_points_all = 0

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.subheader(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")

        for sem in range(1, semesters + 1):
            st.markdown(f"### 📗 Semester {sem}")
            num_courses = st.number_input(f"Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            
            total_units = 0
            total_weighted_points = 0

            for c in range(1, num_courses + 1):
                st.markdown(f"#### 📚 Course {c}")
                course_name = st.text_input("Course name:", key=f"name_{s}_{sem}_{c}")
                
                col1, col2 = st.columns(2)
                with col1:
                    grade_input = st.selectbox("Grade (A-F)", ["A", "B", "C", "D", "F"], key=f"grade_{s}_{sem}_{c}")
                with col2:
                    unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{s}_{sem}_{c}")

                point = grade_map.get(grade_input, 0.0)
                st.write(f"{course_name} → Grade: {grade_input}, GP: {point}")

                total_units += unit
                total_weighted_points += point * unit

            if total_units > 0:
                semester_gpa = total_weighted_points / total_units
                st.success(f"📊 GPA for Session {s}, Semester {sem}: {round(semester_gpa, 2)}")
                total_units_all += total_units
                total_weighted_points_all += total_weighted_points
            else:
                st.error("❌ No valid course entries for this semester.")

    if total_units_all > 0:
        cgpa = total_weighted_points_all / total_units_all
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {semesters}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")

    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)

elif menu == "5.0 GPA/CGPA Calculator":
    st.header("🎓 5.0 GPA & CGPA Calculator")

    grade_map = {
        'A': 5.0,
        'B': 4.0,
        'C': 3.0,
        'D': 2.0,
        'E': 1.0,
        'F': 0.0
    }

    total_units_all = 0
    total_weighted_points_all = 0

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.subheader(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")

        for sem in range(1, semesters + 1):
            st.markdown(f"### 📗 Semester {sem}")
            num_courses = st.number_input(f"Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            
            total_units = 0
            total_weighted_points = 0

            for c in range(1, num_courses + 1):
                st.markdown(f"#### 📚 Course {c}")
                course_name = st.text_input("Course name:", key=f"name_{s}_{sem}_{c}")
                
                col1, col2 = st.columns(2)
                with col1:
                    grade_input = st.selectbox("Grade (A-F)", ["A", "B", "C", "D", "E", "F"], key=f"grade_{s}_{sem}_{c}")
                with col2:
                    unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{s}_{sem}_{c}")

                point = grade_map.get(grade_input, 0.0)
                st.write(f"{course_name} → Grade: {grade_input}, GP: {point}")

                total_units += unit
                total_weighted_points += point * unit

            if total_units > 0:
                semester_gpa = total_weighted_points / total_units
                st.success(f"📊 GPA for Session {s}, Semester {sem}: {round(semester_gpa, 2)}")
                total_units_all += total_units
                total_weighted_points_all += total_weighted_points
            else:
                st.error("❌ No valid course entries for this semester.")

    if total_units_all > 0:
        cgpa = total_weighted_points_all / total_units_all
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {semesters}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")

    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)
