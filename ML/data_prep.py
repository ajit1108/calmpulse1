import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================================================================
# EDA for cleaned_employeedataset_advanced.csv
# ==============================================================================

try:
    # --- FIX 1: Use the correct, advanced cleaned filename ---
    cleaned_employee_file = 'cleaned_employeedataset_advanced.csv'
    if not os.path.exists(cleaned_employee_file):
        raise FileNotFoundError(f"Cleaned file '{cleaned_employee_file}' not found. Please run data_prep.py first.")
    
    df_employee = pd.read_csv(cleaned_employee_file)
    print("--- Exploratory Data Analysis for Employee Dataset ---")

    # --- FIX 2: Use the correct, lowercase column names (snake_case) ---
    numerical_cols = ['working_hours', 'virtual_meetings', 'work_life_balance', 
                      'stress_score', 'access_to_mental_health', 'company_support', 
                      'physical_activity', 'sleep_quality']
    
    print("\nDescriptive Statistics for Numerical Columns:")
    print(df_employee[numerical_cols].describe())
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df_employee['working_hours'], kde=True)
    plt.title('Distribution of Working Hours Per Week')
    plt.subplot(1, 2, 2)
    sns.histplot(df_employee['virtual_meetings'], kde=True)
    plt.title('Distribution of Number of Virtual Meetings')
    plt.tight_layout()
    plt.show()

    # Bivariate Analysis: Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_employee[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Employee Metrics')
    plt.show()

    # Bivariate Analysis: Categorical vs. Numerical Box Plot
    plt.figure(figsize=(12, 6))
    # Using 'job_role' which is the correct snake_case name
    sns.boxplot(x='job_role', y='working_hours', data=df_employee)
    plt.title('Hours Worked Per Week by Job Role')
    plt.xticks(rotation=45)
    plt.show()

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred with the employee dataset: {e}")

print("\n" + "="*80 + "\n")

# ==============================================================================
# EDA for cleaned_studentdataset_advanced.csv
# ==============================================================================

try:
    # --- FIX 3: Use the correct, advanced cleaned filename ---
    cleaned_student_file = 'cleaned_studentdataset_advanced.csv'
    if not os.path.exists(cleaned_student_file):
        raise FileNotFoundError(f"Cleaned file '{cleaned_student_file}' not found. Please run data_prep.py first.")
    
    df_student = pd.read_csv(cleaned_student_file)
    print("--- Exploratory Data Analysis for Student Dataset ---")

    # --- NEW FIX: Rename target variable if it still uses the original name (Stress_Level) ---
    if 'Stress_Level' in df_student.columns and 'stress_score' not in df_student.columns:
        df_student.rename(columns={'Stress_Level': 'stress_score'}, inplace=True)
    
    # --- FIX 4: Use the correct, lowercase column names (snake_case) ---
    print("\nDescriptive Statistics for Student Data:")
    print(df_student.describe())

    # --- Student Numerical Columns (ensuring 'stress_score' is included) ---
    student_numerical_cols = [
        'anxiety_level', 'depression', 'academic_performance', 'study_load', 
        'teacher_student_relationship', 'future_career_concerns', 'social_support', 
        'peer_pressure', 'extracurricular_load', 'stress_score'
    ]
    
    # Filter columns to only include those present in the DataFrame
    present_numerical_cols = [col for col in student_numerical_cols if col in df_student.columns]
    
    # Bivariate Analysis: Correlation Heatmap
    plt.figure(figsize=(12, 10))
    # Use only present numerical columns for correlation to avoid key errors
    sns.heatmap(df_student[present_numerical_cols].corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Student Metrics')
    plt.show()

    # Bivariate Analysis: Pair Plot for key features
    # --- FIX 5: Use the correct snake_case column names ---
    important_features = ['anxiety_level', 'depression', 'academic_performance', 'sleep_quality', 'stress_score']
    # Filter important features to only include those present
    present_important_features = [col for col in important_features if col in df_student.columns]
    
    if present_important_features:
        sns.pairplot(df_student[present_important_features])
        plt.suptitle('Pairwise Relationships of Key Student Metrics', y=1.02)
        plt.show()

    # Bivariate Analysis: Box plot of key features vs. stress_score
    if 'stress_score' in df_student.columns: # Check existence before plotting
        plt.figure(figsize=(15, 6))
        plt.subplot(1, 2, 1)
        sns.boxplot(x='stress_score', y='anxiety_level', data=df_student)
        plt.title('Anxiety Level by Stress Score')
        plt.subplot(1, 2, 2)
        sns.boxplot(x='stress_score', y='depression', data=df_student)
        plt.title('Depression by Stress Score')
        plt.tight_layout()
        plt.show()
    else:
        # This message will still appear if the column is truly missing from the saved file.
        print("\nSkipping Box Plots: 'stress_score' column not found. Rerun data_prep.py with the target variable renamed.") 

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred with the student dataset: {e}")
