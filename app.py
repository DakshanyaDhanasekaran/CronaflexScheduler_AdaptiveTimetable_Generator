from flask import Flask, render_template, request, flash
import time
import db_connector
import validation_engine
from scheduling_engine import TimetableScheduler 

app = Flask(__name__)
app.secret_key = 'your_college_secret_key'

# --- Helper Function ---
def generate_summary(report):
    hard_fails = [i for i in report if i['type'] == 'HARD VIOLATION']
    summary = {
        'hard_fails': len(hard_fails),
        'can_proceed': len(hard_fails) == 0,
    }
    return summary

def run_pipeline(staff_id_selected, workload):
    """Executes the full pipeline: DB -> Validation -> Scheduling."""
    
    # 1. Clear DB and Store All 11 Staff Data, applying the constraint to the selected ID
    db_connector.clear_data()
    db_connector.insert_faculty_data_all_11(staff_id_selected, workload) 
    
    total_required_hours = db_connector.insert_all_subjects() 
    
    # 2. Constraint Validation (Targeted check)
    validation_report = validation_engine.run_validation(staff_id_selected, total_required_hours)
    summary = generate_summary(validation_report)

    # 3. Scheduling Engine (Runs ONLY if validation passes)
    scheduling_result = None
    if summary['can_proceed']:
        scheduler = TimetableScheduler()
        scheduling_result = scheduler.run_ga() 

    return {
        'scenario': 'Dynamic Input',
        'validation': {'report': validation_report, 'summary': summary},
        'final_schedule': scheduling_result
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    pipeline_data = None
    
    db_connector.init_db()
    # Insert initial staff data to populate the dropdown on first load
    db_connector.insert_faculty_data_all_11("MOCK_ID", 40) 
    staff_list = db_connector.get_full_staff_list()
    
    if request.method == 'POST':
        try:
            # Collect data from the form
            staff_id_selected = request.form['staff_id_selected'].strip().upper()
            workload = int(request.form['max_workload'])
            
            # Run the full pipeline with user data
            pipeline_data = run_pipeline(staff_id_selected, workload)
            
            # Flash final status message
            if pipeline_data['validation']['summary']['can_proceed']:
                flash('✅ Validation PASSED! Timetable generated successfully.', 'success')
            else:
                flash('❌ Validation FAILED! Timetable generation BLOCKED.', 'error')

        except Exception as e:
            flash(f'Error processing input: {e}', 'error')
            
    return render_template('report_ui.html', data=pipeline_data, staff_list=staff_list)

if __name__ == '__main__':
    db_connector.init_db() 
    db_connector.clear_data()
    app.run(debug=True)