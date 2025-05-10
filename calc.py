import streamlit as st
from io import StringIO

st.set_page_config(page_title="🎓 GPA/CGPA Calculator", layout="centered")

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
            num_courses = st.number_input(f"Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            total_courses += num_courses
            
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
            session_data.append({
                "session": s, 
                "semester": sem, 
                "total_units": total_units, 
                "total_weighted_points": total_weighted_points,
                "courses": [{"name": course_name, "grade": grade_input, "unit": unit, "point": point} for c in range(1, num_courses + 1)]
            })

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

    # 📄 Feature: Download Readable Result
    if session_data:
        result_txt = StringIO()
        result_txt.write("📘 GPA & CGPA Report\n")
        result_txt.write("-" * 30 + "\n")
    
        for semester in session_data:
            s = semester["session"]
            sem = semester["semester"]
            result_txt.write(f"\nSession {s} - Semester {sem}\n")
            result_txt.write("-" * 30 + "\n")
            for course in semester["courses"]:
                result_txt.write(f"{course['name']} | Grade: {course['grade']} | Unit: {course['unit']} | GP: {course['point']}\n")
            gpa = semester["total_weighted_points"] / semester["total_units"] if semester["total_units"] else 0
            result_txt.write(f"Semester GPA: {round(gpa, 2)}\n")
            total_courses += len(semester["courses"])

        # Calculate the final CGPA
        cgpa = total_weighted_points_all / total_units_all if total_units_all > 0 else 0

        # Add the summary to the report
        result_txt.write("\n🎯 Final Summary\n")
        result_txt.write("-" * 30 + "\n")
        result_txt.write(f"**Total Sessions:** {sessions}\n")
        result_txt.write(f"**Total Semesters:** {total_semesters}\n")
        result_txt.write(f"**Total Courses:** {total_courses}\n")
        result_txt.write(f"**Total Units:** {total_units_all}\n")
        result_txt.write(f"**Final CGPA:** `{round(cgpa, 2)}`\n")
        result_txt.write("-" * 30 + "\n")
        result_txt.write("Generated by: GPA/CGPA App by Datapsalm & Victoria\n")
        
        # Provide the option to download the text file
        st.download_button(
            "📄 Download Readable Report (TXT)",
            result_txt.getvalue(),
            file_name="gpa_report.txt",
            mime="text/plain"
        )

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
            num_courses = st.number_input(f"Number of courses:", min_value=1, step=1, key=f"course_{s}_{sem}")
            total_courses += num_courses
            
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
            session_data.append({
                "session": s, 
                "semester": sem, 
                "total_units": total_units, 
                "total_weighted_points": total_weighted_points,
                "courses": [{"name": course_name, "grade": grade_input, "unit": unit, "point": point} for c in range(1, num_courses + 1)]
            })

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

    # 📄 Feature: Download Readable Result
    if session_data:
        result_txt = StringIO()
        result_txt.write("📘 GPA & CGPA Report\n")
        result_txt.write("-" * 30 + "\n")
    
        for semester in session_data:
            s = semester["session"]
            sem = semester["semester"]
            result_txt.write(f"\nSession {s} - Semester {sem}\n")
            result_txt.write("-" * 30 + "\n")
            result_txt.write(f"Total Units: {semester['total_units']}\n")
            result_txt.write(f"Total Weighted Points: {semester['total_weighted_points']}\n")
            gpa = semester["total_weighted_points"] / semester["total_units"] if semester["total_units"] else 0
            result_txt.write(f"Semester GPA: {round(gpa, 2)}\n")
    
                result_txt.write("\n🎯 Final CGPA: {:.2f}\n".format(cgpa if total_units_all > 0 else 0))
        result_txt.write("-" * 30 + "\n")
        result_txt.write("GPA/CGPA App by Datapsalm & Victoria\n")
    
        st.download_button("📄 Download Readable Report (TXT)", result_txt.getvalue(), file_name="gpa_report.txt", mime="text/plain")

    st.markdown("""  
    <hr>  
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>  
    """, unsafe_allow_html=True)
 
