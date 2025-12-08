from io import StringIO
import streamlit as st

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
    </style>
""", unsafe_allow_html=True)

# Navigation menu
menu = st.selectbox("Choose a page:", ["Homepage", "GPA Calculator", "What Do I Need To Get?"])

# --------------------------- HOME PAGE ----------------------------
def HomePage():
    st.markdown("<h5 style='text-align: center;'>Smart GPA & CGPA Calculator for University Students</h5>", unsafe_allow_html=True)
    st.markdown("<p class='mobile-text'>An interactive GPA & CGPA calculator using the Nigerian grading system. Built with Streamlit, it lets students compute GPA and CGPA easily across multiple sessions and semesters.</p>", unsafe_allow_html=True)
    st.image("smiling-woman-with-afro-posing-pink-sweater.jpg", width=800)
    st.markdown("<hr><p style='text-align: center;'>Built by Datapsalm & Victoria</p>", unsafe_allow_html=True)
    st.markdown("<hr><p style='text-align: center;'>datapsalm@gmail.com</p>", unsafe_allow_html=True)

# -------------------- UPDATE CGPA WITH SEMESTER GRADES ---------------------
def GPACalculator():
    st.image("SS.jpg", use_container_width=True)
    st.header("Update Your CGPA with Semester Grades")
    st.markdown("Enter your current CGPA and completed units (or 0 if you're a fresher), then input the grades and units for your current/future semester(s). The app will calculate your updated CGPA.")

    # User Inputs
    scale = st.radio("Choose Grading Scale:", ("5.0 Scale", "4.0 Scale"))

    if scale == "5.0 Scale":
        grade_map = {'A':5.0, 'B':4.0, 'C':3.0, 'D':2.0, 'E':1.0, 'F':0.0}
        max_scale = 5.0
    else:
        grade_map = {'A':4.0, 'B':3.0, 'C':2.0, 'D':1.0, 'F':0.0}
        max_scale = 4.0

    current_cgpa = st.number_input(f"Current CGPA (0 if fresher) [max {max_scale}]:", min_value=0.0, max_value=max_scale, step=0.001, format="%.3f")
    completed_units = st.number_input("Total completed Units (0 if fresher):", min_value=0, step=1)

    semesters_to_input = st.number_input("Number of upcoming semesters to enter grades for:", min_value=1, step=1)

    semester_data = []
    total_new_units = 0
    total_new_points = 0

    for sem in range(1, semesters_to_input + 1):
        st.markdown(f"Semester {sem}")
        num_courses = st.number_input(f"Number of courses in Semester {sem}:", min_value=1, step=1, key=f"num_courses_{sem}")
        
        semester_units = 0
        semester_points = 0
        courses_list = []

        for c in range(1, num_courses + 1):
            st.markdown(f"Course {c}")
            course_name = st.text_input("Course name:", key=f"name_{sem}_{c}")
            col1, col2 = st.columns(2)
            with col1:
                grade_input = st.selectbox("Grade", list(grade_map.keys()), key=f"grade_{sem}_{c}")
            with col2:
                unit = st.number_input("Course unit", min_value=1, max_value=6, step=1, key=f"unit_{sem}_{c}")

            point = grade_map[grade_input]
            st.write(f"{course_name} → Grade: {grade_input}, GP: {point}")

            semester_units += unit
            semester_points += point * unit
            courses_list.append({"name": course_name, "grade": grade_input, "unit": unit, "point": point})

        semester_data.append({
            "semester": sem,
            "total_units": semester_units,
            "total_points": semester_points,
            "courses": courses_list
        })

        total_new_units += semester_units
        total_new_points += semester_points

    if st.button("Calculate Updated CGPA"):
        total_units_all = completed_units + total_new_units
        total_points_all = (current_cgpa * completed_units) + total_new_points
        updated_cgpa = total_points_all / total_units_all if total_units_all > 0 else 0

        st.markdown("---")
        st.subheader(f"Updated CGPA: {updated_cgpa:.3f}")

        # Show semester GPAs
        for sem in semester_data:
            sem_gpa = sem['total_points'] / sem['total_units'] if sem['total_units'] > 0 else 0
            st.markdown(f"- Semester {sem['semester']} GPA: {sem_gpa:.3f}")

        # Report Download
        result_txt = StringIO()
        result_txt.write("GPA/CGPA Report\n" + "-"*30 + "\n")
        if completed_units > 0:
            result_txt.write(f"Previous CGPA: {current_cgpa} over {completed_units} units\n")
        for sem in semester_data:
            result_txt.write(f"\nSemester {sem['semester']}\n")
            for course in sem["courses"]:
                result_txt.write(f"{course['name']} | Grade: {course['grade']} | Unit: {course['unit']} | GP: {course['point']}\n")
            sem_gpa = sem['total_points'] / sem['total_units'] if sem['total_units'] > 0 else 0
            result_txt.write(f"Semester GPA: {sem_gpa:.3f}\n")

        result_txt.write(f"\nUpdated CGPA: {updated_cgpa:.3f}\n")
        result_txt.write("Generated by: GPA/CGPA App by Datapsalm & Victoria\n")

        st.download_button("Download Report (TXT)", result_txt.getvalue(), "updated_cgpa_report.txt", "text/plain")


# -------------------- WHAT DO I NEED FEATURE ---------------------
def WhatDoINeed():
    st.image("RR.jpg", use_container_width=True)

    st.header("What Do I Need To Reach My Target CGPA?")
    st.markdown("Plan your grades for the upcoming 2 semesters to reach your desired CGPA.")

    current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=5.0, step=0.001, format="%.3f")
    completed_credits = st.number_input("Total completed Units:", min_value=0, step=1)
    
    st.markdown("Semester 1 (Next Semester)")
    sem1_credits = st.number_input("Total Units for Semester 1:", min_value=1, step=1)
    
    st.markdown("Semester 2 (Following Semester)")
    sem2_credits = st.number_input("Total Units for Semester 2:", min_value=1, step=1)
    
    target_cgpa = st.number_input("Target CGPA:", min_value=0.0, max_value=5.0, step=0.001, format="%.3f")

    if st.button("Calculate Required GPA"):
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
        st.subheader("Suggested GPA Plans for Next 2 Semesters")

        st.markdown(f"Option 1 (Equal GPA Both Semesters): Semester 1: {equal_gpa:.3f}  |  Semester 2: {equal_gpa:.3f}")
        st.markdown(f"Option 2 (Semester 1 Lower, Semester 2 Higher): Semester 1: {sem1_lower:.3f}  |  Semester 2: {sem2_higher:.3f}")
        st.markdown(f"Option 3 (Semester 1 Higher, Semester 2 Lower): Semester 1: {sem1_higher:.3f}  |  Semester 2: {sem2_lower:.3f}")

        if equal_gpa > 5:
            st.error("This target is not achievable in the next 2 semesters (required GPA > 5.0).")
        elif equal_gpa >= 4.8:
            st.warning("Extremely challenging: You must score nearly all A's across both semesters.")
        elif equal_gpa >= 4.0:
            st.info("High performance needed: Mostly A's and some B's.")
        else:
            st.success("Achievable target with good performance.")

    st.markdown("<hr><p style='text-align: center;'>Built by Datapsalm & Victoria</p>", unsafe_allow_html=True)


# ------------------ ROUTING -----------------------
if menu == "Homepage":
    HomePage()
elif menu == "GPA Calculator":
    GPACalculator()
elif menu == "What Do I Need To Get?":
    WhatDoINeed()
