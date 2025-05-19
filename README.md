
# 🎓 Student Registration Portal

A dynamic and user-friendly **Streamlit web application** for student registration and placement tracking. This portal supports **multi-tabbed registration**, validates input in real-time, and stores data into a **MySQL relational database** using Python.

---

## 📌 Features

- 🔐 **Login Authentication** (Admin login)
- 📋 **Multi-Tab Registration Interface**
  - **Personal Details**
  - **Programming Track Record**
  - **Soft Skills Evaluation**
  - **Placement Details**
- 🧠 **Session State Management** for multi-tab data retention
- ✅ **Data Summary & Final Confirmation Step**
- 💾 **Secure Database Insertion** into MySQL using `mysql.connector`
- 🎉 **Feedback Messages** with `st.success()`, `st.error()`, and `st.balloons()`

---

## 🛠️ Tech Stack

| Category         | Technology                        |
|------------------|------------------------------------|
| Frontend         | [Streamlit](https://streamlit.io)  |
| Backend (DB)     | [MySQL](https://www.mysql.com)     |
| ORM/Connector    | `mysql.connector` (Python client)  |
| Programming Lang | Python 3.x                         |

---

## 🗃️ Database Schema

The portal uses the following MySQL tables:

1. **`students_record`**  
   Stores basic personal information.

2. **`programming_record`**  
   Tracks programming skills and achievements.

3. **`soft_skills_record`**  
   Evaluates soft skill attributes.

4. **`placements_record`**  
   Records placement data including company, salary, etc.

👉 *SQL schema definitions can be generated on request.*

---

## 🚀 How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/student-registration-portal.git
   cd student-registration-portal
   ```

2. **Install dependencies**  
   ```bash
   pip install streamlit mysql-connector-python
   ```

3. **Update Database Credentials**  
   Edit the database connection section in the code:
   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       database="your_database"
   )
   ```

4. **Run the Streamlit app**  
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Sample Admin Credentials (Hardcoded)

| Username | Password  |
|----------|-----------|
| admin    | admin@123 |

🔒 *You can enhance this with database-backed login or hashed passwords for production.*

---

## ✅ Data Validation

All inputs are validated in each tab before allowing users to proceed:

- Required fields must be filled
- Numerical fields are range-checked
- Email and phone formats are validated
- Dates are optional but correctly handled

---

## 📦 Project Structure

```plaintext
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation (this file)
```

---

## 📈 Future Improvements

- 🌐 Role-based access (Admin, Student)
- 🧾 Downloadable registration reports (PDF/CSV)
- 🔍 Searchable student database dashboard
- 📤 Email notifications on registration
- 🔐 Login with hashed credentials using `bcrypt`

---

## 🧑‍💻 Author

**Manigandan V**  
M.Tech - Modeling and Simulation  
M.S - Mathematical Physics
B.E - Automobile Engineering



