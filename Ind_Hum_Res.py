
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import folium
import numpy as np
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title= "HRM",layout= "wide")
st.markdown("""
    <h1 style='text-align: center; color: black;'>Industrial Human Resource Visualization</h1>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(f""" <style>.stApp {{
                        background:url("https://www.economy-ni.gov.uk/sites/default/files/images/economy/news/Stats%20Graphs.jpeg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)

data = pd.read_csv("/content/HRM_NLP_final.csv")
select = option_menu(
    menu_title = None,
    options = ["HOME","Data Visualize","Geo Visualize"],
    icons =["house","bar-chart"],orientation="horizontal")
if select == "HOME":
  st.markdown("<span style='color: black; font-weight: bold;'>In India, the industrial classification of the workforce is essential to understand the distribution of the labor force across various sectors. The classification of main workers and marginal workers, other than cultivators and agricultural laborers, by sex and by section, division, and class, has been traditionally used to understand the economic status and employment trends in the country. However, the current data on this classification is outdated and may not accurately reflect the current state of the workforce. The aim of this study is to update the information on the industrial classification of the main and marginal workers, other than cultivators and agricultural laborers, by sex and by section, division, and class, to provide relevant and accurate data for policy making and employment planning.</span>", unsafe_allow_html=True)

  st.markdown("<span style='color: black; font-weight: bold;'>This study aims to update and visualize the industrial classification of main and marginal workers, excluding cultivators and agricultural laborers, by sex, section, division, and class. By providing accurate and up-to-date data, this project will serve as a vital tool for policymakers and employment planners, facilitating informed decision-making and strategic planning to address current employment trends and economic needs.</span>", unsafe_allow_html=True)

if select == "Data Visualize":
  data = pd.read_csv("/content/HRM_NLP_final.csv")
  col1, col2, col3 = st.columns([1, 1, 1])
  with col1:
    unique_states = sorted(data['State'].unique())
    st.markdown("<span style='color: black; font-weight: bold;'>Select State</span>", unsafe_allow_html=True); selected_state = st.selectbox("", unique_states, key="state_selector_unique")

  with col2:

    filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
    st.markdown("<span style='color: black; font-weight: bold;'>Select District</span>", unsafe_allow_html=True); selected_district = st.selectbox("", filtered_districts, key="district_selector_unique")

  with col3:

    filtered_nic_names = data[data['District'] == selected_district]['NICName'].unique()
    filtered_nic_names = [nic.replace('[', '').replace(']', '').replace("'", "") for nic in filtered_nic_names]
    filtered_nic_names = [nic.capitalize() for nic in filtered_nic_names]
    filtered_nic_names = sorted(filtered_nic_names)

    st.markdown("<span style='color: black; font-weight: bold;'>Select NIC Name</span>", unsafe_allow_html=True); selected_nic_name = st.selectbox("", filtered_nic_names, key="nic_name_selector")

  state_data = data[(data['State'] == selected_state)]
  district_data = data[(data['District'] == selected_district)]

  st.markdown(f"<span style='color: black; font-weight: bold;'>Showing data for {selected_state} - {selected_district}</span>", unsafe_allow_html=True)

  total_state_workers = state_data['MainWorkersTotalPersons'].sum()
  total_district_workers = district_data['MainWorkersTotalPersons'].sum()

  st.markdown(f"<span style='color: black; font-weight: bold;'>Total number of state workers: {total_state_workers}</span>", unsafe_allow_html=True)
  st.markdown(f"<span style='color: black; font-weight: bold;'>Total number of district workers: {total_district_workers}</span>", unsafe_allow_html=True)

  st.subheader("Data Summary")
  st.write(data.describe())
  # st.write(data)

  state_summary = state_data[[
      'MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales',
      'MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales',
      'MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales',
      'MarginalWorkersTotalPersons', 'MarginalWorkersTotalMales', 'MarginalWorkersTotalFemales',
      'MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales',
      'MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales',
      'TotalPopulation'
  ]].sum().sort_values()

  st.subheader("State-wise Summary")

  import plotly.express as px

  fig = px.bar(
      x=state_summary.index,
      y=state_summary.values,
      color=state_summary.index,
      color_discrete_sequence=px.colors.sequential.Blues,
      labels={'y': 'Count', 'x': 'Worker Cat'},
      title=f"{selected_state} - Workers Summary"
  )
  fig.update_layout(barmode='stack')
  st.plotly_chart(fig)

  # Plotting data for Rural, Main, and Urban workers
  rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
  urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

  rural_data = data[rural_cols].sum().values
  main_data = data[['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']].iloc[0].values
  urban_data = data[urban_cols].sum().values

  # Define blue shades
  blues = ['#1f77b4', '#aec7e8', '#6baed6']

  fig, ax = plt.subplots(figsize=(10, 6))
  x_labels = ['Rural', 'Main', 'Urban']

  # Plot bars with custom colors
  ax.bar(x_labels, rural_data, color=blues[0], label='Rural')
  ax.bar(x_labels, main_data, bottom=rural_data, color=blues[1], label='Main')
  ax.bar(x_labels, urban_data, bottom=rural_data + main_data, color=blues[2], label='Urban')

  ax.set_title(f"{selected_state} - {selected_district} - Workers Distribution")
  ax.legend()

  st.pyplot(fig)


  # Plotting data for Marginal workers (using pie chart)
  marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']
  marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales']

  marginal_data_rural = data[marginal_cols_rural].sum().values
  marginal_data_urban = data[marginal_cols_urban].sum().values

  fig, ax = plt.subplots(figsize=(10, 6))
  ax.pie(marginal_data_rural, labels=marginal_cols_rural, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#aec7e8', '#6baed6'])
  ax.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers Distribution")
  st.pyplot(fig)

  fig, ax = plt.subplots(figsize=(10, 6))
  ax.pie(marginal_data_urban, labels=marginal_cols_urban, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#aec7e8', '#6baed6'])
  ax.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers Distribution")
  st.pyplot(fig)

  main_cols = ['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']
  rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
  urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

  main_data = data[['State'] + main_cols].groupby('State').sum().reset_index()
  rural_data = data[['State'] + rural_cols].groupby('State').sum().reset_index()
  urban_data = data[['State'] + urban_cols].groupby('State').sum().reset_index()

  main_data_melted = main_data.melt(id_vars='State', var_name='WorkerType', value_name='Count')

  fig = px.bar(main_data_melted, x='State', y='Count', color='WorkerType',
              title='Differences in State-wise',
              labels={'Count': 'Total Workers Count'},
              color_discrete_sequence=['#1f77b4', '#aec7e8', '#6baed6'],
              template='plotly_white')

  fig.update_layout(barmode='group', xaxis_title='State', yaxis_title='Total Workers Count (Log Scale)',
                    showlegend=True, yaxis_type="log")

  st.plotly_chart(fig)

if select == "Geo Visualize":

  # Geo-Map Visualization
  data = pd.read_csv("/content/HRM_NLP_final.csv")

  unique_states = sorted(data['State'].unique())
  selected_state = st.selectbox("Select State", unique_states, key="state_selector_unique")

  filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
  selected_district = st.selectbox("Select District", filtered_districts, key="district_selector_unique")

  state_data = data[(data['State'] == selected_state)]
  district_data = data[(data['District'] == selected_district)]

  folium_map = folium.Map(location=[28.6139, 77.2090], zoom_start=5)

  marker_cluster = MarkerCluster().add_to(folium_map)

  for idx, row in state_data.iterrows():
      lat, lon = row['latitude'], row['longitude']
      total_workers = row['MainWorkersTotalPersons']
      male_female_ratio = row['MaleFemaleRatio']
      popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
      folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

  for idx, row in district_data.iterrows():
      lat, lon = row['latitude'], row['longitude']
      total_workers = row['MainWorkersTotalPersons']
      male_female_ratio = row['MaleFemaleRatio']
      popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
      folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

  st.components.v1.html(folium_map._repr_html_(), width=1200, height=500)











