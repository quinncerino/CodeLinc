import streamlit as st
import boto3

from bedrock_client import get_financial_advice

st.set_page_config(layout = 'wide')

st.title("BenefitLink - Benefits Selection Assistant")

# Input Section
st.header("Personal Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    income = st.number_input("Annual Income ($)", min_value=0, value=50000)
    family_status = st.selectbox("Family Status", ["Single", "Married", "Married with children", "Single parent"])
    
with col2:
    dependents = st.number_input("Number of dependents", min_value=0, max_value=10, value=0)
    health_concerns = st.multiselect("Health priorities", ["Preventive care", "Chronic conditions", "Mental health", "Dental", "Vision"])
    financial_goals = st.selectbox("Primary financial goal", ["Save money", "Comprehensive coverage", "Balance cost and coverage"])

# Benefits Selection
st.header("Available Benefits")
benefit_types = st.multiselect("Select benefit types to analyze", 
    ["Health Insurance", "Dental", "Vision", "Employee Assistance Program", "Caregiver Resources", "Tutoring Support"])

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

# Generate Recommendations
if st.button("Get Personalized Recommendations"):
    if benefit_types:
        user_profile = f"Age: {age}, Income: ${income}, Family: {family_status}, Dependents: {dependents}, Health priorities: {health_concerns}, Goal: {financial_goals}"
        question = f"Recommend optimal benefits for: {user_profile}. Focus on: {', '.join(benefit_types)}"
        
        with st.spinner("Analyzing your profile..."):
            st.session_state.recommendations = get_financial_advice(question)
    else:
        st.warning("Please select at least one benefit type.")

# Display recommendations if they exist
if st.session_state.recommendations:
    st.header("Your Personalized Recommendations")
    st.write(st.session_state.recommendations)
    
    # Q&A Section
    st.header("Ask Follow-up Questions")
    user_question = st.text_area("Have questions about your benefits? Ask here:")
    
    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Searching knowledge base..."):
                answer = get_financial_advice(user_question)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.warning("Please enter a question.")