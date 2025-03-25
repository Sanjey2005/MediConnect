# Hospital Management System (HMS)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)

A web-based Hospital Management System built with Flask, MySQL, and Bootstrap, designed to streamline hospital operations including patient management, appointments, prescriptions, lab tests, and billing.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Hospital Management System (HMS) is a comprehensive solution for managing hospital operations. It provides role-based dashboards for patients, doctors, and staff (receptionists and lab technicians), enabling efficient tracking of appointments, patient records, prescriptions, lab results, and bills. The system includes a responsive UI and secure login functionality.

## Features
- **Role-Based Access:**
  - **Patients:** View personal information, upcoming appointments, prescriptions, lab results, and bills.
  - **Doctors:** Manage daily appointments, update statuses, and view patient details.
  - **Staff:**
    - **Receptionists:** Register and remove patients.
    - **Lab Technicians:** Add and view lab test results.
- **Secure Login:** Authentication based on username, password, and role.
- **Database Integration:** MySQL backend for persistent data storage.
- **Responsive Design:** User-friendly interface built with Bootstrap and custom CSS.
- **Real-Time Updates:** AJAX-based appointment status updates for doctors.
- **Flash Messages:** User feedback for successful actions or errors.

## Technologies Used
- **Backend:** Python 3.8+, Flask
- **Frontend:** HTML, CSS, Bootstrap 5, Font Awesome
- **Database:** MySQL
- **Dependencies:** `mysql-connector-python`, `flask`

## Installation
Follow these steps to set up the project locally:

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Sanjey2005/MediConnect.git
   cd hospital-management-system
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install flask mysql-connector-python
   ```

4. **Set Up MySQL Database:**
   See [Database Setup](#database-setup) below.

5. **Run the Application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

## Database Setup
1. **Create the Database:**
   Log in to MySQL and run:
   ```sql
   CREATE DATABASE hospital_db;
   ```

2. **Initialize Tables:**
   Copy and execute the SQL code from `database.sql` (provided in the repository) in your MySQL client (e.g., MySQL Workbench or CLI).

3. **Configure Database Connection:**
   Update the `get_db_connection()` function in `app.py` with your MySQL credentials:
   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       database="hospital_db"
   )
   ```

4. **Sample Data:**
   The `database.sql` file includes sample data for departments, doctors, patients, staff, and more to get you started.

## Usage
- **Login:**
  - Access the system at `http://localhost:5000`.
  - Use credentials from the sample data in `database.sql`:
    - **Patient:** Name as username, PatientID as password (e.g., "Aarav Sharma" / "1")
    - **Doctor:** Name as username, DoctorID as password (e.g., "Dr. Rajesh Sharma" / "1")
    - **Staff:** Name as username, StaffID as password (e.g., "Anjali Verma" / "1")
  - Select the appropriate role from the dropdown.

- **Dashboards:**
  - **Patient Dashboard:** View personal info, appointments, prescriptions, lab results, and bills.
  - **Doctor Dashboard:** Manage today’s appointments and update statuses.
  - **Staff Dashboard:**
    - Receptionists can add/remove patients.
    - Lab Technicians can add lab test results.

- **Logout:** Available on all dashboards to end the session securely.

## Directory Structure
```
hospital-management-system/
├── static/
│   ├── images/
│   │   └── medical-favicon.svg
│   └── styles.css (optional)
├── templates/
│   ├── login.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── staff_dashboard_receptionist.html
│   ├── staff_dashboard_lab.html
│   └── patient_registration.html
├── app.py
├── database.sql
└── README.md
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

