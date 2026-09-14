# BMI Calculator

## Project Overview

The BMI Calculator is a Python-based GUI application developed using Tkinter. It calculates a user's Body Mass Index (BMI), classifies the result, stores BMI history using SQLite, and displays BMI trends using Matplotlib.

## Features

- User-friendly graphical interface using Tkinter
- Accepts user name, weight, and height
- Calculates BMI automatically
- Displays BMI rounded to 2 decimal places
- BMI classification:
  - Underweight: BMI < 18.5
  - Normal: BMI 18.5 – 24.9
  - Overweight: BMI 25 – 29.9
  - Obese: BMI ≥ 30
- Validates invalid and negative inputs
- Stores BMI records in an SQLite database
- Supports multiple users
- Displays previous BMI records
- Displays BMI trend using a line chart
- Handles database errors using exception handling

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## Project Structure

```text
Beginner-BMI-BMI-Calculator/
│
├── bmi_calculator.py
├── bmi_history.db
└── README.md