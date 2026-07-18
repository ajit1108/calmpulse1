import flask
import pickle
import pandas as pd
import csv
import os
import numpy as np
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import google.generativeai as genai

# -----------------------------
# FLASK APP
# -----------------------------
app = flask.Flask(__name__)
CORS(app)

# -----------------------------
# MONGODB CONFIGURATION
# -----------------------------
app.config["MONGO_URI"] = "mongodb+srv://ajitbirajdar1108:Ajit%401108@cluster0.z6qsfui.mongodb.net/calmpulse?retryWrites=true&w=majority&appName=Cluster0"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

users_collection = mongo.db.users
history_collection = mongo.db.stress_history

# -----------------------------
# GEMINI AI CONFIG
# -----------------------------
client = None

try:
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    client = genai.GenerativeModel("gemini-2.5-flash")
    print("Gemini AI Initialized")
except Exception as e:
    print(f"Gemini Error: {e}")

# -----------------------------
# EMPLOYEE MODEL FEATURES
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

# -----------------------------
# STUDENT MODEL FEATURES
# -----------------------------
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
# LOAD MODELS
# -----------------------------
try:
    with open('employee_model.pkl', 'rb') as f:
        employee_model = pickle.load(f)

    with open('student_model.pkl', 'rb') as f:
        student_model = pickle.load(f)

    print("Models Loaded Successfully")

except FileNotFoundError:
    employee_model = None
    student_model = None
    print("Model files not found")

# -----------------------------
# SAFE INTEGER CAST
# -----------------------------
def safe_int_cast(value):
    try:
        return int(value)
    except:
        return 0

# -----------------------------
# EMPLOYEE PREPROCESSING
# -----------------------------
def preprocess_employee_data_for_prediction(df):

    access_to_mental_health_mapping = {
        'Yes': 1,
        'No': 0
    }

    physical_activity_mapping = {
        'None': 0,
        'Weekly': 1,
        'Daily': 2
    }

    sleep_quality_mapping = {
        'Poor': 1,
        'Average': 2,
        'Good': 3
    }

    satisfaction_mapping = {
        'Unsatisfied': 0,
        'Satisfied': 1
    }

    job_role_input = df['job_role'].iloc[0]

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

    df['meetings_per_hour'] = (
        df['virtual_meetings'] / df['working_hours']
    )

    df['meetings_per_hour'] = (
        df['meetings_per_hour']
        .replace([np.inf, -np.inf, np.nan], 0)
    )

    ohe_df = pd.DataFrame(
        0,
        index=df.index,
        columns=EMPLOYEE_OHE_COLS
    )

    ohe_col_name = f'job_role_{str(job_role_input).replace(" ", "_")}'

    if ohe_col_name in ohe_df.columns:
        ohe_df[ohe_col_name] = 1

    df = pd.concat([df, ohe_df], axis=1)

    df = df[EMPLOYEE_FEATURES_ORDER]

    return df

# -----------------------------
# STUDENT PREPROCESSING
# -----------------------------
def preprocess_student_data_for_prediction(df):

    sleep_quality_mapping = {
        'Poor': 1,
        'Average': 2,
        'Good': 3
    }

    df['sleep_quality'] = (
        df['sleep_quality']
        .map(sleep_quality_mapping)
        .fillna(0)
        .astype(int)
    )

    if 'extracurricular_load' in df.columns:
        df.rename(
            columns={
                'extracurricular_load':
                'extracurricular_activities'
            },
            inplace=True
        )

    df = df[STUDENT_FEATURES_ORDER]

    return df

# -----------------------------
# GENERATE SUGGESTIONS
# -----------------------------
def generate_suggestions(stress_score, input_data, user_role):

    suggestions = []

    if user_role == 'employee':

        if stress_score == 3:
            suggestions.append(
                "High stress detected. Take rest and manage workload."
            )

        elif stress_score == 2:
            suggestions.append(
                "Moderate stress detected. Improve work-life balance."
            )

        else:
            suggestions.append(
                "Low stress. Keep maintaining healthy habits."
            )

    elif user_role == 'student':

        if stress_score == 2:
            suggestions.append(
                "High stress detected. Talk with mentor or counselor."
            )

        elif stress_score == 1:
            suggestions.append(
                "Moderate stress detected. Take regular breaks."
            )

        else:
            suggestions.append(
                "Low stress. Continue healthy study habits."
            )

    return suggestions

# -----------------------------
# SIGNUP API
# -----------------------------
@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "error": "Missing email or password"
        }), 400

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    hashed_password = (
        bcrypt.generate_password_hash(password)
        .decode('utf-8')
    )

    user_data = {
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "contact": data.get('contact'),
        "email": email,
        "password_hash": hashed_password,
        "age": None,
        "gender": None,
        "role": None,
        "is_new_user": True
    }

    result = users_collection.insert_one(user_data)

    return jsonify({
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }), 201

# -----------------------------
# LOGIN API
# -----------------------------
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({
        "email": email
    })

    if user and bcrypt.check_password_hash(
        user['password_hash'],
        password
    ):

        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id']),
            "is_new_user": user.get('is_new_user', True),
            "role": user.get('role')
        }), 200

    return jsonify({
        "error": "Invalid credentials"
    }), 401

# -----------------------------
# PROFILE API
# -----------------------------
@app.route('/profile', methods=['POST'])
def save_profile():

    data = request.get_json()

    user_id = data.get('user_id')

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "first_name": data.get('first_name'),
                "last_name": data.get('last_name'),
                "age": data.get('age'),
                "gender": data.get('gender'),
                "contact": data.get('contact'),
                "role": data.get('mode'),
                "is_new_user": False
            }
        }
    )

    return jsonify({
        "message": "Profile updated successfully"
    })

# -----------------------------
# PREDICT API
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()

    user_id = data.get('user_id')

    user = users_collection.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    input_data = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'job_role': data.get('job_role'),
        'working_hours': safe_int_cast(
            data.get('working_hours')
        ),
        'virtual_meetings': safe_int_cast(
            data.get('virtual_meetings')
        ),
        'work_life_balance': safe_int_cast(
            data.get('work_life_balance')
        ),
        'access_to_mental_health': data.get(
            'access_to_mental_health'
        ),
        'satisfaction_with_remote_work': data.get(
            'satisfaction_with_remote_work'
        ),
        'company_support': safe_int_cast(
            data.get('company_support')
        ),
        'physical_activity': data.get(
            'physical_activity'
        ),
        'sleep_quality': data.get(
            'sleep_quality'
        ),
        'anxiety_level': safe_int_cast(
            data.get('anxiety_level')
        ),
        'depression': safe_int_cast(
            data.get('depression')
        ),
        'academic_performance': safe_int_cast(
            data.get('academic_performance')
        ),
        'study_load': safe_int_cast(
            data.get('study_load')
        ),
        'teacher_student_relationship': safe_int_cast(
            data.get('teacher_student_relationship')
        ),
        'future_career_concerns': safe_int_cast(
            data.get('future_career_concerns')
        ),
        'social_support': safe_int_cast(
            data.get('social_support')
        ),
        'peer_pressure': safe_int_cast(
            data.get('peer_pressure')
        ),
        'extracurricular_load': safe_int_cast(
            data.get('extracurricular_load')
        )
    }

    try:

        df_features = pd.DataFrame([input_data])

        if user['role'] == 'employee':

            df_features = df_features.drop(
                columns=[
                    'timestamp',
                    'user_id',
                    'anxiety_level',
                    'depression',
                    'academic_performance',
                    'study_load',
                    'teacher_student_relationship',
                    'future_career_concerns',
                    'social_support',
                    'peer_pressure',
                    'extracurricular_load'
                ],
                errors='ignore'
            )

            df_features = (
                preprocess_employee_data_for_prediction(
                    df_features
                )
            )

            prediction = employee_model.predict(
                df_features
            )

        else:

            df_features = df_features.drop(
                columns=[
                    'timestamp',
                    'user_id',
                    'job_role',
                    'working_hours',
                    'virtual_meetings',
                    'work_life_balance',
                    'access_to_mental_health',
                    'satisfaction_with_remote_work',
                    'company_support',
                    'physical_activity'
                ],
                errors='ignore'
            )

            df_features = (
                preprocess_student_data_for_prediction(
                    df_features
                )
            )

            prediction = student_model.predict(
                df_features
            )

        stress_score = float(prediction[0])

        input_data['stress_score'] = stress_score

        history_collection.insert_one(input_data)

        suggestions = generate_suggestions(
            stress_score,
            input_data,
            user['role']
        )

        return jsonify({
            "stress_score": stress_score,
            "suggestions": suggestions
        })

    except Exception as e:

        print(f"Prediction Error: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# HISTORY API
# -----------------------------
@app.route('/history/<string:user_id>', methods=['GET'])
def get_history(user_id):

    records = history_collection.find({
        "user_id": user_id
    })

    history = []

    for record in records:

        history.append({
            "stress_score": record.get('stress_score'),
            "timestamp": record.get('timestamp'),
            "factors": {
                "sleep_quality": record.get(
                    'sleep_quality'
                ),
                "working_hours": record.get(
                    'working_hours'
                ),
                "virtual_meetings": record.get(
                    'virtual_meetings'
                ),
                "anxiety_level": record.get(
                    'anxiety_level'
                ),
                "depression": record.get(
                    'depression'
                )
            }
        })

    return jsonify(history)

# -----------------------------
# AI CHATBOT API
# -----------------------------
@app.route('/chat_api', methods=['POST'])
def chat_api():

    if client is None:
        return jsonify({
            "response": "AI service unavailable"
        }), 503

    data = request.get_json()

    user_message = data.get('message', '')
    user_role = data.get('user_role', 'user')

    if not user_message:
        return jsonify({
            "response": "Message required"
        }), 400

    prompt = f"""
    You are a calm mental wellness assistant.
    User role: {user_role}

    User message:
    {user_message}
    """

    try:

        response = client.generate_content(prompt)

        return jsonify({
            "response": response.text
        })

    except Exception as e:

        print(f"Gemini Error: {e}")

        return jsonify({
            "response": "AI Error"
        }), 500

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':

    print("MongoDB Connected Successfully")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )