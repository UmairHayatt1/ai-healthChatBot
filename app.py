import streamlit as st
from openai import OpenAI

# 1. Page Layout Configuration
st.set_page_config(page_title="AI Health Assistant", page_icon="🩺")
st.title("🩺 AI Health ChatBot")
st.markdown("<h3 style='text-align: center;'><b>Solving healthcare delays through instant symptom triage and health education.</b></h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'><b>BY UMAIR HAYAT</b></h3>", unsafe_allow_html=True)

# 2. Sidebar for Secure API Key Entry
api_key_input = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

if not api_key_input:
    st.info("Please enter your OpenAI API key in the sidebar to begin.", icon="🔑")
    st.stop()

# 3. Initialize the OpenAI Client
client = OpenAI(api_key=api_key_input)

# 4. Mandatory Medical Disclaimer Box (Shows high professionalism for your project)
st.warning(
    "⚠️ **Disclaimer:** This chatbot is an AI-powered educational tool for symptom triage. "
    "It does not provide official medical diagnoses or treatments. If you are experiencing a life-threatening emergency, "
    "please call your local emergency services immediately."
)

# 5. Initialize Chat History with a Medical Persona
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": (
                "You are an empathetic, professional AI Medical Triage Assistant named MediTriage.\n"
                "Your goal is to ask clarifying questions about a patient's symptoms, offer helpful educational health insights, "
                "and categorize their risk level.\n\n"
                "Follow these strict clinical rules:\n"
                "1. Start by asking for the patient's age and how long they have experienced the symptoms.\n"
                "2. Check for critical 'red flag' symptoms (e.g., chest pain, severe shortness of breath, sudden numbness).\n"
                "3. Based on their answers, explicitly provide a 'Triage Recommendation':\n"
                "   - EMERGENCY: Advise them to visit an ER immediately.\n"
                "   - ROUTINE: Advise booking an appointment with a primary care doctor.\n"
                "   - SELF-CARE: Provide safe, standard home care tips (rest, hydration) while monitoring symptoms.\n"
                "4. Always end your advice with a reminder to consult a human physician."
            )
        }
    ]

# Display previous conversation history in the UI (skipping system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6. Accept Interactive User Input
if user_input := st.chat_input("Describe your symptoms (e.g., 'I have a mild fever and a sore throat')..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 7. Generate Medical Triage Response using conversation context
    with st.chat_message("assistant"):
        try:
            # Structuring the history string for your client.responses endpoint
            chat_context = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
            
            response = client.responses.create(
                model="gpt-5.4-mini",
                input=chat_context + "\nAssistant:",
                store=True,
            )
            
            ai_response = response.output_text
            st.markdown(ai_response)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
