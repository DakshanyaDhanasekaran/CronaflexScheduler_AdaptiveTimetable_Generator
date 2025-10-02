import sqlite3
import json
import os

DB_NAME = 'cronaflex.db'

# --- 11 Total Staff Definitions and Subject Assignments ---
STAFF_ASSIGNMENTS = {
    'Web Tech.': 'T101', 'Ethical Hacking': 'T102', 'IoT': 'T103', 
    'Hospital Waste Mgmt.': 'T104', 'Compiler Eng.': 'T105', 'Artificial Intelligence': 'T106', 
    
    # Labs assigned to Theory Staff + 1 dedicated Lab Staff (2 staff total for these labs)
    'Web Tech. Lab': 'T101, L201',  
    'IoT Lab': 'T103, L202',

    # Labs assigned to 2 different dedicated Lab Staff (2 staff total)
    'TSP Lab': 'L203', 
    'Project Dev. Lab': 'L204',
    
    'Library': 'Librarian' 
}

# Define subject loads (Total 34 hours)
SUBJECT_LOADS = {
    'Web Tech. Lab': 3, 'Ethical Hacking': 4, 'IoT': 4, 'IoT Lab': 3,
    'Hospital Waste Mgmt.': 3, 'TSP Lab': 2, 'Project Dev. Lab': 2,
    'Compiler Eng.': 4, 'Web Tech.': 4, 'Artificial Intelligence': 4,
    'Library': 1 
}
TOTAL_REQUIRED_HOURS = sum(SUBJECT_LOADS.values())

# Complete list of all 11 staff names and IDs
ALL_STAFF_DETAILS = [
    ('T101', 'Dr. Web', 'CS'), ('T102', 'Dr. Ethics', 'CS'), ('T103', 'Dr. IOT', 'CS'),
    ('T104', 'Dr. Waste', 'CS'), ('T105', 'Dr. Compile', 'CS'), ('T106', 'Dr. AI', 'CS'),
    ('L201', 'Mr. Lab1', 'CS'), ('L202', 'Ms. Lab2', 'CS'), ('L203', 'Mr. TSP', 'CS'),
    ('L204', 'Ms. Project', 'CS'), ('Librarian', 'Ms. Read', 'Library')
]

def get_db_connection():
    """Returns a connection object to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Ensures tables exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            staff_name TEXT NOT NULL,
            department TEXT NOT NULL,
            max_workload INTEGER NOT NULL,
            availability_matrix TEXT
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS batch_subjects (
            subject_code TEXT PRIMARY KEY,
            subject_name TEXT NOT NULL,
            assigned_faculty_id TEXT,
            weekly_hours INTEGER NOT NULL,
            batch_id TEXT
        );
    ''')
    conn.commit()
    conn.close()

def clear_data():
    """Clears all dynamic data from the system."""
    conn = get_db_connection()
    conn.execute("DELETE FROM staff")
    conn.execute("DELETE FROM batch_subjects")
    conn.commit()
    conn.close()

def get_full_staff_list():
    """Returns the list of all staff IDs and Names for the dropdown."""
    return ALL_STAFF_DETAILS

# --- This function fixes the AttributeError ---
def insert_faculty_data_all_11(selected_staff_id, workload_constraint):
    """Inserts all 11 faculty members, applying the constraint only to the selected one."""
    conn = get_db_connection()
    availability_data = json.dumps({}) 
    
    conn.execute("DELETE FROM staff")

    for s_id, s_name, dept in ALL_STAFF_DETAILS:
        current_workload = 40 # Default high workload for all staff
        
        # Apply the user's input constraint ONLY to the selected staff member
        if s_id == selected_staff_id:
            current_workload = workload_constraint
            
        conn.execute(
            "INSERT INTO staff (staff_id, staff_name, department, max_workload, availability_matrix) VALUES (?, ?, ?, ?, ?)",
            (s_id, s_name, dept, current_workload, availability_data)
        )

    conn.commit()

def insert_all_subjects():
    """Inserts all subjects, assigned to the primary staff member for the load calculation."""
    conn = get_db_connection()
    conn.execute("DELETE FROM batch_subjects")

    subject_counter = 1
    for name, hours in SUBJECT_LOADS.items():
        assignment_str = STAFF_ASSIGNMENTS[name]
        primary_faculty_id = assignment_str.split(',')[0].strip()
        
        conn.execute("INSERT INTO batch_subjects VALUES (?, ?, ?, ?, ?)", 
                     (f'SUB{subject_counter}', name, primary_faculty_id, hours, 'B101'))
        subject_counter += 1

    conn.commit()
import sqlite3
import json
import os

DB_NAME = 'cronaflex.db'

# --- 11 Total Staff Definitions and Subject Assignments ---
STAFF_ASSIGNMENTS = {
    'Web Tech.': 'T101', 'Ethical Hacking': 'T102', 'IoT': 'T103', 
    'Hospital Waste Mgmt.': 'T104', 'Compiler Eng.': 'T105', 'Artificial Intelligence': 'T106', 
    
    # Labs assigned to Theory Staff + 1 dedicated Lab Staff (2 staff total for these labs)
    'Web Tech. Lab': 'T101, L201',  
    'IoT Lab': 'T103, L202',

    # Labs assigned to 2 different dedicated Lab Staff (2 staff total)
    'TSP Lab': 'L203', 
    'Project Dev. Lab': 'L204',
    
    'Library': 'Librarian' 
}

# Define subject loads (Total 34 hours)
SUBJECT_LOADS = {
    'Web Tech. Lab': 3, 'Ethical Hacking': 4, 'IoT': 4, 'IoT Lab': 3,
    'Hospital Waste Mgmt.': 3, 'TSP Lab': 2, 'Project Dev. Lab': 2,
    'Compiler Eng.': 4, 'Web Tech.': 4, 'Artificial Intelligence': 4,
    'Library': 1 
}
TOTAL_REQUIRED_HOURS = sum(SUBJECT_LOADS.values())

# Complete list of all 11 staff names and IDs
ALL_STAFF_DETAILS = [
    ('T101', 'Dr. Web', 'CS'), ('T102', 'Dr. Ethics', 'CS'), ('T103', 'Dr. IOT', 'CS'),
    ('T104', 'Dr. Waste', 'CS'), ('T105', 'Dr. Compile', 'CS'), ('T106', 'Dr. AI', 'CS'),
    ('L201', 'Mr. Lab1', 'CS'), ('L202', 'Ms. Lab2', 'CS'), ('L203', 'Mr. TSP', 'CS'),
    ('L204', 'Ms. Project', 'CS'), ('Librarian', 'Ms. Read', 'Library')
]

def get_db_connection():
    """Returns a connection object to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Ensures tables exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            staff_name TEXT NOT NULL,
            department TEXT NOT NULL,
            max_workload INTEGER NOT NULL,
            availability_matrix TEXT
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS batch_subjects (
            subject_code TEXT PRIMARY KEY,
            subject_name TEXT NOT NULL,
            assigned_faculty_id TEXT,
            weekly_hours INTEGER NOT NULL,
            batch_id TEXT
        );
    ''')
    conn.commit()
    conn.close()

def clear_data():
    """Clears all dynamic data from the system."""
    conn = get_db_connection()
    conn.execute("DELETE FROM staff")
    conn.execute("DELETE FROM batch_subjects")
    conn.commit()
    conn.close()

def get_full_staff_list():
    """Returns the list of all staff IDs and Names for the dropdown."""
    return ALL_STAFF_DETAILS

# --- This function fixes the AttributeError ---
def insert_faculty_data_all_11(selected_staff_id, workload_constraint):
    """Inserts all 11 faculty members, applying the constraint only to the selected one."""
    conn = get_db_connection()
    availability_data = json.dumps({}) 
    
    conn.execute("DELETE FROM staff")

    for s_id, s_name, dept in ALL_STAFF_DETAILS:
        current_workload = 40 # Default high workload for all staff
        
        # Apply the user's input constraint ONLY to the selected staff member
        if s_id == selected_staff_id:
            current_workload = workload_constraint
            
        conn.execute(
            "INSERT INTO staff (staff_id, staff_name, department, max_workload, availability_matrix) VALUES (?, ?, ?, ?, ?)",
            (s_id, s_name, dept, current_workload, availability_data)
        )

    conn.commit()

def insert_all_subjects():
    """Inserts all subjects, assigned to the primary staff member for the load calculation."""
    conn = get_db_connection()
    conn.execute("DELETE FROM batch_subjects")

    subject_counter = 1
    for name, hours in SUBJECT_LOADS.items():
        assignment_str = STAFF_ASSIGNMENTS[name]
        primary_faculty_id = assignment_str.split(',')[0].strip()
        
        conn.execute("INSERT INTO batch_subjects VALUES (?, ?, ?, ?, ?)", 
                     (f'SUB{subject_counter}', name, primary_faculty_id, hours, 'B101'))
        subject_counter += 1

    conn.commit()
    return TOTAL_REQUIRED_HOURS