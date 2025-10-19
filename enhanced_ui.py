import streamlit as st
import boto3
import datetime
from datetime import timedelta
from bedrock_client import get_financial_advice

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('UserBenefitsContext')

# Page configuration
st.set_page_config(
    page_title="BeneLinc - Benefits Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b35 0%, #8b1a1a 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .section-header {
        background: #fff5f0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b35;
        margin: 1rem 0;
    }
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(255,107,53,0.1);
        margin: 1rem 0;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #ff6b35 0%, #8b1a1a 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ff6b35 0%, #8b1a1a 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255,107,53,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>💼 BeneLinc</h1>
    <h3>Your Intelligent Benefits Selection Assistant</h3>
    <p>Get personalized recommendations tailored to your unique needs</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for quick actions
with st.sidebar:
    st.markdown("### 🚀 Quick Actions")
    if st.button("🔄 Reset Form"):
        st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
    
    st.markdown("### 💡 Tips")
    st.info("💰 Consider your budget and family needs when selecting benefits")
    st.info("🏥 Prioritize health coverage based on your medical history")
    st.info("📊 Review all options before making final decisions")

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'custom_answer' not in st.session_state:
    st.session_state.custom_answer = None
if 'comparison' not in st.session_state:
    st.session_state.comparison = None
if 'profile_loaded' not in st.session_state:
    st.session_state.profile_loaded = False
if 'loaded_profile' not in st.session_state:
    st.session_state.loaded_profile = {}
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'employee_number' not in st.session_state:
    st.session_state.employee_number = ''

# User Identification Section
st.markdown('<div class="section-header"><h2>👤 User Identification</h2></div>', unsafe_allow_html=True)
col_id1, col_id2, col_id3 = st.columns([1, 1, 1])
with col_id1:
    name = st.text_input("Name", value=st.session_state.name)
with col_id2:
    employee_number = st.text_input("Employee Number", value=st.session_state.employee_number)
with col_id3:
    if st.button("Load Profile", use_container_width=True):
        if not name or not employee_number:
            st.warning("Please enter your Name and Employee Number.")
        elif len(employee_number) < 5:
            st.error("Employee Number must be at least 5 characters.")
        else:
            try:
                # Check if table exists first
                table.load()
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
                        st.session_state.name = name
                        st.session_state.employee_number = employee_number
                        st.success("Profile loaded successfully!")
                    else:
                        st.info("Last interaction over 30 days ago—starting fresh.")
                        st.session_state.profile_loaded = True
                        st.session_state.name = name
                        st.session_state.employee_number = employee_number
                else:
                    st.info("No prior profile found—starting new.")
                    st.session_state.profile_loaded = True
                    st.session_state.name = name
                    st.session_state.employee_number = employee_number
            except Exception as e:
                if "ResourceNotFoundException" in str(e):
                    st.warning("DynamoDB table not found. Creating table...")
                    try:
                        # Create table if it doesn't exist
                        import subprocess
                        subprocess.run(["python3", "create_dynamodb_table.py"], check=True)
                        st.success("Table created! Please try loading your profile again.")
                    except Exception as create_error:
                        st.error(f"Error creating table: {create_error}")
                else:
                    st.error(f"Error loading profile: {e}")
                st.session_state.profile_loaded = True
                st.session_state.name = name
                st.session_state.employee_number = employee_number

if not st.session_state.profile_loaded:
    st.info("Enter your details above and click 'Load Profile' to continue.")
    st.stop()

# Main content area
col_left, col_right = st.columns([2, 1])

with col_left:
    # Personal Information Section
    st.markdown('<div class="section-header"><h2>👤 Personal Information</h2></div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("🎂 Age", min_value=18, max_value=100, value=int(st.session_state.loaded_profile.get('age', 30)), help="Your current age")
            income = st.number_input("💵 Annual Income ($)", min_value=0, value=int(st.session_state.loaded_profile.get('income', 50000)), step=5000, help="Your gross annual income")
            family_status = st.selectbox("👨👩👧👦 Family Status", 
                ["Single", "Married", "Married with children", "Single parent"],
                index=["Single", "Married", "Married with children", "Single parent"].index(st.session_state.loaded_profile.get('family_status', 'Single')),
                help="Your current family situation")
        
        with col2:
            dependents = st.number_input("👶 Number of Dependents", min_value=0, max_value=10, value=int(st.session_state.loaded_profile.get('dependents', 0)), help="People who depend on your income")
            health_concerns = st.multiselect("🏥 Health Priorities", 
                ["Preventive care", "Chronic conditions", "Mental health", "Dental", "Vision"],
                default=st.session_state.loaded_profile.get('health_concerns', []),
                help="Select your main health focus areas")
            financial_goals = st.selectbox("🎯 Primary Financial Goal", 
                ["Save money", "Comprehensive coverage", "Balance cost and coverage"],
                index=["Save money", "Comprehensive coverage", "Balance cost and coverage"].index(st.session_state.loaded_profile.get('financial_goals', 'Save money')),
                help="What's most important to you?")

    # Benefits Selection Section
    st.markdown('<div class="section-header"><h2>📋 Available Benefits</h2></div>', unsafe_allow_html=True)
    
    benefit_types = st.multiselect("Select benefit types to analyze:", 
        ["Health Insurance", "Dental", "Vision", "Employee Assistance Program", "Caregiver Resources", "Tutoring Support"],
        help="Choose the benefits you want recommendations for")

    # Custom prompt section
    st.markdown('<div class="section-header"><h2>💬 Custom Questions</h2></div>', unsafe_allow_html=True)
    custom_prompt = st.text_area("Ask a specific question about benefits:", 
        placeholder="e.g., What's the difference between HMO and PPO plans?",
        help="Enter any specific questions about benefits or coverage")

with col_right:
    # Profile Summary
    st.markdown('<div class="section-header"><h2>📊 Your Profile</h2></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div class="info-card">
            <h4>Profile Summary</h4>
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Income:</strong> ${income:,}</p>
            <p><strong>Family:</strong> {family_status}</p>
            <p><strong>Dependents:</strong> {dependents}</p>
            <p><strong>Goal:</strong> {financial_goals}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress indicator
    progress_items = [age > 0, income > 0, bool(family_status), bool(benefit_types)]
    progress = sum(progress_items) / len(progress_items)
    
    st.markdown("### ✅ Completion Status")
    st.progress(progress)
    st.write(f"Profile: {int(progress * 100)}% complete")

# Action buttons
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    get_recommendations = st.button("🎯 Get Personalized Recommendations", use_container_width=True)

with col_btn2:
    ask_question = st.button("❓ Ask Custom Question", use_container_width=True)

with col_btn3:
    compare_benefits = st.button("⚖️ Compare Benefits", use_container_width=True)

# Results Section
if get_recommendations:
    if benefit_types:
        user_profile = f"Age: {age}, Income: ${income}, Family: {family_status}, Dependents: {dependents}, Health priorities: {health_concerns}, Goal: {financial_goals}"
        question = f"Recommend optimal benefits for: {user_profile}. Focus on: {', '.join(benefit_types)}"
        
        with st.spinner("🔍 Analyzing your profile and generating recommendations..."):
            st.session_state.recommendations = get_financial_advice(question)
            
            # Save to DynamoDB
            profile_data = {
                'age': age, 'income': income, 'family_status': family_status,
                'dependents': dependents, 'health_concerns': health_concerns,
                'financial_goals': financial_goals
            }
            item = {
                'employee_number': st.session_state.employee_number,
                'name': st.session_state.name,
                'last_interaction': datetime.datetime.now().isoformat(),
                'profile': profile_data,
                'recommendations': st.session_state.recommendations
            }
            try:
                table.put_item(Item=item)
            except Exception as e:
                st.error(f"Error saving profile: {e}")
    else:
        st.warning("⚠️ Please select at least one benefit type to get recommendations.")

if ask_question and custom_prompt:
    with st.spinner("🤔 Finding the best answer for you..."):
        st.session_state.custom_answer = get_financial_advice(custom_prompt)
        
        # Update DynamoDB
        profile_data = {
            'age': age, 'income': income, 'family_status': family_status,
            'dependents': dependents, 'health_concerns': health_concerns,
            'financial_goals': financial_goals
        }
        item = {
            'employee_number': st.session_state.employee_number,
            'name': st.session_state.name,
            'last_interaction': datetime.datetime.now().isoformat(),
            'profile': profile_data,
            'recommendations': st.session_state.recommendations
        }
        try:
            table.put_item(Item=item)
        except Exception as e:
            st.error(f"Error saving: {e}")

if compare_benefits:
    if len(benefit_types) >= 2:
        comparison_question = f"Compare and contrast these benefits for someone with profile: Age {age}, Income ${income}, Family status: {family_status}. Benefits to compare: {', '.join(benefit_types)}"
        
        with st.spinner("⚖️ Comparing your selected benefits..."):
            st.session_state.comparison = get_financial_advice(comparison_question)
    else:
        st.warning("⚠️ Please select at least 2 benefit types to compare.")

# Display results from session state
if st.session_state.recommendations:
    st.markdown("""
    <div class="recommendation-box">
        <h2>🎯 Your Personalized Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(st.session_state.recommendations)
    
    if st.button("💾 Save Recommendations"):
        profile_data = {
            'age': age, 'income': income, 'family_status': family_status,
            'dependents': dependents, 'health_concerns': health_concerns,
            'financial_goals': financial_goals
        }
        item = {
            'employee_number': st.session_state.employee_number,
            'name': st.session_state.name,
            'last_interaction': datetime.datetime.now().isoformat(),
            'profile': profile_data,
            'recommendations': st.session_state.recommendations
        }
        try:
            table.put_item(Item=item)
            st.success("✅ Recommendations saved to your profile!")
        except Exception as e:
            st.error(f"Error saving: {e}")

if st.session_state.custom_answer:
    st.markdown('<div class="section-header"><h2>💡 Answer</h2></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <h4>Your Question:</h4>
        <p><em>"{custom_prompt}"</em></p>
        <h4>Answer:</h4>
        <p>{st.session_state.custom_answer}</p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.comparison:
    st.markdown('<div class="section-header"><h2>⚖️ Benefits Comparison</h2></div>', unsafe_allow_html=True)
    st.markdown(st.session_state.comparison)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💼 BenefitLink - Making benefits selection simple and personalized</p>
    <p>Need help? Contact our support team or check our FAQ section.</p>
</div>
""", unsafe_allow_html=True)