import streamlit as st
from fpdf import FPDF

# Set up page
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

# Menu options
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

# PDF generation function
def generate_pdf(results):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GPA/CGPA Calculation Result", ln=True, align="C")
    
    # Add the results to the PDF
    pdf.ln(10)  # Line break
    pdf.set_font("Arial", size=12)
    
    for line in results:
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    
    # Save the PDF to a file
    pdf_file_path = "/mnt/data/gpa_cgpa_result.pdf"
    pdf.output(pdf_file_path)
    
    return pdf_file_path

# Home page
if menu == "Home":
    HomePage()

# 4.0 GPA/CGPA Calculator
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

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.subheader(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")
        total_semesters += semesters
        
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
        sem = total_semesters
        results = [
            f"Total Sessions: {sessions}",
            f"Total Semesters: {sem}",
            f"Total Units: {total_units_all}",
            f"Final CGPA: {round(cgpa, 2)}"
        ]
        
        # Generate PDF
        pdf_file_path = generate_pdf(results)
        
        # Provide download link
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {sem}")
        st.markdown(f"**Total Units:** {total_units_all}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
        st.markdown(f"[Download your GPA/CGPA result as a PDF here]({pdf_file_path})")
    else:
        st.error("❌ No valid GPA data to compute CGPA.")

    st.markdown("""
    <hr>
    <p style='text-align: center;'>Built with ❤️ by Datapsalm & Victoria | GPA/CGPA App</p>
    """, unsafe_allow_html=True)

# 5.0 GPA/CGPA Calculator
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

    sessions = st.number_input("How many sessions?", min_value=1, step=1)

    for s in range(1, sessions + 1):
        st.subheader(f"📘 Session {s}")
        semesters = st.number_input(f"How many semesters in session {s}?", min_value=1, step=1, key=f"sem_{s}")
        total_semesters += semesters
        
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
        sem = total_semesters
        results = [
            f"Total Sessions: {sessions}",
            f"Total Semesters: {sem}",
            f"Total Units: {total_units_all}",
            f"Final CGPA: {round(cgpa, 2)}"
        ]
        
        # Generate PDF
        pdf_file_path = generate_pdf(results)
        
        # Provide download link
        st.markdown("---")
        st.subheader("📌 Final Summary")
        st.markdown(f"**Total Sessions:** {sessions}")
        st.markdown(f"**Total Semesters:** {sem}")
        st.markdown(f"**Total Units:** {total_units_all}")
        st.markdown(f"**Final CGPA:** `{round(cgpa, 2)}`")
        st.markdown(f"[Download your GPA/CGPA result as a PDF here]({pdf_file_path})")
    else
