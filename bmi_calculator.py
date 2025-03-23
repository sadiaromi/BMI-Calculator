import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
        padding-bottom: 20px;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 30px;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .info-text {
        color: #7f8c8d;
        font-size: 14px;
    }
    .category-underweight { color: #3498db; font-weight: bold; }
    .category-normal { color: #2ecc71; font-weight: bold; }
    .category-overweight { color: #f39c12; font-weight: bold; }
    .category-obese { color: #e74c3c; font-weight: bold; }
    
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("BMI Calculator")
st.markdown("BMI analysis tool for health assessment")
st.markdown('</div>', unsafe_allow_html=True)

# Create a single column layout
col1 = st.container()

with col1:
    st.markdown("### Personal Information")
    
    # Add name
    name = st.text_input("Name (Optional)", placeholder="Enter your name")
    
    # Gender selection
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    
    # Age with slider
    age = st.slider("Age", min_value=2, max_value=120, value=30)
    
    st.markdown("### Body Measurements")
    
    # Weight
    weight = st.number_input(
        "Weight",
        min_value=1.0,
        max_value=500.0,
        value=70.0,
        step=0.1,
        format="%.1f"
    )
    weight_unit = st.selectbox("Weight unit", ["kg", "lbs"])
    
    # Height
    height = st.number_input(
        "Height",
        min_value=1.0,
        max_value=300.0,
        value=170.0,
        step=0.1,
        format="%.1f"
    )
    height_unit = st.selectbox("Height unit", ["cm", "m", "ft"])


# Calculate button
calculate_button = st.button("Calculate BMI", use_container_width=True)

# Process calculation when button is pressed
if calculate_button:
    # Convert weight to kg if in lbs
    weight_kg = weight * 0.453592 if weight_unit == "lbs" else weight
    
    # Convert height to meters
    if height_unit == "cm":
        height_m = height / 100
    elif height_unit == "ft":
        height_m = height * 0.3048
    else:
        height_m = height
    
    # Calculate BMI
    bmi = weight_kg / (height_m ** 2)
    
    # Determine BMI category and color
    if bmi < 18.5:
        category = "Underweight"
        category_class = "category-underweight"
        progress_color = "#3498db"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
        category_class = "category-normal"
        progress_color = "#2ecc71"
    elif 25 <= bmi < 30:
        category = "Overweight"
        category_class = "category-overweight"
        progress_color = "#f39c12"
    else:
        category = "Obese"
        category_class = "category-obese"
        progress_color = "#e74c3c"
    
    # Display results
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Personalized greeting if name is provided
    if name:
        st.markdown(f"## Hello, {name}!")
    else:
        st.markdown("## Your Results")
    
    
    
    # Display BMI
    st.markdown(f"### BMI: **{bmi:.1f}**")
    
    # Create a custom progress bar for BMI visualization
    bmi_min, bmi_max = 10, 40
    normalized_bmi = min(max((bmi - bmi_min) / (bmi_max - bmi_min), 0), 1)
    
    st.progress(normalized_bmi, text=f"BMI: {bmi:.1f}")
    
    # Display category
    st.markdown(f"### Category: <span class='{category_class}'>{category}</span>", unsafe_allow_html=True)
    
    # Create a more visualization
    bmi_range = pd.DataFrame({
        'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
        'Start': [10, 18.5, 25, 30],
        'End': [18.5, 25, 30, 40],
        'Color': ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    })
    
    # Create a bar chart for BMI categories
    bars = alt.Chart(bmi_range).mark_bar().encode(
        x='Start',
        x2='End',
        y=alt.value(20),  # Fixed height
        color=alt.Color('Category:N', scale=alt.Scale(
            domain=['Underweight', 'Normal', 'Overweight', 'Obese'],
            range=['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
        ))
    )
    
    # Add a marker for the user's BMI
    marker = alt.Chart(pd.DataFrame({'BMI': [bmi]})).mark_rule(
        color='black',
        strokeWidth=2
    ).encode(x='BMI:Q')
    
    # Combine the charts
    chart = (bars + marker).properties(
        width=600,
        height=50,
        title='Your BMI on the Scale'
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Personalized health insights based on BMI category
    st.markdown("### Health Insights")
    
    if category == "Underweight":
        st.markdown("""
        - Your BMI indicates you may be underweight
        - Consider consulting with a healthcare provider
        - Focus on nutrient-dense foods to gain healthy weight
        - Regular strength training can help build muscle mass
        """)
    elif category == "Normal weight":
        st.markdown("""
        - Your BMI falls within the healthy weight range
        - Maintain your current healthy habits
        - Regular physical activity and balanced nutrition are key
        - Continue with preventive health check-ups
        """)
    elif category == "Overweight":
        st.markdown("""
        - Your BMI indicates you may be overweight
        - Consider moderate weight loss through healthy eating
        - Aim for 150+ minutes of moderate exercise weekly
        - Regular health monitoring is recommended
        """)
    else:  # Obese
        st.markdown("""
        - Your BMI indicates obesity, which may increase health risks
        - Consult with healthcare providers for personalized advice
        - Consider a structured approach to weight management
        - Regular monitoring of health metrics is important
        """)
    
    # Additional health metrics 
    st.markdown("### Additional Health Metrics")
    
    # Calculate ideal weight range
    ideal_weight_min = 18.5 * (height_m ** 2)
    ideal_weight_max = 24.9 * (height_m ** 2)
    
    if weight_unit == "lbs":
        ideal_weight_min = ideal_weight_min * 2.20462
        ideal_weight_max = ideal_weight_max * 2.20462
        weight_unit_display = "lbs"
    else:
        weight_unit_display = "kg"
    
    st.markdown(f"**Ideal Weight Range:** {ideal_weight_min:.1f} - {ideal_weight_max:.1f} {weight_unit_display}")
    
    # Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * (height_m * 100) - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * (height_m * 100) - 5 * age - 161
    
    st.markdown(f"**Estimated BMR:** {bmr:.0f} calories/day")
    st.markdown("<div class='info-text'>BMR is the number of calories your body needs at rest</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

