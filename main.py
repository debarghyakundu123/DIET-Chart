import streamlit as st
import google.generativeai as genai
import requests

# Configure Google Gemini AI
API_KEY = "AIzaSyDM7z8pBmnrkX8e9ycc4CRgWUmJFlgzr6o"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Nutritionix API credentials
APP_ID = "f9f1895e"
API_KEY_NUTRI = "c8cdaff4b8d656b4b7f9d0e53405f424"

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

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

def generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input=None):
    prompt = (f"Hi {name}, based on your details:\n"
              f"Age: {age}\nGender: {gender}\nBMI: {bmi}\nDiet: {diet_preference}\n"
              "Location: India\n"
              "Provide a balanced diet plan with affordable Indian foods and recipes.")
    if additional_input:
        prompt += f"Additional Preferences: {additional_input}\n"
    
    response = model.generate_content(prompt)
    return response.text

# Streamlit App
st.title("Health & Nutrition Assistant")
tabs = st.tabs(["Diet Plan ", "Nutritional Info", "BMI Calculator"])

# Diet Plan Generator
with tabs[0]:
    st.header("Personalized Diet Plan")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, step=1)
    gender = st.selectbox("Select gender:", ["Male", "Female", "Other"])
    diet_preference = st.selectbox("Diet preference:", ["Vegetarian", "Non-Vegetarian"])
    additional_input = st.text_area("Any allergies or preferences?")
    
    # Get weight and height inputs in this section for BMI calculation
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, key="weight_diet_plan")
    height = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1, key="height_diet_plan")
    
    if st.button("Generate Diet Plan"):
        if name and age and diet_preference and weight and height:
            bmi = calculate_bmi(weight, height)  # Calculate BMI here
            diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input)
            st.write(diet_plan)

# Nutritional Info
with tabs[1]:
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
with tabs[2]:
    st.header("BMI Calculator")
    weight_bmi = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1, key="weight_bmi")
    height_bmi = st.number_input("Enter your height (cm):", min_value=50.0, step=0.1, key="height_bmi")
    
    if st.button("Calculate BMI"):
        if weight_bmi and height_bmi:
            bmi = calculate_bmi(weight_bmi, height_bmi)
            category = get_bmi_category(bmi)
            st.success(f"Your BMI is {bmi} ({category})")
        else:
            st.error("Please enter valid weight and height.")
