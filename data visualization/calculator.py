#CT20254675416
import streamlit as st

st.title("Simple calculator")

c1,c2=st.columns(2)
fnum=c1.number_input("Enter first number",value=0)
snum=c2.number_input("Enter second number",value=0)

options=['Add','Sub','Mul','Div']
choice=st.radio("Select Operation",options)

button=st.button("Calculate")

result=0
if button:
    if choice=='Add':
        result=fnum+snum
    if choice=='Sub':
        result=fnum-snum
    if choice=='Mul':
        result=fnum*snum
    if choice=='Div':
        result=fnum/snum
st.warning(f'Result:{result}')

st.snow()
