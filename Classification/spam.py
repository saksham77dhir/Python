import streamlit as st
import pandas as pd
import joblib


# --- Page config ---
st.set_page_config(
    page_title="Spam Detection App",
    page_icon="🈸",
    layout="wide"
)

# --- Load model and vectorizer ---
@st.cache_resource
def load_model():
    model_data = joblib.load('spam_detector.joblib')
    return model_data['model'], model_data['vectorizer']

try:
    model, vectorizer = load_model()

    # --- Main UI ---
    st.title("🈸 Spam Message Detector")
    st.write("Enter a message below to check whether it's **spam** or **ham (not spam)**.")

    # Text input
    message = st.text_area("Enter the message:", height=100)

    if st.button("Check Message", type="primary"):
        if message.strip():
            # Preprocess and predict
            message_clean = message.lower()
            message_vectorized = vectorizer.transform([message_clean])
            prediction = model.predict(message_vectorized)[0]
            probability = model.predict_proba(message_vectorized)[0]

            # --- Determine spam probability safely ---
            classes = list(model.classes_)
            try:
                spam_index = classes.index("spam")
            except ValueError:
                # if model used numeric labels
                spam_index = 1 if 1 in classes else 0

            spam_prob = probability[spam_index]

            # --- Show results ---
            st.write("---")
            col1, col2 = st.columns(2)

            with col1:
                if prediction == "spam" or prediction == 1:
                    st.error("🚫 This message is likely **SPAM**!")
                else:
                    st.success("✅ This message is likely **HAM** (not spam)")

            with col2:
                st.metric("Spam Probability", f"{spam_prob * 100:.2f}%")

            # Confidence progress bars
            st.write("Confidence Scores:")
            st.progress(spam_prob, text="Spam")
            st.progress(1 - spam_prob, text="Ham")

    else:
        st.warning("⚠️ Please enter a message to check")

            
        #example messages
        with st.expander("Example Messages"):
            st.write("""
                     **Spam Examples:**
                     - "Congratulations! You've won a $1,000 Walmart gift card.Click here to claim your prize."
                     -"URGENT! Your account has been compromised.Please reset your password immediately."
                     -"Get paid to work from here! No experience required.Sign up now!"
                     
                     **Ham Examples**
                     -"Hey,are we still on for lunch tomorrow?"
                     -"Don't forget to bring the documents for the meeting"
                     -"Happy Birthday! Wishing you a wonderful day filled with joy."
                     """)
            
except Exception as e:
    st.error(f"""Error loading model: {e}"
             Please ensure:
            1.The 'spam_detector.joblib' file is in the correct location.
            2.The saved file contains both the model and vectorizer.body
            3.All required packages are installed"""
    )
    #footer
    st.markdown("---")
    st.markdown("Developed using Streamlit")
