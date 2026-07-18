import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# MODEL CONFIGURATIONS & FEATURE ORDERS
# -----------------------------
EMPLOYEE_OHE_COLS = [
    'job_role_Data Scientist',
    'job_role_Designer',
    'job_role_HR',
    'job_role_Marketing',
    'job_role_Project Manager',
    'job_role_Sales',
    'job_role_Software Engineer'
]

EMPLOYEE_FEATURES_ORDER = [
    'working_hours',
    'virtual_meetings',
    'work_life_balance',
    'access_to_mental_health',
    'satisfaction_with_remote_work',
    'company_support',
    'physical_activity',
    'sleep_quality',
    'meetings_per_hour'
] + EMPLOYEE_OHE_COLS

STUDENT_FEATURES_ORDER = [
    'anxiety_level',
    'depression',
    'sleep_quality',
    'academic_performance',
    'study_load',
    'teacher_student_relationship',
    'future_career_concerns',
    'social_support',
    'peer_pressure',
    'extracurricular_activities'
]

# -----------------------------
# LOAD MODELS ONCE AT STARTUP
# -----------------------------
employee_model = None
student_model = None

# Get base directory of current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
employee_model_path = os.path.join(BASE_DIR, 'employee_model.pkl')
student_model_path = os.path.join(BASE_DIR, 'student_model.pkl')

try:
    with open(employee_model_path, 'rb') as f:
        employee_model = pickle.load(f)
    print("Employee ML model loaded successfully.")
except Exception as e:
    print(f"Error loading employee model: {e}")

try:
    with open(student_model_path, 'rb') as f:
        student_model = pickle.load(f)
    print("Student ML model loaded successfully.")
except Exception as e:
    print(f"Error loading student model: {e}")

# -----------------------------
# SAFE INTEGER CAST
# -----------------------------
def safe_int_cast(value):
    try:
        return int(value)
    except:
        return 0

# -----------------------------
# PREPROCESSING FUNCTIONS
# -----------------------------
def preprocess_employee_data_for_prediction(df):
    access_to_mental_health_mapping = {'Yes': 1, 'No': 0}
    physical_activity_mapping = {'None': 0, 'Weekly': 1, 'Daily': 2}
    sleep_quality_mapping = {'Poor': 1, 'Average': 2, 'Good': 3}
    satisfaction_mapping = {'Unsatisfied': 0, 'Satisfied': 1}

    job_role_input = df['job_role'].iloc[0] if 'job_role' in df.columns else 'Unknown'
    if pd.isna(job_role_input):
        job_role_input = 'Unknown'

    df = df.drop(columns=['job_role'], errors='ignore')

    df['access_to_mental_health'] = (
        df['access_to_mental_health']
        .map(access_to_mental_health_mapping)
        .fillna(0)
        .astype(int)
    )

    df['physical_activity'] = (
        df['physical_activity']
        .map(physical_activity_mapping)
        .fillna(0)
        .astype(int)
    )

    df['sleep_quality'] = (
        df['sleep_quality']
        .map(sleep_quality_mapping)
        .fillna(0)
        .astype(int)
    )

    df['satisfaction_with_remote_work'] = (
        df['satisfaction_with_remote_work']
        .map(satisfaction_mapping)
        .fillna(0)
        .astype(int)
    )

    # meetings_per_hour
    virtual_meetings = safe_int_cast(df['virtual_meetings'].iloc[0])
    working_hours = safe_int_cast(df['working_hours'].iloc[0])
    
    if working_hours > 0:
        df['meetings_per_hour'] = virtual_meetings / working_hours
    else:
        df['meetings_per_hour'] = 0.0

    df['meetings_per_hour'] = (
        df['meetings_per_hour']
        .replace([np.inf, -np.inf, np.nan], 0)
    )

    # OHE Job Roles
    ohe_df = pd.DataFrame(0, index=df.index, columns=EMPLOYEE_OHE_COLS)
    ohe_col_name = f'job_role_{str(job_role_input).replace(" ", "_")}'
    if ohe_col_name in ohe_df.columns:
        ohe_df[ohe_col_name] = 1

    df = pd.concat([df, ohe_df], axis=1)
    df = df[EMPLOYEE_FEATURES_ORDER]
    return df


def preprocess_student_data_for_prediction(df):
    sleep_quality_mapping = {'Poor': 1, 'Average': 2, 'Good': 3}

    df['sleep_quality'] = (
        df['sleep_quality']
        .map(sleep_quality_mapping)
        .fillna(0)
        .astype(int)
    )

    if 'extracurricular_load' in df.columns:
        df.rename(
            columns={'extracurricular_load': 'extracurricular_activities'},
            inplace=True
        )
    elif 'extracurricular_activities' not in df.columns:
        df['extracurricular_activities'] = 0

    df = df[STUDENT_FEATURES_ORDER]
    return df

# -----------------------------
# PREDICT API ENDPOINT
# -----------------------------
@app.route('/predict_ml', methods=['POST'])
def predict_ml():
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing request body"}), 400

    role = body.get('role')
    data = body.get('data')

    if not role or not data:
        return jsonify({"error": "Missing 'role' or 'data' in request body"}), 400

    try:
        df = pd.DataFrame([data])
        
        if role == 'employee':
            if employee_model is None:
                return jsonify({"error": "Employee model is not loaded."}), 500
            
            df_prep = preprocess_employee_data_for_prediction(df)
            prediction = employee_model.predict(df_prep)
            
        elif role == 'student':
            if student_model is None:
                return jsonify({"error": "Student model is not loaded."}), 500
            
            df_prep = preprocess_student_data_for_prediction(df)
            prediction = student_model.predict(df_prep)
            
        else:
            return jsonify({"error": f"Invalid role '{role}'. Must be 'employee' or 'student'."}), 400

        stress_score = float(prediction[0])
        return jsonify({
            "stress_score": stress_score
        })

    except Exception as e:
        print(f"ML Microservice Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Listen on localhost port 5001
    app.run(host='0.0.0.0', port=5001)
