import streamlit as st
from openai import OpenAI

# 1. Page Layout & Setup
st.set_page_config(page_title="FitTrack AI", page_icon="🏋️‍♂️", layout="centered")
st.title("🏋️‍♂️ FitTrack: Specialized Fitness & Nutrition AI")
st.markdown("*Your hyper-focused domain assistant for Food Logging, Calorie Deficit Tracking, and Workout Design.*")

# 2. Sidebar Secure Key Input
api_key_input = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

if not api_key_input:
    st.info("Please enter your OpenAI API key in the sidebar to begin.", icon="🔑")
    st.stop()

# 3. Initialize OpenAI Client Connection
client = OpenAI(api_key=api_key_input)

# 4. Initialize Memory & Strict Domain System Prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": (
                "Identity & Domain Restriction:\n"
                "You are 'FitTrack AI,' a deeply specialized, domain-specific AI Fitness and Nutrition Coach. "
                "You are strictly restricted to answering questions regarding fitness, exercise, food logging, "
                "macronutrients, TDEE calculation, weight loss, muscle gain, and workout planning.\n\n"
                "STRICT OUT-OF-DOMAIN RULE: If the user asks about ANY topic outside of fitness and nutrition "
                "(e.g., medical diagnoses, mental health, coding, cars, pop culture, history, general technology), "
                "you must absolutely refuse to answer. Use this exact refusal statement:\n"
                "'I am a dedicated Fitness & Nutrition AI Assistant. I am strictly restricted to answering questions regarding workouts, diet, and fitness tracking, so I cannot assist with that topic. Please let me know how I can help you reach your physical fitness goals.'\n\n"
                "Core Feature Requirements:\n"
                "1. Food Logging: Analyze natural meal descriptions (e.g., 'aloo paratha with yogurt'). Instantly calculate and return an estimated breakdown of Calories, Protein, Carbs, and Fats.\n"
                "2. Calorie Deficit Tracking: Calculate user TDEE when provided age, weight, height, and activity level. Establish a daily target for fat loss/muscle gain, tracking eaten vs burned metrics with daily summaries (calories remaining, protein targets).\n"
                "3. Workout Suggestions: Generate specific, structured workout routines when given constraints like time, equipment available, and training goal. Include exercise names, sets, reps, rest times, and estimated total calories burned.\n\n"
                "Tone & Motivation:\n"
                "Maintain a highly motivating, energetic, coaching-focused, and supportive tone. Actively encourage progress updates and suggest macro-friendly meals if the user indicates they have remaining calorie budgets left."
            )
        }
    ]

# Display conversation history (hiding the background system setup)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. Capture User Input
if user_input := st.chat_input("Log a meal, calculate your TDEE, or ask for a workout plan..."):
    # Display user chat bubble
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Save to session history array
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. Generate Response using the conversation context transcript
    with st.chat_message("assistant"):
        try:
            # Map historical array list to context string pattern
            chat_context = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
            
            response = client.responses.create(
                model="gpt-5.4-mini",
                input=chat_context + "\nAssistant:",
                store=True,
            )
            
            ai_response = response.output_text
            st.markdown(ai_response)
            
            # Save generated response to session history array
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"An error occurred while communicating with the model: {e}")
