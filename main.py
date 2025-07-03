import pandas as pd
import plotly.express as px
import streamlit as st
from collections import defaultdict

def clamp(val, minimum, maximum):
    return min(max(minimum, val), maximum)

df = pd.read_csv('Healthcare Dataset Clean.csv')
st.set_page_config(page_title='Healthcare Data Visualization', page_icon='⚕️', layout='wide')
admissions_metric = defaultdict(lambda: 0)
total = 0

print(df.head())

x_options = [
    'Name', 
    'Age', 
    'Gender', 
    'Blood Type', 
    'Medical Condition', 
    'Date of Admission', 
    'Doctor', 
    'Hospital', 
    'Insurance Provider', 
    'Billing Amount', 
    'Room Number', 
    'Admission Type', 
    'Discharge Date', 
    'Medication', 
    'Test Results'
    ]

y_options = ['Total Admissions', 'Admissions Percentile']

st.title('Admissions Data Visualization')

x_choice = st.selectbox('Choose a patient attribute for the x-axis: ', x_options)
y_choice = st.selectbox('Choose an admissions metric for the y-axis: ', y_options)

if y_choice == y_options[0]:
    for i in df[x_choice]:
        admissions_metric[i] += 1
elif y_choice == y_options[1]:
    for i in df[x_choice]:
        admissions_metric[i] += 1

    max_admissions = max(list(admissions_metric.values()))
    min_admissions = min(list(admissions_metric.values()))

    max_admissions -= min_admissions

    for i in list(admissions_metric.keys()):
        admissions_metric[i] -= min_admissions
        admissions_metric[i] /= max_admissions
        admissions_metric[i] *= 100
        admissions_metric[i] = clamp(admissions_metric[i], 1, 100)

new_df = pd.DataFrame(list(admissions_metric.items()), columns=[x_choice, y_choice])

bar_chart = px.bar(new_df, x=new_df[x_choice], y=new_df[y_choice], title='{} by {}'.format(y_choice, x_choice))

st.subheader('Bar Chart')
st.plotly_chart(bar_chart)

box_plot = px.box(new_df, y=y_choice, labels={ 0:x_choice }, points=False, title='{} Distribution'.format(y_choice, x_choice))

st.subheader('Box Plot')
st.plotly_chart(box_plot)
st.caption('Note: box plot represents distribution of bar chart y-axis values')
