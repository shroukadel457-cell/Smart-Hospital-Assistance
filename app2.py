import sqlite3
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt


#create data base and connect 
connection = sqlite3.connect("medical_system.db")
#setting cursor 
cursor = connection.cursor()
#create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    temperature REAL NOT NULL,
    symptoms TEXT NOT NULL,
    symptom_duration INTEGER NOT NULL,
    chronic_diseases TEXT,
    priority TEXT,
    specialty TEXT,
    doctor TEXT,
    queue_number INTEGER,
    status TEXT DEFAULT 'waiting'
)
""")
#save (commit)
connection.commit()


class Patient:
    def __init__(self, name, age, temperature, symptoms, symptom_duration, chronic_diseases):
        self.name = name
        self.age = age
        self.temperature = temperature
        self.symptoms = symptoms.lower()
        self.symptom_duration = symptom_duration
        self.chronic_diseases = chronic_diseases.lower()


doctors = {
    "Neurology": ["Dr. Ahmed", "Dr. Mona"],
    "Cardiology": ["Dr. Ali", "Dr. Youssef"],
    "Gastroenterology": ["Dr. Amr", "Dr. Sara"],
    "Pulmonology": ["Dr. Mohamed", "Dr. Nour"],
    "Orthopedics": ["Dr. Osama", "Dr. Karim"],
    "Psychiatry": ["Dr. Malak", "Dr. Lina"],
    "ENT": ["Dr. Salma", "Dr. Hany"],
    "General Medicine": ["Dr. Shorouk", "Dr. Menna"]}

doctor_queues = {
    "Dr. Ahmed": ["Patient1", "Patient2"], "Dr. Mona": ["Patient3"],
    "Dr. Ali": ["Patient4", "Patient5", "Patient6"], "Dr. Youssef": ["Patient7"],
    "Dr. Amr": ["Patient8", "Patient9"], "Dr. Sara": ["Patient10"],
    "Dr. Mohamed": ["Patient11", "Patient12", "Patient13"], "Dr. Nour": ["Patient14"],
    "Dr. Osama": ["Patient15"], "Dr. Karim": ["Patient16", "Patient17"],
    "Dr. Malak": ["Patient18", "Patient19"], "Dr. Lina": ["Patient20"],
    "Dr. Salma": ["Patient21", "Patient22"], "Dr. Hany": ["Patient23"],
    "Dr. Shorouk": ["Patient24", "Patient25"], "Dr. Menna": ["Patient26"]}

# ==========================================
#input 
def audio_symptoms():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print(" Listening... please speak in English")
            recognizer.adjust_for_ambient_noise(source, duration=1)  
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            symptoms = recognizer.recognize_google(audio, language="en-US")
            return symptoms      
    except sr.WaitTimeoutError:
        print(" No speech detected (Timeout).")
    except Exception as e:
        print(f" Error: {e}") 
    return input("Enter your symptoms manually: ").lower()

while True:
    print("\n" + "="*30)
    print("--- Enter New Patient Details ---")
    name = input('Name: ')
    age = int(input('Age: '))
    temperature = float(input('Temperature: '))
    
    print("How would you like to enter your symptoms?")
    print("1. Speak via Microphone ")
    print("2.Type manually")

    while True:
        input_choice = input("Choose option (1 or 2): ")
        if input_choice == '1':
            symptoms = audio_symptoms()
            break
        elif input_choice == '2':
            symptoms = input("Enter your symptoms manually: ").lower()
            break
        else:
            print("Please choose a valid option (1 or 2).")

    print(f"symptoms: {symptoms}")

    symptom_duration = int(input('Symptom duration (days): '))
    chronic_diseases = input('Chronic diseases (type "none" if no): ').lower()

    patient = Patient(name, age, temperature, symptoms, symptom_duration, chronic_diseases)

 #################################
 
    priority_score = 0
    if patient.chronic_diseases not in ["no", "none", ""]: priority_score += 1
    if patient.age < 4 or patient.age >= 60: priority_score += 2
    if patient.temperature >= 38: priority_score += 3
    if patient.symptom_duration >= 4: priority_score += 1

    if 'chest pain' in patient.symptoms: priority_score += 3
    if 'difficulty breathing' in patient.symptoms: priority_score += 4
    if 'dizziness' in patient.symptoms: priority_score += 3
    if 'stomach pain' in patient.symptoms: priority_score += 3
    if 'headache' in patient.symptoms: priority_score += 2

    if priority_score >= 7: priority = 'HIGH'
    elif priority_score >= 4: priority = 'MEDIUM'
    else: priority = 'LOW'


    scores = {
        "Neurology": 0, "Cardiology": 0, "Gastroenterology": 0,
        "Pulmonology": 0, "Orthopedics": 0, "Psychiatry": 0,
        "ENT": 0, "General Medicine": 0
    }
    if "headache" in patient.symptoms: scores["Neurology"] += 2
    if "dizziness" in patient.symptoms: scores["Neurology"] += 3
    if "chest pain" in patient.symptoms: scores["Cardiology"] += 3
    if "stomach pain" in patient.symptoms: scores["Gastroenterology"] += 3
    if "nausea" in patient.symptoms: scores["Gastroenterology"] += 2
    if "cough" in patient.symptoms: scores["Pulmonology"] += 2
    if "difficulty breathing" in patient.symptoms: scores["Pulmonology"] += 4
    if "joint pain" in patient.symptoms: scores["Orthopedics"] += 3
    if "anxiety" in patient.symptoms: scores["Psychiatry"] += 3
    if "depression" in patient.symptoms: scores["Psychiatry"] += 3
    if "earache" in patient.symptoms: scores["ENT"] += 3

    if max(scores.values()) == 0:
        specialty = "General Medicine"
    else:
        specialty = max(scores, key=scores.get)

    specialty_doctors = doctors[specialty]


    print(f"\n--- Available Doctors for {specialty} ---")
    for i, doc_name in enumerate(specialty_doctors, start=1):
        waiting = len(doctor_queues[doc_name])
        print(f"{i}. {doc_name} ({waiting} patients waiting)")

    print("\n1. Choose a doctor manually")
    print("2. Auto-assign doctor with the shortest queue")

    while True:
        try:
            option = int(input("Option (1/2): "))
            if option in [1,2]: break
            print("Invalid option.")
        except ValueError:
            print("Please enter a number.")

    if option == 1:
        while True:
            try:
                choice = int(input("Enter doctor number: "))
                if 1 <= choice <= len(specialty_doctors): break
                print("Invalid doctor number.")
            except ValueError:
                print("Please enter a number.")
        selected_doctor = specialty_doctors[choice - 1]
    else:
        selected_doctor = min(specialty_doctors, key=lambda d: len(doctor_queues[d]))


    waiting_before_me = len(doctor_queues[selected_doctor])

    doctor_queues[selected_doctor].append(patient.name)

    my_queue_position = len(doctor_queues[selected_doctor])

    cursor.execute("""
    INSERT INTO patients
    (name, age, temperature, symptoms, symptom_duration, chronic_diseases, priority, specialty, doctor, queue_number, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient.name, patient.age, patient.temperature, patient.symptoms,
        patient.symptom_duration, patient.chronic_diseases, priority,
        specialty, selected_doctor, my_queue_position, "waiting"
    ))
    connection.commit()


    print("\n--- Appointment Confirmed ---")
    print(f"Name: {patient.name}")
    print(f"Priority: {priority}")
    print(f"Specialty: {specialty}")
    print(f"Assigned Doctor: {selected_doctor}")
    print(f"Your Queue Number: {my_queue_position}")
    print(f"Patients ahead of you: {waiting_before_me}")
    print("-----------------------------")


    add_another = input("\nDo you want to add another patient? (y/n): ")
    if add_another.lower() != 'y':
        print("System closed. Data saved successfully.")
        break

# statisticsss
def show_statistics():
    conn = sqlite3.connect("medical_system.db")
    df = pd.read_sql_query("SELECT specialty, priority FROM patients", conn)
    conn.close()
  
    specialty_counts = df["specialty"].value_counts()
    priority_counts = df["priority"].value_counts()

    plt.figure(figsize=(10, 4))
  #bar chart
    plt.subplot(1, 2, 1)
    plt.bar(specialty_counts.index, specialty_counts.values)
    plt.title("Patients per Speciality")
    plt.xticks(rotation=30, ha="right")
  #pie chart
    plt.subplot(1, 2, 2)
    plt.pie(priority_counts.values, labels=priority_counts.index)
    plt.title("Priority Distribution")
    plt.show()

show_statistics()