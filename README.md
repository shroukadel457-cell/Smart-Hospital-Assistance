# 🏥 Medical Patient Management System

A simple Python project for managing patients, assigning doctors, and organizing queues.

## Features

* Add patient information
* Enter symptoms manually or by voice 🎤
* Calculate patient priority: **HIGH, MEDIUM, LOW**
* Suggest a medical specialty
* Assign a doctor
* Generate queue numbers
* Save patient data using SQLite
* Display statistics using charts 📊

## Libraries Used

* **SQLite3** – Database management
* **SpeechRecognition** – Voice recognition
* **PyAudio** – Microphone/audio input
* **Pandas** – Data analysis
* **Matplotlib** – Charts and visualization

## Installation

Install all required libraries:

```bash
pip install pandas matplotlib SpeechRecognition PyAudio
```

> `sqlite3` is included with Python, so it does not need to be installed separately.

## Run the Project

```bash
python medical_system.py
```

The database `medical_system.db` will be created automatically.

## Specialties

* Neurology
* Cardiology
* Gastroenterology
* Pulmonology
* Orthopedics
* Psychiatry
* ENT
* General Medicine

## Disclaimer

This project is for **educational purposes only**. The priority and specialty rules are simple programming rules and are not a medical diagnosis or professional medical advice.


