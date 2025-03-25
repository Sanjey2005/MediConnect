from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sanjey",
        database="hospital_db"
    )
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if role == "Patient":
        cursor.execute("SELECT * FROM Patients WHERE Name = %s AND PatientID = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['PatientID']
            session['username'] = user['Name']
            session['role'] = 'Patient'
            flash(f'Welcome back, {user["Name"]}!', 'success')
            return redirect(url_for('patient_dashboard'))

    elif role == "Doctor":
        cursor.execute("SELECT * FROM Doctors WHERE Name = %s AND DoctorID = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['DoctorID']
            session['username'] = user['Name']
            session['role'] = 'Doctor'
            flash(f'Welcome back, Dr. {user["Name"]}!', 'success')
            return redirect(url_for('doctor_dashboard'))

    elif role == "Staff":
        cursor.execute("SELECT * FROM Staff WHERE Name = %s AND StaffID = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['StaffID']
            session['username'] = user['Name']
            session['role'] = 'Staff'
            session['staff_role'] = user['Role']
            flash(f'Welcome back, {user["Name"]}!', 'success')
            return redirect(url_for('staff_dashboard'))

    cursor.close()
    conn.close()
    flash('Invalid credentials. Please try again.', 'error')
    return redirect(url_for('index'))

@app.route('/patient/dashboard')
def patient_dashboard():
    # Check if user is logged in and is a patient
    if 'user_id' not in session or session.get('role') != 'Patient':
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch patient information
        cursor.execute("""
            SELECT PatientID, Name, DOB, Gender, ContactInfo, Address
            FROM Patients
            WHERE PatientID = %s
        """, (session['user_id'],))
        patient = cursor.fetchone()

        # Fetch upcoming appointments
        cursor.execute("""
            SELECT a.AppointmentDate, d.Name as DoctorName, 
                   d.Specialization, a.Status
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            WHERE a.PatientID = %s
            AND a.AppointmentDate >= CURDATE()
            ORDER BY a.AppointmentDate
        """, (session['user_id'],))
        appointments = cursor.fetchall()

        # Fetch current prescriptions
        cursor.execute("""
            SELECT m.Name as MedicationName, p.Dosage, 
                   d.Name as DoctorName, p.StartDate, p.EndDate
            FROM Prescriptions p
            JOIN Medications m ON p.MedicationID = m.MedicationID
            JOIN Doctors d ON p.DoctorID = d.DoctorID
            WHERE p.PatientID = %s
            AND p.EndDate >= CURDATE()
        """, (session['user_id'],))
        prescriptions = cursor.fetchall()

        # Fetch recent lab results
        cursor.execute("""
            SELECT TestName, TestResults
            FROM LabTests
            WHERE PatientID = %s
            ORDER BY TestDate DESC
            LIMIT 5
        """, (session['user_id'],))
        lab_tests = cursor.fetchall()

        # Fetch recent bills
        cursor.execute("""
            SELECT Date, TotalAmount, InsuranceCovered, 
                   Status
            FROM Bills
            WHERE PatientID = %s
            ORDER BY Date DESC
            LIMIT 5
        """, (session['user_id'],))
        bills = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('patient_dashboard.html',
                             patient=patient,
                             appointments=appointments,
                             prescriptions=prescriptions,
                             lab_tests=lab_tests,
                             bills=bills)

    except mysql.connector.Error as err:
        # Log the error appropriately
        print(f"Database error: {err}")
        return "An error occurred while fetching your information. Please try again later.", 500

    except Exception as e:
        # Log the error appropriately
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later.", 500

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'role' in session and session['role'] == 'Doctor':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        doctor_id = session['user_id']

        # Fetch doctor's details including department info
        cursor.execute("""
            SELECT d.DoctorID, d.Name, d.Specialization, d.ContactInfo, d.Experience,
                   dept.Name as DepartmentName, dept.Location as DepartmentLocation
            FROM Doctors d
            LEFT JOIN Departments dept ON d.DepartmentID = dept.DepartmentID
            WHERE d.DoctorID = %s
        """, (doctor_id,))
        doctor = cursor.fetchone()

        # Get today's date for filtering appointments
        today = datetime.now().date()

        # Fetch today's appointments with modified lab test info
        cursor.execute("""
            SELECT 
                a.AppointmentID,
                a.AppointmentDate,
                a.Status as AppointmentStatus,
                a.Reason,
                p.PatientID,
                p.Name as PatientName,
                p.ContactInfo as PatientContact,
                COALESCE(lt.TestResults, 'No test results') as LatestTestResults,
                COALESCE(lt.TestName, 'No tests') as TestName
            FROM Appointments a
            JOIN Patients p ON a.PatientID = p.PatientID
            LEFT JOIN (
                SELECT PatientID, TestResults, TestName,
                    ROW_NUMBER() OVER (PARTITION BY PatientID ORDER BY TestID DESC) as rn
                FROM LabTests
            ) lt ON p.PatientID = lt.PatientID AND lt.rn = 1
            WHERE a.DoctorID = %s
                AND DATE(a.AppointmentDate) = %s
            ORDER BY a.AppointmentDate ASC
        """, (doctor_id, today))
        appointments = cursor.fetchall()

        # Fetch appointment statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_appointments,
                SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN Status = 'Pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled
            FROM Appointments
            WHERE DoctorID = %s
                AND DATE(AppointmentDate) = %s
        """, (doctor_id, today))
        stats = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template('doctor_dashboard.html', 
                             doctor=doctor,
                             appointments=appointments,
                             stats=stats)

    return redirect(url_for('index'))

@app.route('/update_appointment_status', methods=['POST'])
def update_appointment_status():
    if 'role' in session and session['role'] == 'Doctor':
        appointment_id = request.form.get('appointment_id')
        new_status = request.form.get('status')
        doctor_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # First verify if the appointment exists and belongs to this doctor
            cursor.execute("""
                SELECT AppointmentID, Status 
                FROM Appointments 
                WHERE AppointmentID = %s AND DoctorID = %s
            """, (appointment_id, doctor_id))
            
            appointment = cursor.fetchone()
            if appointment:
                # Simple status update
                cursor.execute("""
                    UPDATE Appointments 
                    SET Status = %s
                    WHERE AppointmentID = %s 
                    AND DoctorID = %s
                """, (new_status, appointment_id, doctor_id))
                
                conn.commit()
                
                # Fetch updated appointment data
                cursor.execute("""
                    SELECT 
                        a.AppointmentID,
                        a.AppointmentDate,
                        a.Status as AppointmentStatus,
                        a.Reason,
                        p.PatientID,
                        p.Name as PatientName,
                        p.ContactInfo as PatientContact
                    FROM Appointments a
                    JOIN Patients p ON a.PatientID = p.PatientID
                    WHERE a.AppointmentID = %s
                """, (appointment_id,))
                
                updated_appointment = cursor.fetchone()
                
                return jsonify({
                    'success': True,
                    'message': 'Appointment status updated successfully',
                    'appointment': updated_appointment
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Appointment not found or unauthorized'
                }), 404
                
        except Exception as e:
            conn.rollback()
            print(f"Error in update_appointment_status: {str(e)}")  # For debugging
            return jsonify({
                'success': False,
                'message': f'Error updating appointment status: {str(e)}'
            }), 500
        finally:
            cursor.close()
            conn.close()

    return jsonify({
        'success': False,
        'message': 'Unauthorized access'
    }), 401


@app.route('/staff_dashboard')
def staff_dashboard():
    if 'role' in session and session['role'] == 'Staff':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        staff_role = session['staff_role']
        
        if staff_role == 'Receptionist':
            # Fetch all patients for receptionist
            cursor.execute("SELECT * FROM Patients ORDER BY PatientID")
            patients = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('staff_dashboard_receptionist.html', patients=patients)
            
        elif staff_role == 'Lab Technician':
            # Fetch recent lab tests
            cursor.execute("""
                SELECT lt.*, p.Name as PatientName 
                FROM LabTests lt
                JOIN Patients p ON lt.PatientID = p.PatientID
                ORDER BY lt.TestDate DESC, lt.TestID DESC
            """)
            recent_tests = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('staff_dashboard_lab.html', recent_tests=recent_tests)
        
        # If staff role doesn't match any expected values
        flash('Invalid staff role', 'error')
        return redirect(url_for('logout'))
    
    # If not logged in or not staff
    flash('Please log in with valid staff credentials', 'error')
    return redirect(url_for('index'))

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if 'role' in session and session['role'] == 'Staff' and session['staff_role'] == 'Receptionist':
        try:
            name = request.form['name']
            dob = request.form['dob']
            gender = request.form['gender']
            contact = request.form['contact']
            address = request.form['address']
            insurance = request.form['insurance']
            emergency = request.form['emergency']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            args = (name, dob, gender, contact, address, insurance, emergency, 0)
            result_args = cursor.callproc('sp_register_patient', args)
            patient_id = result_args[-1]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Patient added successfully with ID: ' + str(patient_id))
            return redirect(url_for('staff_dashboard'))
            
        except mysql.connector.Error as e:
            flash(f'Error adding patient: {str(e)}', 'error')
            return redirect(url_for('staff_dashboard'))
    
    return redirect(url_for('index'))

@app.route('/remove_patient/<int:patient_id>', methods=['POST'])
def remove_patient(patient_id):
    if 'role' in session and session['role'] == 'Staff' and session['staff_role'] == 'Receptionist':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First delete related records from dependent tables
        cursor.execute("DELETE FROM Appointments WHERE PatientID = %s", (patient_id,))
        cursor.execute("DELETE FROM Prescriptions WHERE PatientID = %s", (patient_id,))
        cursor.execute("DELETE FROM Bills WHERE PatientID = %s", (patient_id,))
        cursor.execute("DELETE FROM LabTests WHERE PatientID = %s", (patient_id,))
        
        # Then delete the patient
        cursor.execute("DELETE FROM Patients WHERE PatientID = %s", (patient_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Patient removed successfully')
        return redirect(url_for('staff_dashboard'))
    
    return redirect(url_for('index'))

@app.route('/add_lab_test', methods=['POST'])
def add_lab_test():
    if 'role' in session and session['role'] == 'Staff' and session['staff_role'] == 'Lab Technician':
        try:
            patient_id = request.form['patient_id']
            test_name = request.form['test_name']
            test_results = request.form['test_results']
            test_cost = request.form['test_cost']
            
            # Validate inputs
            if not patient_id or not test_name or not test_results or not test_cost:
                flash('All fields are required', 'warning')
                return redirect(url_for('staff_dashboard'))
            
            try:
                test_cost = float(test_cost)
                if test_cost <= 0:
                    flash('Test cost must be greater than 0', 'warning')
                    return redirect(url_for('staff_dashboard'))
            except ValueError:
                flash('Invalid test cost value', 'warning')
                return redirect(url_for('staff_dashboard'))
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # First verify if patient exists
            cursor.execute("SELECT Name FROM Patients WHERE PatientID = %s", (patient_id,))
            patient = cursor.fetchone()
            
            if not patient:
                flash(f'Patient ID {patient_id} not found in the system', 'danger')
                return redirect(url_for('staff_dashboard'))
            
            # Insert lab test
            cursor.execute("""
                INSERT INTO LabTests (PatientID, TestName, TestResults, TestCost, TestDate, Status)
                VALUES (%s, %s, %s, %s, CURDATE(), 'Completed')
            """, (patient_id, test_name, test_results, test_cost))
            
            conn.commit()
            flash(f'Lab test results for patient {patient["Name"]} (ID: {patient_id}) added successfully', 'success')
            
        except mysql.connector.Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error adding lab test: {str(e)}', 'danger')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
            
        return redirect(url_for('staff_dashboard'))
    
    flash('Unauthorized access', 'danger')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    username = session.get('username', '')
    session.clear()
    flash(f'You have been successfully logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)