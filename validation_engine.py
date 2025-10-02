<<<<<<< HEAD
from db_connector import get_db_connection

def validate_max_workload(conn, report, selected_staff_id, total_required_hours):
    """HARD CONSTRAINT: Checks if the total required load (34 hrs) exceeds the Max Workload of the SELECTED staff."""
    
    # Retrieve the data for the specific staff member selected in the dropdown
    staff_data = conn.execute("SELECT staff_id, staff_name, max_workload FROM staff WHERE staff_id = ?", (selected_staff_id,)).fetchone()

    if not staff_data:
        report.append({'type': 'HARD VIOLATION', 'rule': 'Staff Data Missing', 'entity': 'System', 'details': f'Could not find the selected staff member ({selected_staff_id}) in the database.'})
        return

    max_workload = staff_data['max_workload']
    
    # Check: Are the TOTAL hours required by the class (34) higher than the capacity of the faculty member being tested?
    if total_required_hours > max_workload:
        report.append({
            'type': 'HARD VIOLATION',
            'rule': 'Max Workload Exceeded',
            'entity': staff_data['staff_name'],
            'details': f"Total required course hours ({total_required_hours} hrs) exceeds the staff Max Workload constraint ({max_workload} hrs)."
        })

def run_validation(selected_staff_id, total_required_hours):
    """Executes all validation checks and returns the report list."""
    conn = get_db_connection()
    validation_report = []
    
    validate_max_workload(conn, validation_report, selected_staff_id, total_required_hours)
    
    conn.close()
=======
from db_connector import get_db_connection

def validate_max_workload(conn, report, selected_staff_id, total_required_hours):
    """HARD CONSTRAINT: Checks if the total required load (34 hrs) exceeds the Max Workload of the SELECTED staff."""
    
    # Retrieve the data for the specific staff member selected in the dropdown
    staff_data = conn.execute("SELECT staff_id, staff_name, max_workload FROM staff WHERE staff_id = ?", (selected_staff_id,)).fetchone()

    if not staff_data:
        report.append({'type': 'HARD VIOLATION', 'rule': 'Staff Data Missing', 'entity': 'System', 'details': f'Could not find the selected staff member ({selected_staff_id}) in the database.'})
        return

    max_workload = staff_data['max_workload']
    
    # Check: Are the TOTAL hours required by the class (34) higher than the capacity of the faculty member being tested?
    if total_required_hours > max_workload:
        report.append({
            'type': 'HARD VIOLATION',
            'rule': 'Max Workload Exceeded',
            'entity': staff_data['staff_name'],
            'details': f"Total required course hours ({total_required_hours} hrs) exceeds the staff Max Workload constraint ({max_workload} hrs)."
        })

def run_validation(selected_staff_id, total_required_hours):
    """Executes all validation checks and returns the report list."""
    conn = get_db_connection()
    validation_report = []
    
    validate_max_workload(conn, validation_report, selected_staff_id, total_required_hours)
    
    conn.close()
>>>>>>> 2c2f59cbed0206238ef81bae59663e5c2949a2b9
    return validation_report