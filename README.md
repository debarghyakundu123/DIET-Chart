Health & Nutrition Assistant

Overview

The Health & Nutrition Assistant is a Streamlit-based web application that provides personalized health recommendations, including diet plans, BMI analysis, nutritional insights, and exercise & yoga routines. The app integrates Google Gemini AI and Nutritionix API to generate AI-powered diet plans and retrieve nutritional information for various food items.

Features

Personalized Diet Plans: Generates diet plans based on BMI, diet preferences, and allergies using Google Gemini AI.

BMI Calculator: Computes BMI and categorizes the result as Underweight, Normal, Overweight, or Obese.

Nutritional Information Lookup: Fetches detailed nutritional information (calories, protein, carbs, fats) using Nutritionix API.

Exercise & Yoga Routines: Provides AI-generated workout routines and yoga recommendations based on BMI.

Session State Management: Stores user details to prevent repetitive input.

Installation

Prerequisites

Ensure you have Python 3.x installed along with the required dependencies.

Clone the Repository

git clone https://github.com/debarghyakundu123/Health-Nutrition-Assistant.git
cd Health-Nutrition-Assistant

Install Dependencies

pip install -r requirements.txt

Run the Application

streamlit run app.py

API Integration

Google Gemini AI

The application utilizes the Gemini AI API to generate diet and exercise plans. Ensure your API key is set correctly in the script:

API_KEY = "your_google_api_key"

Nutritionix API

For nutritional lookup, the Nutritionix API is used. Set your credentials in the script:

APP_ID = "your_nutritionix_app_id"
API_KEY_NUTRI = "your_nutritionix_api_key"

Usage

Start the application and click Start.

Enter your details (Name, Age, Gender, Diet Preference, Weight, Height, Allergies/Preferences).

View different sections:

Diet Plan: AI-generated meal plans based on BMI.

Nutritional Info: Check food nutritional details.

BMI Calculator: Displays BMI and its category.

Exercise & Yoga Routine: Personalized workout and yoga recommendations.

Optimization Strategies

Caching API Calls: Implemented st.cache_data to optimize responses.

Session State Management: Prevents redundant user input.

Reduced API Calls: Cached AI-generated diet plans and nutritional info to improve speed.

License

This project is open-source and available under the MIT License.

Contributors

Debarghya Kundu

Future Enhancements

Add meal tracking and calorie tracking.

Implement user authentication for personalized progress tracking.

Expand diet preferences with more options like vegan, keto, etc.

