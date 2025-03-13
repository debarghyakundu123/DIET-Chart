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

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

# Function to get BMI category
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Function to get nutritional info from Nutritionix API
def get_nutritional_info(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {"x-app-id": APP_ID, "x-app-key": API_KEY_NUTRI, "Content-Type": "application/json"}
    body = {"query": food_item, "timezone": "US/Eastern"}
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            food = data['foods'][0]
            return {
                "calories": food.get('nf_calories'),
                "protein": food.get('nf_protein'),
                "carbohydrates": food.get('nf_total_carbohydrate'),
                "fat": food.get('nf_total_fat')
            }
    return None

# Function to generate diet plan using Gemini API
def generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input=None):
    prompt = (f"Hi {name}, based on your details:\n"
              f"Age: {age}\nGender: {gender}\nBMI: {bmi}\nDiet: {diet_preference}\n"
              "Location: India\n"
              "Provide a balanced diet plan with affordable Indian foods and recipes.")
    if additional_input:
        prompt += f"Additional Preferences: {additional_input}\n"
    
    response = model.generate_content(prompt)
    return response.text

# Function to generate exercise and yoga routine based on BMI
def generate_exercise_yoga_routine(bmi, name, age, gender):
    # Generate the prompt to send to the Gemini model
    prompt = f"""
    Hi {name}, based on your details:
    Age: {age}
    Gender: {gender}
    BMI: {bmi}
    Please generate a complete daily workout routine and yoga practice suitable for a person with the given BMI. 
    The routine should include:
    - Cardiovascular exercises
    - Strength training exercises
    - Yoga poses
    - Duration for each exercise
    - Specific recommendations based on the BMI (Underweight, Normal, Overweight, Obese)
    """

    # Get the response from the Gemini model
    response = model.generate_content(prompt)
    
    return response.text

# Example function for generating workout and yoga routine based on BMI
def get_routine_for_user(name, age, gender, weight, height):
    bmi = calculate_bmi(weight, height)  # Calculate BMI
    
    # Get exercise and yoga routine from Gemini
    routine = generate_exercise_yoga_routine(bmi, name, age, gender)
    
    return routine

# Streamlit App
st.title("Health & Nutrition Assistant")
tabs = st.tabs(["Home", "Diet Plan", "Nutritional Info", "BMI Calculator"])

# Home Page with Motivational Quotes and Welcome
with tabs[0]:
    st.header("Welcome to Your Health Journey!")
    st.subheader("Stay Healthy, Stay Fit!")
    
    motivational_quotes = [
        "The only bad workout is the one that didn’t happen.",
        "Push yourself, no one else is going to do it for you.",
        "The body achieves what the mind believes."
    ]
    st.write(f"**Today's Motivation**: {random.choice(motivational_quotes)}")
    
    st.markdown("Start your journey towards a healthier you. Let's create a customized diet plan and fitness routine together.")
    st.button("Start Now")

# Diet Plan Generator
with tabs[1]:
    st.header("Personalized Diet Plan")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, step=1)
    gender = st.selectbox("Select gender:", ["Male", "Female", "Other"])
    diet_preference = st.selectbox("Diet preference:", ["Vegetarian", "Non-Vegetarian"])
    additional_input = st.text_area("Any allergies or preferences?")
    
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, key="weight_diet_plan")
    height = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1, key="height_diet_plan")
    
    if st.button("Generate Diet Plan"):
        if name and age and diet_preference and weight and height:
            bmi = calculate_bmi(weight, height)  # Calculate BMI here
            diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input)
            st.write(diet_plan)

# Nutritional Info
with tabs[2]:
    st.header("Food Nutritional Info")
    food_item = st.text_input("Enter a food item:")
    if st.button("Get Nutrition Info"):
        if food_item:
            nutrition = get_nutritional_info(food_item)
            if nutrition:
                st.write(f"Calories: {nutrition['calories']} kcal")
                st.write(f"Protein: {nutrition['protein']} g")
                st.write(f"Carbs: {nutrition['carbohydrates']} g")
                st.write(f"Fat: {nutrition['fat']} g")
            else:
                st.error("No data found!")

# BMI Calculator
with tabs[3]:
    st.header("BMI Calculator")
    weight_bmi = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, key="weight_bmi")
    height_bmi = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1, key="height_bmi")
    
    if st.button("Calculate BMI"):
        if weight_bmi and height_bmi:
            bmi = calculate_bmi(weight_bmi, height_bmi)
            category = get_bmi_category(bmi)
            st.success(f"Your BMI is {bmi} ({category})")
            
            # Generate exercise and yoga routine based on BMI
            exercise_yoga_routine = generate_exercise_yoga_routine(bmi)
            st.write(f"**Recommended Exercise & Yoga**: {exercise_yoga_routine}")
        else:
            st.error("Please enter valid weight and height.")

with tabs[4]:
    st.header("Personalized Exercise & Yoga Routine")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, step=1)
    gender = st.selectbox("Select gender:", ["Male", "Female", "Other"])
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, key="weight_routine")
    height = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1, key="height_routine")

    if st.button("Generate Exercise & Yoga Routine"):
        if name and age and weight and height:
            bmi = calculate_bmi(weight, height)  # Calculate BMI here
            # Pass the correct arguments to the function
            routine = generate_exercise_yoga_routine(bmi, name, age, gender)
            st.write(routine)
