from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load the ML model
model_path = 'svc.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        print("Model loaded successfully!")
else:
    raise FileNotFoundError(f"Error: {model_path} not found!")

# Load datasets
diets = pd.read_csv('diets.csv')
medications = pd.read_csv('medications.csv')
workout = pd.read_csv('workout_df.csv')
description = pd.read_csv('description.csv')
precautions = pd.read_csv('precautions_df.csv')

# Symptom dictionary for encoding the symptoms
symptoms_dict = {  'itching': 0, 'skin rash': 1, 'nodal skin eruptions': 2, 'continuous sneezing': 3, 'shivering': 4, 'chills': 5, 'joint pain': 6, 'stomach pain': 7, 'acidity': 8, 'ulcers on tongue': 9,
    'muscle wasting': 10, 'vomiting': 11, 'burning micturition': 12, 'spotting urination': 13, 'fatigue': 14, 'weight gain': 15, 'anxiety': 16, 'cold hands and feets': 17, 'mood swings': 18,
    'weight loss': 19, 'restlessness': 20, 'lethargy': 21,
    'patches in throat': 22, 'irregular sugar level': 23, 'cough': 24, 'high fever': 25, 'sunken eyes': 26, 'breathlessness': 27, 'sweating': 28,
    'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish skin': 32, 'dark urine': 33, 'nausea': 34, 'loss of appetite': 35, 'pain behind the eyes': 36,
    'back pain': 37, 'constipation': 38, 'abdominal pain': 39, 'diarrhoea': 40, 'mild fever': 41, 'yellow urine': 42, 'yellowing of eyes': 43, 'acute liver failure': 44,
    'fluid overload': 45, 'swelling of stomach': 46, 'swelled lymph_nodes': 47, 'malaise': 48, 'blurred and distorted vision': 49, 'phlegm': 50, 'throat irritation': 51,
    'redness of eyes': 52, 'sinus pressure': 53, 'runny nose': 54, 'congestion': 55,
    'chest pain': 56, 'weakness in limbs': 57, 'e': 58, 'pain during bowel movements': 59, 'pain in anal region': 60, 'bloody stool': 61, 'irritation in anus': 62, 'neck pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen legs': 68,
      'swollen blood vessels': 69, 'puffy face and eyes': 70, 'enlarged thyroid': 71, 'brittle nails': 72,
      'swollen extremities': 73, 'excessive hunger': 74, 'extra marital contacts': 75, 'drying and tingling lips': 76, 'slurred speech': 77, 'knee pain': 78, 'hip joint_pain': 79, 'muscle weakness': 80, 'stiffneck': 81, 'swelling joints': 82, 'movement stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87,
      'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dichromatic_patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108,
    'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131
}

# Disease list dictionary for decoding the predicted disease label
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine',
                7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E',
                3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5:
                'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'

}

# Helper function to fetch details based on disease
def fetch_details(disease):
    desc = description[description['Disease'] == disease]['Description'].values[0] if not description[description['Disease'] == disease].empty else "No description available."
    pre = precautions[precautions['Disease'] == disease][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values
    pre_list = pre[0] if len(pre) > 0 else ["No precautions listed."]
    meds = medications[medications['Disease'] == disease]['Medication'].values if not medications[medications['Disease'] == disease].empty else ["No medications listed."]
    diet = diets[diets['Disease'] == disease]['Diet'].values if not diets[diets['Disease'] == disease].empty else ["No diet listed."]
    wrkout = workout[workout['Disease'] == disease]['workout'].values if not workout[workout['Disease'] == disease].empty else ["No workout listed."]
    return desc, pre_list, meds, diet, wrkout

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms', [])
    input_vector = np.zeros(len(symptoms_dict))

    for symptom in symptoms:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1

    predicted_disease = model.predict([input_vector])[0]
    disease_name = diseases_list.get(predicted_disease, "Unknown disease")
    desc, pre, meds, diet, wrkout = fetch_details(disease_name)

    response = {
        "disease": disease_name,
        "description": desc,
        "precautions": pre.tolist() if isinstance(pre, np.ndarray) else pre,
        "medications": meds.tolist() if isinstance(meds, np.ndarray) else meds,
        "diet": diet.tolist() if isinstance(diet, np.ndarray) else diet,
        "workout": wrkout.tolist() if isinstance(wrkout, np.ndarray) else wrkout
    }

    return jsonify(response)

# Health check endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is running!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
