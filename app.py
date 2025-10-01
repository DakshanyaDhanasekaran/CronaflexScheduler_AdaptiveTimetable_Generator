import os
from flask import Flask, render_template, request, flash
import db_connector
import validation_engine
from scheduling_engine import TimetableScheduler

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_dev_secret")

def generate_summary(report):
    hard_fails = [i for i in report if i.get('type') == 'HARD VIOLATION']
    summary = {
        'hard_fails': len(hard_fails),
        'can_proceed': len(hard_fails) == 0,
    }
    return summary

def run_pipeline(staff_id_selected, workload):
    db_connector.clear_data()
    db_connector.insert_faculty_data_all_11(staff_id_selected, workload)
    total_required_hours = db_connector.insert_all_subjects()

    validation_report = validation_engine.run_validation(staff_id_selected, total_required_hours)
    summary = generate_summary(validation_report)

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

    # Initialize DB and staff list
    db_connector.init_db()
    db_connector.insert_faculty_data_all_11("MOCK_ID", 40)
    staff_list = db_connector.get_full_staff_list()

    if request.method == 'POST':
        try:
            staff_id_selected = request.form['staff_id_selected'].strip().upper()
            workload = int(request.form['max_workload'])
            pipeline_data = run_pipeline(staff_id_selected, workload)
            if pipeline_data['validation']['summary']['can_proceed']:
                flash('✅ Validation PASSED! Timetable generated successfully.', 'success')
            else:
                flash('❌ Validation FAILED! Timetable generation BLOCKED.', 'error')
        except Exception as e:
            flash(f'Error processing input: {e}', 'error')

    return render_template('report_ui.html', data=pipeline_data, staff_list=staff_list)

# Health check route
@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    db_connector.init_db()
    db_connector.clear_data()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
