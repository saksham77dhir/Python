import streamlit as st
import pickle
import numpy as np

model = pickle.load(open('model.pkl', 'rb'))

st.title("Rock vs Mine Prediction")

input_data = st.text_input("Enter 60 values separated by comma")

if st.button("Predict"):
    try:
        data = np.asarray(input_data.split(','), dtype=float)
        prediction = model.predict([data])
        
        if prediction[0] == 'R':
            st.success("Rock")
        else:
            st.success("Mine")
    except:
        st.error("Enter valid 60 numbers")