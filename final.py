import streamlit as st
import pymysql
import re
from datetime import datetime
import pandas as pd


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Brokenleg@1",
    database="db1",
    autocommit=True
)


cursor = conn.cursor(pymysql.cursors.DictCursor)


# Initialize all session state variables at the top
if "menu" not in st.session_state:
    st.session_state.menu = "Login"
if "tab_index" not in st.session_state:
    st.session_state.tab_index = 0
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False


st.set_page_config(page_title="Student Portal", layout="centered")
st.title("🎓 Student Portal")

# Reflect session state in the sidebar menu
menu_options = ["Login", "Register"]
menu_index = menu_options.index(st.session_state.menu)
menu = st.sidebar.radio("Menu", menu_options, index=menu_index)

# Update session state with the selected menu
st.session_state.menu = menu



# --------------- LOGIN PAGE --------------- #



if st.session_state.menu == "Login":
    st.subheader("🔐 Login Page")
    email = st.text_input("Enter your Email")

    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])  # Equal widths; adjust as needed

    with col1:
        if st.button("Login"):
            cursor.execute("SELECT * FROM students_record WHERE email = %s", (email,))
            student = cursor.fetchone()
            
            if student:
                st.success(f"Welcome, {student['name']}!")
                
                # Fetch data from all four tables using the student_id
                student_id = student['student_id']
                
                # 1. Fetch programming data
                cursor.execute("SELECT * FROM programming_record WHERE student_id = %s", (student_id,))
                programming_data = cursor.fetchone()
                
                # 2. Fetch soft skills data
                cursor.execute("SELECT * FROM soft_skills_record WHERE student_id = %s", (student_id,))
                soft_skills_data = cursor.fetchone()
                
                # 3. Fetch placement data
                cursor.execute("SELECT * FROM placements_record WHERE student_id = %s", (student_id,))
                placement_data = cursor.fetchone()
                
                # Display all the fetched data
                st.write("### 🧾 Your Registered Details")
                
                # Personal details
                st.write("#### 👤 Personal")
                for key, value in student.items():
                    if key != 'student_id':  # Skip displaying the ID
                        st.write(f"{key.replace('_', ' ').title()}: {value}")
                
                # Programming details
                st.write("#### 💻 Programming")
                if programming_data:
                    for key, value in programming_data.items():
                        if key != 'student_id':  # Skip displaying the ID
                            st.write(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    st.info("No programming details found")
                
                # Soft skills details
                st.write("#### 🎤 Soft Skills")
                if soft_skills_data:
                    for key, value in soft_skills_data.items():
                        if key != 'student_id':  # Skip displaying the ID
                            st.write(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    st.info("No soft skills details found")
                
                # Placement details
                st.write("#### 🎓 Placement")
                if placement_data:
                    for key, value in placement_data.items():
                        if key != 'student_id':  # Skip displaying the ID
                            st.write(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    st.info("No placement details found")
            else:
                st.warning("Email not found. It seems you're not registered.")
                    
    with col4:
        if st.button("Register"):
            st.session_state.menu = "Register"
            st.rerun()  # Add rerun to refresh the page with new menu

elif st.session_state.menu == "Register":
    st.subheader("📝 New Student Registration")

    tabs = st.tabs(["📝 New Student Registration","📋 Summary"])

    active_tab = st.session_state.tab_index
    if "personal_data" not in st.session_state:
        st.session_state.personal_data = {}
    if "programming_data" not in st.session_state:
        st.session_state.programming_data = {}
    if "soft_skills_data" not in st.session_state:
        st.session_state.soft_skills_data = {}
    if "placement_data" not in st.session_state:
        st.session_state.placement_data = {}


    try:
        cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'db1' AND TABLE_NAME = 'students_record'")
        next_id = cursor.fetchone()[0]
        
        # If for some reason the query doesn't work, provide a fallback
        if not next_id:
            # Alternative approach: get max ID and add 1
            cursor.execute("SELECT COALESCE(MAX(student_id), 0) + 1 FROM students_record")
            next_id = cursor.fetchone()[0]
    except Exception as e:
        st.error(f"Error fetching next ID: {e}")
        next_id = "Unable to fetch ID"


    with tabs[active_tab]:
        if active_tab == 0:

            with st.form("registration_form"):
                with st.expander("Personal Details", expanded=True):
                    st.text_input("Student ID", value=next_id, disabled=True, key="student_id_display")
                    name = st.text_input('Full Name')

                    if name and not re.match(r'^[a-zA-Z ]+$', name):
                            st.warning("Name should contain only alphabets and spaces.")

                    # Get date of birth input
                    min_date = datetime(1975, 1, 1)

                    # Get date of birth input, restricting the date range to be from 1975 onwards
                    dob = st.date_input("Date of Birth", min_value=min_date.date(), max_value=datetime.today().date())

                    # Calculate and display age
                    if dob:
                        today = datetime.today().date()
                        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                    
                    gender = st.selectbox("Gender", ("Male", "Female", "Other"), index=2)
                    email = st.text_input("Email")

                    # List of allowed domains
                    allowed_domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "protonmail.com"]

                    if email:
                        # General email regex check
                        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                            # Extract the domain
                            domain = email.split('@')[-1]
                            if domain in allowed_domains:
                                st.success(f"✅ Valid email: {email}")
                            else:
                                st.warning(f"❌ Please enter an email from one of the following: {', '.join(allowed_domains)}")
                        else:
                            st.warning("❌ Please enter a valid email address.")

                    phone_number = st.text_input("Phone Number")

                
                    today = datetime.today()

                    # Create a list of years from 2010 to the current year
                    years = list(range(2010, today.year + 1))

                    # Selectbox for enrollment year
                    enrollment_year = st.selectbox("Enrollment Year", years[::-1])

                    course_batch = st.text_input("Course Batch / Cohort Name")
                    
                    city = st.text_input('City')

                    years = list(range(2010, today.year + 3))  # Adding two years beyond the current year

                    # Display the selectbox for graduation year
                    graduation_year = st.selectbox("Graduation Year", years, index=len(years)-1)   
                
                with st.expander("Programming Details"):
                    
                    programming_id = f'p-{next_id}'
                    st.text_input("Programming ID", value=programming_id, disabled=True, key="programming_id_display")
                    language = st.multiselect('Programming Languages',("Python", "R", "SQL", "Java", "Scala", "Julia", 
                                                                        "C++", "JavaScript", "MATLAB", "Bash", "Go", 
                                                                        "Rust", "Other"))
                    problems_solved = st.number_input("Problems_solved", min_value=0, max_value=1000, step=1, format="%d")

                    assessments_completed = st.number_input("Assessments Completed", min_value=0, max_value=50, step=1, format="%d")
                    mini_projects = st.number_input("Mini Projects", min_value=0, max_value=15, step=1, format="%d")
                    certifications_earned = st.number_input("Certifications Earned", min_value=0, max_value=50, step=1, format="%d")
                    latest_project_score = st.number_input("Latest Project Score", min_value=0, max_value=100, step=1, format="%d")

                
                with st.expander("Soft Skills Details"):
                    
                    soft_skill_id = f's-{next_id}'
                    st.text_input("Soft Skill ID", value=soft_skill_id, disabled=True, key="Soft_skill_id_display")
                    communication = st.number_input("Communication Score", min_value=0, max_value=100, step=1, format="%d")
                    teamwork = st.number_input("Teamwork Score", min_value=0, max_value=100, step=1, format="%d")
                    presentation = st.number_input("Presentation Score", min_value=0, max_value=100, step=1, format="%d")
                    leadership = st.number_input("Leadership Score", min_value=0, max_value=100, step=1, format="%d")
                    critical_thinking = st.number_input("Critical Thinking Score", min_value=0, max_value=100, step=1, format="%d")
                    interpersonal_skills = st.number_input("Interpersonal Skills Score", min_value=0, max_value=100, step=1, format="%d")
                
                with st.expander("Plavcement Details"):
                    
                    placement_id = f'pp-{next_id}'
                    st.text_input("Placement ID", value=placement_id, disabled=True, key="placement_id_display")
                    mock_interview_score = st.number_input("Mock Interview Score", min_value=0, max_value=100, step=1, format="%d")
                    internships_completed = st.number_input("Number of Internships Completed", min_value=0, max_value=30, step=1, format="%d")
                    
                    # Create the placement status selectbox
                    placement_status = st.selectbox(
                        "Placement Status",
                        options=["Ready", "Not Ready", "Placed"],
                        key="placement_status"
                    )
                    
                    # Only show these fields if "Placed" is selected
                    company_name = st.text_input("Company Name", placeholder="Type NA if not applicable")
                    placement_package = st.text_input("Placement Package", placeholder="Type NA if not applicable")
                    num_rounds = st.number_input("Number of Rounds Cleared", min_value=1, value=None, placeholder="NA")
                    date_na = st.checkbox("Placement Date Not Applicable")
                    if not date_na:
                        placed_date = st.date_input("Placement Date", today.date())
                    else:
                        placed_date = None


                submitted = st.form_submit_button("Preview")

                if submitted:
                    if (not name or not age or not email or not phone_number or not enrollment_year or not course_batch or not city or not graduation_year
                         or not  programming_id or not language or not soft_skill_id or not placement_id ):
                        st.error("All fields are required. Please fill in all fields.")
                    
                    elif not phone_number.isdigit() or len(phone_number) != 10:
                        st.error("Please enter a valid 10-digit phone number.")
                    elif not re.match(r'^[a-zA-Z ]+$', name):
                        st.error("Name should contain only alphabets and spaces.")
                    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                        st.error("Please enter a valid email address.")
                    else:
                        st.success("Form submitted successfully!")
                        st.session_state.personal_data = {
                            "student_id": next_id,
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "email": email,
                            "phone_number": phone_number,
                            "enrollment_year": enrollment_year,
                            "course_batch": course_batch,
                            "city": city,
                            "graduation_year": graduation_year
                        }

                        st.session_state.programming_data = {
                            "student_id": next_id,
                            "programming_id": programming_id,
                            "language": language,
                            "problems_solved": problems_solved,
                            "assessments_completed": assessments_completed,
                            "mini_projects": mini_projects,
                            "certifications_earned": certifications_earned,
                            "latest_project_score": latest_project_score
                        }

                        st.session_state.soft_skills_data = {
                            "soft_skill_id": soft_skill_id,
                            "student_id": next_id,
                            "communication": communication,
                            "teamwork": teamwork,
                            "presentation": presentation,
                            "leadership": leadership,
                            "critical_thinking": critical_thinking,
                            "interpersonal_skills": interpersonal_skills,
                            
                        }

                        st.session_state.placement_data = {
                            "placement_id": placement_id,
                            "student_id": next_id,
                            "mock_interview_score": mock_interview_score,
                            "internships_completed": internships_completed,
                            "placement_status": placement_status,
                            "company_name": company_name,
                            "placement_package": placement_package,
                            "num_rounds": num_rounds,
                            'placed_date' : placed_date,
                            
                        }
                        st.success("✅ Registration details saved successfully!")
                        st.session_state.tab_index = 1
                        st.rerun()

        elif active_tab == 1:    
            st.subheader("📋 Registration Summary")
                
            # Display Personal Data
            st.write("### 👤 Personal Details")
            if st.session_state.personal_data:
                for key, value in st.session_state.personal_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.warning("Personal details not completed")
            
            # Display Programming Data
            st.write("### 💻 Programming Details")
            if st.session_state.programming_data:
                for key, value in st.session_state.programming_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.warning("Programming details not completed")
            
            # Display Soft Skills Data
            st.write("### 🎤 Soft Skills Details")
            if st.session_state.soft_skills_data:
                for key, value in st.session_state.soft_skills_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.warning("Soft skills details not completed")
            
            # Display Placement Data
            st.write("### 🎓 Placement Details")
            if st.session_state.placement_data:
                for key, value in st.session_state.placement_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.warning("Placement details not completed")
            col1, col2 = st.columns(2)
            with col1:
                prev_button = st.button("Previous")
            with col2:
                next_button = st.button("Submit All Data")
                
            if next_button:
            
                try:
                    # Insert into MySQL tables
                    # Personal data
                    if st.session_state.personal_data:
                        personal_data = st.session_state.personal_data
                        query = """
                            INSERT INTO students_record
                            
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (
                            personal_data["student_id"], personal_data["name"], personal_data["age"], 
                            personal_data["gender"], personal_data["email"], personal_data["phone_number"],
                            personal_data["enrollment_year"], personal_data["course_batch"], 
                            personal_data["city"], personal_data["graduation_year"]
                        ))
                    
                    # Programming data
                    if st.session_state.programming_data:
                        programming_data = st.session_state.programming_data
                        insert_query = """
                                            INSERT INTO programming_record
                                            
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                        """
                        cursor.execute(insert_query, (
                                                programming_data["programming_id"],
                                                programming_data["student_id"],
                                                programming_data["language"],
                                                programming_data["problems_solved"],
                                                programming_data["assessments_completed"],
                                                programming_data["mini_projects"],
                                                programming_data["certifications_earned"],
                                                programming_data["latest_project_score"]
                                            ))
                                                            
                    # Soft skills data
                    if st.session_state.soft_skills_data:
                        soft_skills_data = st.session_state.soft_skills_data
                        insert_query = """
                                            INSERT INTO soft_skills_record
                                            
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                        """
                        cursor.execute(insert_query, (
                                                        soft_skills_data["soft_skill_id"],
                                                        soft_skills_data["student_id"],
                                                        soft_skills_data["communication"],
                                                        soft_skills_data["teamwork"],
                                                        soft_skills_data["presentation"],
                                                        soft_skills_data["leadership"],
                                                        soft_skills_data["critical_thinking"],
                                                        soft_skills_data["interpersonal_skills"]
                                                    ))
                        
                    # Placement data
                    if st.session_state.placement_data:
                        placement_data = st.session_state.placement_data
                        insert_query = """
                                            INSERT INTO placements_record
                                            
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """
                        cursor.execute(insert_query, (
                                                    placement_data["placement_id"],
                                                    placement_data["student_id"],
                                                    placement_data["mock_interview_score"],
                                                    placement_data["internships_completed"],
                                                    placement_data["placement_status"],
                                                    placement_data["company_name"],
                                                    placement_data["placement_package"],
                                                    placement_data["num_rounds"],
                                                    placement_data["placed_date"]
                                                ))
                        conn.commit()   
                        st.success("🎉 All data successfully submitted to database!")
                        
                        # Reset session state for new registration
                        st.session_state.personal_data = {}
                        st.session_state.programming_data = {}
                        st.session_state.soft_skills_data = {}
                        st.session_state.placement_data = {}
                        st.session_state.tab_index = 0
                    
                    
                except Exception as e:
                    st.error(f"Error submitting data: {e}")

            if prev_button:
                    # Go back to the previous tab
                    st.session_state.tab_index = 0
                    st.rerun()

                    

# Close database connection when app is done
conn.close()      


                    