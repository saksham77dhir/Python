import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.subheader('Titanic Data Insights and Visualization')
st.markdown('Get all the insights as stats and visuals of Titanic data in this application')

st.subheader('Dataset')

# Load dataset and drop rows with missing key values
df = sns.load_dataset('titanic').dropna(subset=['age', 'embarked', 'pclass', 'sex'])

# Filters
st.sidebar.header("Filter Options")

gender = st.sidebar.multiselect(
    'Gender',
    options=df['sex'].unique(),
    default=df['sex'].unique()
)

pclass = st.sidebar.multiselect(
    'Passenger Class',
    options=df['pclass'].unique(),
    default=df['pclass'].unique()
)

min_age, max_age = st.sidebar.slider(
    'Age',
    min_value=int(df['age'].min()),
    max_value=int(df['age'].max()),
    value=(int(df['age'].min()), int(df['age'].max()))
)

filtered_data = df[
    (df['sex'].isin(gender)) &
    (df['pclass'].isin(pclass)) &
    (df['age'] >= min_age) &
    (df['age'] <= max_age)
].copy()

st.dataframe(filtered_data)

st.subheader('Visuals of Insights')

# Age distribution
fig = px.histogram(filtered_data, x='age', title='Age Distribution', color='embarked')
st.plotly_chart(fig)
st.markdown("This graph shows the distribution of age of people on the Titanic")

# Box plot (convert survived to string for coloring)
filtered_data['survived'] = filtered_data['survived'].astype(str)
fig = px.box(filtered_data, x='pclass', y='age', color='survived',
             title='Age Distribution by Class & Survival')
st.plotly_chart(fig)

