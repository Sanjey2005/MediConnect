USE hospital_db;

-- 1. Patients Table
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    DOB DATE NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    ContactInfo VARCHAR(100),
    Address VARCHAR(255),
    InsuranceDetails VARCHAR(255),
    EmergencyContact VARCHAR(100)
);

-- 2. Doctors Table
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    ContactInfo VARCHAR(100),
    Experience INT,
    DepartmentID INT,
    Availability ENUM('Available', 'Unavailable') DEFAULT 'Available',
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- 3. Departments Table
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100),
    HeadDoctor VARCHAR(100)
);

-- 4. Appointments Table
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATETIME,
    Reason VARCHAR(255),
    Status ENUM('Pending', 'Completed', 'Cancelled'),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- 5. Medications Table
CREATE TABLE Medications (
    MedicationID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Dosage VARCHAR(50),
    SideEffects VARCHAR(255),
    Price DECIMAL(10, 2)
);

-- 6. Prescriptions Table
CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY AUTO_INCREMENT,
    DoctorID INT,
    PatientID INT,
    MedicationID INT,
    Dosage VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID)
);

-- 7. Bills Table


-- 8. Rooms Table
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY AUTO_INCREMENT,
    RoomType ENUM('Single', 'Shared', 'ICU'),
    Capacity INT,
    Availability ENUM('Available', 'Occupied'),
    Charges DECIMAL(10, 2)
);

-- 9. Staff Table
CREATE TABLE Staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Role VARCHAR(100),
    DepartmentID INT,
    ContactInfo VARCHAR(100),
    ShiftDetails VARCHAR(100),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- 10. LabTests Table
CREATE TABLE LabTests (
    TestID INT PRIMARY KEY AUTO_INCREMENT,
    TestName VARCHAR(100),
    TestCost DECIMAL(10, 2),
    TestResults VARCHAR(255),
    PatientID INT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- First truncate all tables in correct order
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE Bills;
TRUNCATE TABLE Prescriptions;
TRUNCATE TABLE LabTests;
TRUNCATE TABLE Appointments;
TRUNCATE TABLE Staff;
TRUNCATE TABLE Rooms;
TRUNCATE TABLE Medications;
TRUNCATE TABLE Doctors;
TRUNCATE TABLE Patients;
TRUNCATE TABLE Departments;

SET FOREIGN_KEY_CHECKS = 1;

-- Insert Departments
INSERT INTO Departments (Name, Location, HeadDoctor) VALUES
('Cardiology', 'Building A, Floor 2', 'Dr. Sharma'),
('Neurology', 'Building B, Floor 1', 'Dr. Patel'),
('Pediatrics', 'Building A, Floor 1', 'Dr. Gupta'),
('Orthopedics', 'Building C, Floor 2', 'Dr. Singh'),
('Emergency', 'Building A, Ground Floor', 'Dr. Kumar'),
('Dermatology', 'Building B, Floor 2', 'Dr. Reddy'),
('ENT', 'Building C, Floor 1', 'Dr. Kapoor');

-- Insert Doctors
INSERT INTO Doctors (Name, Specialization, ContactInfo, Experience, DepartmentID, Availability) VALUES
('Dr. Rajesh Sharma', 'Cardiologist', 'sharma@hospital.com', 15, 1, 'Available'),
('Dr. Priya Patel', 'Neurologist', 'patel@hospital.com', 12, 2, 'Available'),
('Dr. Amit Gupta', 'Pediatrician', 'gupta@hospital.com', 10, 3, 'Available'),
('Dr. Harpreet Singh', 'Orthopedic Surgeon', 'singh@hospital.com', 8, 4, 'Available'),
('Dr. Suresh Kumar', 'Emergency Medicine', 'kumar@hospital.com', 20, 5, 'Available'),
('Dr. Deepa Reddy', 'Dermatologist', 'reddy@hospital.com', 14, 6, 'Available'),
('Dr. Vikram Kapoor', 'ENT Specialist', 'kapoor@hospital.com', 16, 7, 'Available');

-- Insert Staff (Receptionists and Lab Technicians)
INSERT INTO Staff (Name, Role, DepartmentID, ContactInfo, ShiftDetails) VALUES
('Anjali Verma', 'Receptionist', 1, '555-0201', 'Morning Shift'),
('Rahul Malhotra', 'Lab Technician', 2, '555-0202', 'Evening Shift'),
('Pooja Saxena', 'Receptionist', 3, '555-0203', 'Morning Shift'),
('Karthik Rajan', 'Lab Technician', 4, '555-0204', 'Night Shift'),
('Neha Mehra', 'Receptionist', 5, '555-0205', 'Evening Shift'),
('Sanjay Desai', 'Lab Technician', 6, '555-0206', 'Morning Shift');

-- Insert Medications
INSERT INTO Medications (Name, Dosage, SideEffects, Price) VALUES
('Crocin', '500mg', 'Mild drowsiness', 9.99),
('Azithral', '250mg', 'Nausea, stomach upset', 19.99),
('Telma', '40mg', 'Dizziness, headache', 29.99),
('Metformin', '500mg', 'Stomach pain, nausea', 24.99),
('Pan-D', '40mg', 'Headache, dryness', 14.99),
('Allegra', '120mg', 'Drowsiness', 12.99),
('Saridon', '500mg', 'Mild sedation', 8.99),
('Thyronorm', '100mcg', 'Weight changes', 22.99);

-- Insert large number of patients with Indian names
INSERT INTO Patients (Name, DOB, Gender, ContactInfo, Address, InsuranceDetails, EmergencyContact) VALUES
('Aarav Sharma', '1990-05-15', 'Male', '555-0101', '123 Gandhi Road', 'Insurance A123', '555-0102'),
('Diya Patel', '1985-08-22', 'Female', '555-0103', '456 Nehru Street', 'Insurance B456', '555-0104'),
('Arjun Singh', '1995-03-30', 'Male', '555-0105', '789 Tagore Lane', 'Insurance C789', '555-0106'),
('Zara Khan', '1982-11-08', 'Female', '555-0107', '321 Bose Road', 'Insurance D321', '555-0108'),
('Kabir Malhotra', '1992-07-19', 'Male', '555-0109', '654 Raman Street', 'Insurance E654', '555-0110'),
('Ananya Reddy', '1988-12-03', 'Female', '555-0111', '987 Krishna Nagar', 'Insurance F987', '555-0112'),
('Ishaan Gupta', '1993-09-27', 'Male', '555-0113', '147 Indira Colony', 'Insurance G147', '555-0114'),
('Aisha Kapoor', '1987-04-14', 'Female', '555-0115', '258 Patel Nagar', 'Insurance H258', '555-0116'),
('Vihaan Kumar', '1991-01-25', 'Male', '555-0117', '369 Rajaji Street', 'Insurance I369', '555-0118'),
('Riya Mehta', '1994-06-08', 'Female', '555-0119', '741 Shastri Road', 'Insurance J741', '555-0120'),
('Aryan Verma', '1984-02-17', 'Male', '555-0121', '852 Bharati Lane', 'Insurance K852', '555-0122'),
('Saanvi Chopra', '1989-10-30', 'Female', '555-0123', '963 Subhash Nagar', 'Insurance L963', '555-0124'),
('Reyansh Shah', '1996-07-11', 'Male', '555-0125', '159 Tilak Road', 'Insurance M159', '555-0126'),
('Advait Joshi', '1993-03-22', 'Male', '555-0127', '753 Vivekananda St', 'Insurance N753', '555-0128'),
('Kiara Sinha', '1990-11-15', 'Female', '555-0129', '264 Ambedkar Road', 'Insurance O264', '555-0130'),
('Vivaan Saxena', '1987-08-04', 'Male', '555-0131', '951 Azad Nagar', 'Insurance P951', '555-0132'),
('Anika Desai', '1992-04-19', 'Female', '555-0133', '357 Bhabha Colony', 'Insurance Q357', '555-0134'),
('Dhruv Mehra', '1985-12-28', 'Male', '555-0135', '846 Tagore Nagar', 'Insurance R846', '555-0136'),
('Myra Rajput', '1994-09-07', 'Female', '555-0137', '153 Gandhi Colony', 'Insurance S153', '555-0138'),
('Advik Choudhury', '1991-05-16', 'Male', '555-0139', '759 Nehru Nagar', 'Insurance T759', '555-0140');

-- Insert Rooms
INSERT INTO Rooms (RoomType, Capacity, Availability, Charges) VALUES
('Single', 1, 'Available', 2000.00),
('Shared', 2, 'Available', 1500.00),
('ICU', 1, 'Available', 5000.00),
('Single', 1, 'Occupied', 2000.00),
('Shared', 2, 'Available', 1500.00),
('ICU', 1, 'Available', 5000.00),
('Single', 1, 'Available', 2000.00),
('Shared', 2, 'Occupied', 1500.00);

-- Insert Appointments for next 5 days (multiple appointments per doctor per day)
-- Using variables to make date handling easier
SET @current_date = CURDATE();

INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Reason, Status)
SELECT 
    p.PatientID,
    d.DoctorID,
    TIMESTAMP(
        DATE_ADD(@current_date, INTERVAL (a.day_offset) DAY),
        MAKETIME(FLOOR(RAND() * 8) + 9, FLOOR(RAND() * 12) * 5, 0)
    ) as AppointmentDate,
    CASE FLOOR(RAND() * 5)
        WHEN 0 THEN 'Regular checkup'
        WHEN 1 THEN 'Fever and cold'
        WHEN 2 THEN 'Follow-up'
        WHEN 3 THEN 'Consultation'
        ELSE 'Emergency'
    END as Reason,
    'Pending' as Status
FROM 
    (SELECT 1 as day_offset UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) a
    CROSS JOIN Patients p
    CROSS JOIN Doctors d
WHERE 
    RAND() < 0.3  -- This creates appointments for roughly 30% of possible combinations
ORDER BY RAND()
LIMIT 100;  -- Limiting to 100 total appointments

-- Insert Prescriptions
INSERT INTO Prescriptions (DoctorID, PatientID, MedicationID, Dosage, StartDate, EndDate)
SELECT 
    a.DoctorID,
    a.PatientID,
    FLOOR(RAND() * 8) + 1 as MedicationID,
    CASE FLOOR(RAND() * 3)
        WHEN 0 THEN '1 tablet daily'
        WHEN 1 THEN '2 tablets twice daily'
        ELSE '1 tablet three times daily'
    END as Dosage,
    DATE(a.AppointmentDate) as StartDate,
    DATE_ADD(DATE(a.AppointmentDate), INTERVAL FLOOR(RAND() * 10 + 5) DAY) as EndDate
FROM 
    Appointments a
WHERE 
    a.Status = 'Completed'
LIMIT 50;

-- Insert Bills
INSERT INTO Bills (PatientID, TotalAmount, Date, Status, InsuranceCovered)
SELECT 
    PatientID,
    ROUND(RAND() * 9000 + 1000, 2) as TotalAmount,
    DATE(AppointmentDate) as Date,
    CASE WHEN RAND() < 0.7 THEN 'Paid' ELSE 'Unpaid' END as Status,
    CASE WHEN RAND() < 0.8 THEN 1 ELSE 0 END as InsuranceCovered
FROM 
    Appointments
LIMIT 50;

-- Insert LabTests
INSERT INTO LabTests (TestName, TestCost, TestResults, PatientID)
SELECT 
    CASE FLOOR(RAND() * 5)
        WHEN 0 THEN 'Complete Blood Count'
        WHEN 1 THEN 'Lipid Profile'
        WHEN 2 THEN 'Thyroid Function Test'
        WHEN 3 THEN 'Liver Function Test'
        ELSE 'Kidney Function Test'
    END as TestName,
    ROUND(RAND() * 900 + 100, 2) as TestCost,
    CASE FLOOR(RAND() * 3)
        WHEN 0 THEN 'Normal'
        WHEN 1 THEN 'Slightly elevated levels'
        ELSE 'Requires follow-up'
    END as TestResults,
    PatientID
FROM 
    Patients
WHERE 
    RAND() < 0.7
LIMIT 40;

CREATE TABLE IF NOT EXISTS LabTests (
    TestID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT NOT NULL,
    TestName VARCHAR(100) NOT NULL,
    TestResults TEXT,
    TestCost DECIMAL(10,2),
    TestDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

