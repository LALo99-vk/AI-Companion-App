import numpy as np
import pyttsx3
import speech_recognition as sr
import pickle
import pandas as pd
import time
import os

# Load the ML model
model_path = 'svc.pkl'  # Or provide the full/relative path as needed

if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        print("model loaded succesfully")
else:
    print(f"Error: {model_path} not found!")

# Load your datasets (ensure these CSV files exist in your project folder)
diets = pd.read_csv('diets.csv')  # CSV file containing diets for each disease
medications = pd.read_csv('medications.csv')  # CSV file containing medications for each disease
workout = pd.read_csv('workout_df.csv')  # CSV file containing workouts for each disease
description = pd.read_csv('description.csv')  # CSV file containing disease descriptions
precautions = pd.read_csv('precautions_df.csv')  # CSV file containing precautions for each disease
symptoms = pd.read_csv('symtoms_df.csv')



# Check if the 'Disease' column exists in the DataFrames
if 'Disease' not in description.columns:
    print("Error: 'Disease' column not found in description DataFrame.")
if 'Disease' not in medications.columns:
    print("Error: 'Disease' column not found in medications DataFrame.")
if 'Disease' not in workout.columns:
    print("Error: 'Disease' column not found in workout DataFrame.")
if 'Disease' not in diets.columns:
    print("Error: 'Disease' column not found in diets DataFrame.")
if 'Disease' not in precautions.columns:
    print("Error: 'Disease' column not found in precautions DataFrame.")




# Sample helper function to fetch data based on disease
def helper(Disease):
    # Fetch the description of the disease
    desc = description[description['Disease'] == Disease]['Description'].values[0] if not description[description['Disease'] == Disease].empty else "No description available."
    
    # Fetch precautions for the disease (assuming they are in separate columns like Precaution_1, Precaution_2, etc.)
    pre = precautions[precautions['Disease'] == Disease][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values
    pre_list = pre[0] if len(pre) > 0 else ["No precautions listed."]
    
    # Fetch medications for the disease
    meds = medications[medications['Disease'] == Disease]['Medication'].values if not medications[medications['Disease'] == Disease].empty else ["No medications listed."]
    
    # Fetch diet recommendations for the disease
    diet = diets[diets['Disease'] == Disease]['Diet'].values if not diets[diets['Disease'] == Disease].empty else ["No diet listed."]
    
    # Fetch workout recommendations for the disease
    wrkout = workout[workout['Disease'] == Disease]['workout'].values if not workout[workout['Disease'] == Disease].empty else ["No workout listed."]
    
    return desc, pre_list, meds, diet, wrkout

# Symptom dictionary for encoding the symptoms
symptoms_dict = {'itching': 0, 'skin rash': 1, 'nodal skin eruptions': 2, 'continuous sneezing': 3, 'shivering': 4, 'chills': 5, 'joint pain': 6, 'stomach pain': 7, 'acidity': 8, 'ulcers on tongue': 9, 
    'muscle wasting': 10, 'vomiting': 11, 'burning micturition': 12, 'spotting urination': 13, 'fatigue': 14, 'weight gain': 15, 'anxiety': 16, 'cold hands and feets': 17, 'mood swings': 18, 
    'weight loss': 19, 'restlessness': 20, 'lethargy': 21,
    'patches in throat': 22, 'irregular sugar level': 23, 'cough': 24, 'high fever': 25, 'sunken eyes': 26, 'breathlessness': 27, 'sweating': 28,
    'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish skin': 32, 'dark urine': 33, 'nausea': 34, 'loss of appetite': 35, 'pain behind the eyes': 36,
    'back pain': 37, 'constipation': 38, 'abdominal pain': 39, 'diarrhoea': 40, 'mild fever': 41, 'yellow urine': 42, 'yellowing of eyes': 43, 'acute liver failure': 44,
    'fluid overload': 45, 'swelling of stomach': 46, 'swelled lymph_nodes': 47, 'malaise': 48, 'blurred and distorted vision': 49, 'phlegm': 50, 'throat irritation': 51, 
    'redness of eyes': 52, 'sinus pressure': 53, 'runny nose': 54, 'congestion': 55,
    'chest pain': 56, 'weakness in limbs': 57, 'e': 58, 'pain during bowel movements': 59, 'pain in anal region': 60, 'bloody stool': 61, 'irritation in anus': 62, 'neck pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen legs': 68,
      'swollen blood vessels': 69, 'puffy face and eyes': 70, 'enlarged thyroid': 71, 'brittle nails': 72,
      'swollen extremeties': 73, 'excessive hunger': 74, 'extra marital contacts': 75, 'drying and tingling lips': 76, 'slurred speech': 77, 'knee pain': 78, 'hip joint_pain': 79, 'muscle weakness': 80, 'stiffneck': 81, 'swellingjoints': 82, 'movement stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 
      'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108,
    'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}


# Disease list dictionary for decoding the predicted disease label
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine',
                7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 
                3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5:
                'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Initialize pyttsx3 engine (for Text-to-Speech)
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to convert speech to text using Google API
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for symptoms...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that"
        except sr.RequestError:
            return "Sorry, I could not request results"

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
    predicted_disease = model.predict([input_vector])[0]
    return diseases_list[predicted_disease]  # Return the disease name

# Function to listen for "Wake up Dobby"
def listen_for_wakeup():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Wake up Dobby'...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")
                
                # Check if the command is 'Wake up Dobby'
                if 'wake up dobby' in command:
                    print("Dobby is awake!")
                    text_to_speech("Hello, I am Dobby. How can I assist you?")
                    return  # Once it hears the wake-up command, return and continue with further actions
            except sr.UnknownValueError:
                pass  # Ignore unknown audio
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")
                break

# Main function to run the disease prediction and output results via speech and text
def main():
    # Get user input (either typed or audio)
    symptoms_input = input("Enter your symptoms (comma-separated) or type 'audio' to speak your symptoms: ").strip()

    # If user selects 'audio', we process it through speech-to-text
    if symptoms_input.lower() == "audio":
        symptoms_input = speech_to_text()

    print(f"User input: {symptoms_input}")
    
    # Process the symptoms input into a list (splitting by comma)
    user_symptoms = [s.strip() for s in symptoms_input.split(',')]

    # Get the predicted disease from the model
    predicted_disease = get_predicted_value(user_symptoms)

    # Fetch additional disease details (description, diet, medication, etc.)
    desc, pre, med, die, wrkout = helper(predicted_disease)

    # Prepare the result as a string (for both print and text-to-speech)
    result_text = f"Disease: {predicted_disease}. {desc} Diet: {', '.join(die)}. Medications: {', '.join(med)}. Precautions: {', '.join(pre)}. Workout: {', '.join(wrkout)}"

    # Print the result (in text form)
    print("\n** Disease Prediction **")
    print(f"Predicted Disease: {predicted_disease}")
    print(f"Description: {desc}")
    print(f"Precautions: {', '.join(pre)}")
    print(f"Medications: {', '.join(med)}")
    print(f"Diets: {', '.join(die)}")
    print(f"Workout: {', '.join(wrkout)}")
    print("***")

    # Convert the result to speech (read it aloud)
    text_to_speech(result_text)

# Run the program
if __name__ == "__main__":
    print("Listening for 'Wake up Dobby'...")
    listen_for_wakeup()  # First, listen for the wake-up command
    main()  # Once "Wake up Dobby" is heard, start the main program