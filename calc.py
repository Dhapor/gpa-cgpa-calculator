# 💄 1. Custom CSS for Styling
import streamlit as st

st.set_page_config(page_title="GPA/CGPA Calculator", layout="centered")


st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"]  {
            font-family: 'Montserrat', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

menu = st.selectbox(
    "Choose a page:",
    ["Home", "4.0 GPA/CGPA Calculator", "5.0 GPA/CGPA Calculator"]
)


def HomePage():
    # Streamlit app header
    st.markdown("<h5 style = 'text-align: center; font-family:montserrat'>Smart GPA & CGPA Calculator for University Students</h5>",unsafe_allow_html=True)
    st.markdown("<p style = 'margin: 10px; text-align: center ; font-family:montserrat'>A simple, interactive GPA & CGPA calculator for university students using the Nigerian grading system. Built with Streamlit, it lets students input scores across multiple semesters and sessions to instantly compute GPA and CGPA.</p>",unsafe_allow_html=True)
    st.image('smiling-woman-with-afro-posing-pink-sweater.jpg',  width = 800)
    # 👣 6. Footer
    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)



if menu == "Home":
    HomePage()
elif menu == "4.0 GPA/CGPA Calculator":
    st.markdown("""
        <style>
            .main {
                background-color: #f9f9fc;
            }
            h1 {
                color: #004085;
            }
            .stButton>button {
                background-color: #004085;
                color: white;
                border-radius: 8px;
            }
            .stNumberInput label {
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # 📌 2. Title
    st.title("🎓 4.0 GPA & CGPA Calculator")
    def get_grade_point(score):
        if score >= 85:
            return 'A', 4.0
        elif score >= 70:
            return 'B', 3.0
        elif score >= 60:
            return 'C', 2.0
        elif score >= 50:
            return 'D', 1.0
        else:
            return 'F', 0.0
    
    # 📚 3. Main App Logic
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
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    test_score = st.number_input("Test score", min_value=0.0, max_value=100.0, key=f"test_{s}_{sem}_{c}")
                with col2:
                    exam_score = st.number_input("Exam score", min_value=0.0, max_value=100.0, key=f"exam_{s}_{sem}_{c}")
                with col3:
                    unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{s}_{sem}_{c}")

                total_score = test_score + exam_score
                if total_score > 100:
                    st.warning(f"⚠ {course_name}: Total score cannot exceed 100. Skipping.")
                    continue

                grade, point = get_grade_point(total_score)
                st.write(f"{course_name} → Total: {total_score}, Grade: {grade}, GP: {point}")

                total_units += unit
                total_weighted_points += point * unit

            if total_units > 0:
                semester_gpa = total_weighted_points / total_units
                st.success(f"📊 GPA for Session {s}, Semester {sem}: {round(semester_gpa, 2)}")
                total_units_all += total_units
                total_weighted_points_all += total_weighted_points
            else:
                st.error("❌ No valid course entries for this semester.")

    # 🎯 5. Final Summary
    if total_units_all > 0:
        cgpa = total_weighted_points_all / total_units_all
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {semesters}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")
    # 👣 6. Footer
    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)


elif menu == "5.0 GPA/CGPA Calculator":
    st.markdown("""
        <style>
            .main {
                background-color: #f9f9fc;
            }
            h1 {
                color: #004085;
            }
            .stButton>button {
                background-color: #004085;
                color: white;
                border-radius: 8px;
            }
            .stNumberInput label {
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # 📌 2. Title
    st.title("🎓 5.0 GPA & CGPA Calculator")

    # 🧠 3. Helper Function
    def get_grade_point(score):
        if score >= 70:
            return 'A', 5.0
        elif score >= 60:
            return 'B', 4.0
        elif score >= 50:
            return 'C', 3.0
        elif score >= 45:
            return 'D', 2.0
        elif score >= 40:
            return 'E', 1.0
        else:
            return 'F', 0.0

    # 📚 4. Main App Logic
    total_units_all = 0
    total_weighted_points_all = 0

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.markdown(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")

        for sem in range(1, semesters + 1):
            st.markdown(f"### 📗 Semester {sem}")
            num_courses = st.number_input(f"Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            
            total_units = 0
            total_weighted_points = 0

            for c in range(1, num_courses + 1):
                st.markdown(f"#### 📚 Course {c}")
                course_name = st.text_input("Course name:", key=f"name_{s}_{sem}_{c}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    test_score = st.number_input("Test score", min_value=0.0, max_value=100.0, key=f"test_{s}_{sem}_{c}")
                with col2:
                    exam_score = st.number_input("Exam score", min_value=0.0, max_value=100.0, key=f"exam_{s}_{sem}_{c}")
                with col3:
                    unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{s}_{sem}_{c}")

                total_score = test_score + exam_score
                if total_score > 100:
                    st.warning(f"⚠ {course_name}: Total score cannot exceed 100. Skipping.")
                    continue

                grade, point = get_grade_point(total_score)
                st.write(f"{course_name} → Total: {total_score}, Grade: {grade}, GP: {point}")

                total_units += unit
                total_weighted_points += point * unit

            if total_units > 0:
                semester_gpa = total_weighted_points / total_units
                st.success(f"📊 GPA for Session {s}, Semester {sem}: {round(semester_gpa, 2)}")
                total_units_all += total_units
                total_weighted_points_all += total_weighted_points
            else:
                st.error("❌ No valid course entries for this semester.")

    # 🎯 5. Final Summary
    if total_units_all > 0:
        cgpa = total_weighted_points_all / total_units_all
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {semesters}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")

    # 👣 6. Footer
    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)
