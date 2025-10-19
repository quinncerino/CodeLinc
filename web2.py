import streamlit as st
import boto3
import datetime
from datetime import timedelta

from bedrock_client import get_financial_advice

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('UserBenefitsContext')

st.set_page_config(layout = 'wide')

st.title("BenefitLink - Benefits Selection Assistant")

# User Identification Section
st.header("User Identification")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", value="")
with col2:
    employee_number = st.text_input("Employee Number", value="")

# Initialize session state
if 'profile_loaded' not in st.session_state:
    st.session_state.profile_loaded = False
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'loaded_profile' not in st.session_state:
    st.session_state.loaded_profile = {}

# Load Profile Logic
if st.button("Load Profile"):
    if not name or not employee_number:
        st.warning("Please enter your Name and Employee Number.")
    elif len(employee_number) < 5:
        st.error("Employee Number must be at least 5 characters.")
    else:
        try:
            response = table.get_item(Key={'employee_number': employee_number})
            if 'Item' in response:
                item = response['Item']
                if item.get('name') != name:
                    st.warning("Name doesn't match records—updating with new name.")
                last_interaction = datetime.datetime.fromisoformat(item['last_interaction'])
                if datetime.datetime.now() - last_interaction <= timedelta(days=30):
                    st.session_state.loaded_profile = item.get('profile', {})
                    st.session_state.recommendations = item.get('recommendations', None)
                    st.session_state.profile_loaded = True
                    st.success("Profile loaded successfully!")
                else:
                    st.info("Last interaction over 30 days ago—starting fresh.")
                    st.session_state.profile_loaded = True
            else:
                st.info("No prior profile found—starting new.")
                st.session_state.profile_loaded = True
        except Exception as e:
            st.error(f"Error loading profile: {e}—proceeding without persistence.")
            st.session_state.profile_loaded = True

# Only show the rest of the UI if profile is loaded
if name and employee_number and st.session_state.profile_loaded:
    # Input Section
    st.header("Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=st.session_state.loaded_profile.get('age', 30))
        income = st.number_input("Annual Income ($)", min_value=0, value=st.session_state.loaded_profile.get('income', 50000))
        family_status = st.selectbox("Family Status", ["Single", "Married", "Married with children", "Single parent"], 
                                   index=["Single", "Married", "Married with children", "Single parent"].index(st.session_state.loaded_profile.get('family_status', 'Single')))
        
    with col2:
        dependents = st.number_input("Number of dependents", min_value=0, max_value=10, value=st.session_state.loaded_profile.get('dependents', 0))
        health_concerns = st.multiselect("Health priorities", ["Preventive care", "Chronic conditions", "Mental health", "Dental", "Vision"],
                                       default=st.session_state.loaded_profile.get('health_concerns', []))
        financial_goals = st.selectbox("Primary financial goal", ["Save money", "Comprehensive coverage", "Balance cost and coverage"],
                                     index=["Save money", "Comprehensive coverage", "Balance cost and coverage"].index(st.session_state.loaded_profile.get('financial_goals', 'Save money')))

    # Benefits Selection
    st.header("Available Benefits")
    benefit_types = st.multiselect("Select benefit types to analyze", 
        ["Health Insurance", "Dental", "Vision", "Employee Assistance Program", "Caregiver Resources", "Tutoring Support"])

    # Generate Recommendations
    if st.button("Get Personalized Recommendations"):
        if benefit_types:
            user_profile = f"Age: {age}, Income: ${income}, Family: {family_status}, Dependents: {dependents}, Health priorities: {health_concerns}, Goal: {financial_goals}"
            question = f"Recommend optimal benefits for: {user_profile}. Focus on: {', '.join(benefit_types)}"
            
            with st.spinner("Analyzing your profile..."):
                st.session_state.recommendations = get_financial_advice(question)
                
                # Save to DynamoDB
                profile_data = {
                    'age': age, 'income': income, 'family_status': family_status, 
                    'dependents': dependents, 'health_concerns': health_concerns, 
                    'financial_goals': financial_goals
                }
                item = {
                    'employee_number': employee_number,
                    'name': name,
                    'last_interaction': datetime.datetime.now().isoformat(),
                    'profile': profile_data,
                    'recommendations': st.session_state.recommendations
                }
                try:
                    table.put_item(Item=item)
                except Exception as e:
                    st.error(f"Error saving profile: {e}")
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
                    
                    # Update DynamoDB with latest interaction
                    profile_data = {
                        'age': age, 'income': income, 'family_status': family_status,
                        'dependents': dependents, 'health_concerns': health_concerns,
                        'financial_goals': financial_goals
                    }
                    item = {
                        'employee_number': employee_number,
                        'name': name,
                        'last_interaction': datetime.datetime.now().isoformat(),
                        'profile': profile_data,
                        'recommendations': st.session_state.recommendations
                    }
                    try:
                        table.put_item(Item=item)
                    except Exception as e:
                        st.error(f"Error saving profile: {e}")
                        
                st.subheader("Answer")
                st.write(answer)
            else:
                st.warning("Please enter a question.")
else:
    st.info("Enter your details above and click 'Load Profile' to continue.")