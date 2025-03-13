import streamlit as st
import google.generativeai as genai
import requests
import random

# Configure Google Gemini AI
API_KEY = "AIzaSyDM7z8pBmnrkX8e9ycc4CRgWUmJFlgzr6o"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Nutritionix API credentials
APP_ID = "f9f1895e"
API_KEY_NUTRI = "c8cdaff4b8d656b4b7f9d0e53405f424"

# Function for BMI calculation
def calculate_bmi(weight, height):
    height_in_m = height / 100  # Convert height to meters
    bmi = weight / (height_in_m ** 2)
    return round(bmi, 2)

# Function to generate diet plan based on BMI and preferences
def generate_diet_plan(bmi, diet_preference, name, age, gender, allergies):
    if bmi < 18.5:
        return f"Hello {name}, based on your BMI, we recommend a high-calorie diet. Since you prefer a {diet_preference} diet, here are some recommendations.\n\nAllergy info: {allergies}"
    elif 18.5 <= bmi < 24.9:
        return f"Hello {name}, your BMI is in the normal range. Maintain a balanced diet with a focus on protein and fiber. Since you prefer a {diet_preference} diet, here are some recommendations.\n\nAllergy info: {allergies}"
    else:
        return f"Hello {name}, based on your BMI, we recommend a low-calorie diet. Since you prefer a {diet_preference} diet, here are some recommendations.\n\nAllergy info: {allergies}"

# Function to generate exercise and yoga routine based on BMI
def generate_exercise_yoga_routine(bmi):
    if bmi < 18.5:
        return "We recommend strength training exercises and yoga poses focused on building muscle mass."
    elif 18.5 <= bmi < 24.9:
        return "We recommend a combination of cardio, strength training, and yoga for overall fitness."
    else:
        return "We recommend light cardio exercises and yoga poses focused on flexibility and stress relief."

# Layout with tabs
tabs = st.tabs(["Home", "Diet Plan", "Nutritional Info", "BMI Calculator", "Exercise & Yoga Routine"])

# Collecting personal details once
with tabs[0]:
    st.header("Welcome to Your Health Journey!")
    st.subheader("Stay Healthy, Stay Fit!")
    
    # Collecting user data
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, step=1)
    gender = st.selectbox("Select gender:", ["Male", "Female", "Other"])
    diet_preference = st.selectbox("Diet preference:", ["Vegetarian", "Non-Vegetarian"])
    allergies = st.text_area("Any allergies or preferences?")
    
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1)
    height = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1)
    
    st.button("Submit Details")

# Use the entered data for other sections
if name and age and gender and diet_preference and weight and height:
    # Diet Plan Section
    with tabs[1]:
        st.header("Personalized Diet Plan")
        bmi = calculate_bmi(weight, height)
        diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, allergies)
        st.write(diet_plan)

    # Nutritional Info Section
    with tabs[2]:
        st.header("Food Nutritional Info")
        food_item = st.text_input("Enter a food item:")
        if st.button("Get Nutrition Info"):
            if food_item:
                # Example: Dummy data for nutritional info
                nutrition = {"calories": 200, "protein": 10, "carbohydrates": 30, "fat": 5}
                st.write(f"Calories: {nutrition['calories']} kcal")
                st.write(f"Protein: {nutrition['protein']} g")
                st.write(f"Carbs: {nutrition['carbohydrates']} g")
                st.write(f"Fat: {nutrition['fat']} g")
            else:
                st.error("Please enter a food item.")

    # BMI Calculator Section
    with tabs[3]:
        st.header("BMI Calculator")
        bmi = calculate_bmi(weight, height)
        category = "Normal" if 18.5 <= bmi < 24.9 else "Underweight" if bmi < 18.5 else "Overweight"
        st.success(f"Your BMI is {bmi} ({category})")

    # Exercise & Yoga Routine Section
    with tabs[4]:
        st.header("Personalized Exercise & Yoga Routine")
        routine = generate_exercise_yoga_routine(bmi)
        st.write(f"**Recommended Exercise & Yoga**: {routine}")
