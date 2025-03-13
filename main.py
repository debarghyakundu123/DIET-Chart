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

# Streamlit App
st.title("Health & Nutrition Assistant")

# Collect all user information at once
with st.form(key='user_info_form'):
    st.header("Enter Your Details:")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, step=1)
    gender = st.selectbox("Select gender:", ["Male", "Female", "Other"])
    diet_preference = st.selectbox("Diet preference:", ["Vegetarian", "Non-Vegetarian"])
    additional_input = st.text_area("Any allergies or preferences?")
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1)
    height = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1)
    
    submit_button = st.form_submit_button(label="Generate Health Plan")

if submit_button:
    if name and age and diet_preference and weight and height:
        # Calculate BMI and other details
        bmi = calculate_bmi(weight, height)  
        bmi_category = get_bmi_category(bmi)
        
        # Generate outputs
        diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input)
        exercise_yoga_routine = generate_exercise_yoga_routine(bmi, name, age, gender)
        
        # Display the results
        st.write(f"**Your BMI is {bmi} ({bmi_category})**")
        st.write(f"**Personalized Diet Plan:**\n{diet_plan}")
        st.write(f"**Exercise & Yoga Routine:**\n{exercise_yoga_routine}")
    else:
        st.error("Please fill in all the details to generate the health plan.")
