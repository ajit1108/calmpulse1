import pickle

try:
    with open('student_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Common attribute names where feature list is stored
    if hasattr(model, 'feature_names_in_'):
        print("Model Features (feature_names_in_):")
        print(model.feature_names_in_.tolist())
    elif hasattr(model, 'feature_names'):
        print("Model Features (feature_names):")
        print(model.feature_names)
    else:
        print("Could not find feature names attribute directly in the model.")
        
except FileNotFoundError:
    print("Error: 'student_model.pkl' not found.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
