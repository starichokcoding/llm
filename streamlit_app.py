#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 2024

@author: NCS
"""

from PIL import Image
import numpy as np

# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import datarobot

# read prediction data that we saved as a csv file while working on the ai_accelerator_modelInsights_streamlit_v1.ipynb notebook
predictions = pd.read_csv("https://aws-datarobot.s3.us-west-2.amazonaws.com/predictions/loan_dr_aws_smpl_apr2024.csv")

max_rows = predictions.shape[0]  # calculates the number of rows in predictions dataset


# --------setting page config -------------------------------------------------------
# im = Image.open("/content/streamlit/DR_icon.jpeg")
st.set_page_config(
    page_title="Loan Approval Prediction",  # edit this for your usecase
    #page_icon=im,  # Adds datarobot logo to the app tab
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "App to access likelihood score and understand its prediction explanations."
    },
)
col1, col2 = st.columns([8, 1])

with col1:
    st.header(":blue[Customer Loan default prediction]")  # edit this for your usecase
    st.markdown(
        "_Allows you to access churn score/top churn reason (using Datarobot) and \
                drill down on customers based on their top churn reason_"
    )
with col2:
    #st.image("/content/streamlit/DR_icon.jpeg", width=50)  # Image for logo
    st.caption("**_Powered by Datarobot & NCS_**")


# st.sidebar.header("Load default Prediction ") #uncomment and edit this for your usecase in case you need a sidebar


with st.container():
    with st.expander("Make your criteria selections"):
        threshold = st.slider(
            "Select likelihood of default interval", min_value=0.00, max_value=1.00, value=(0.0, 1.00)
        )
        max_rows = predictions[
            (predictions["is_bad_1_PREDICTION"] >= threshold[0])
            & (predictions["is_bad_1_PREDICTION"] <= threshold[-1])
        ].shape[
            0
        ]  # calculates the number of rows in predictions dataset based on churn threshold criteria
        display_rows = st.slider(
            "Select how many customers you want to see within the interval ",
            min_value=1,
            max_value=max_rows,
            value=max_rows,
        )

    # columns to display in scores table
    columns_to_display = ["Customer_ID_x", "Churn_Value_1_PREDICTION"]
    # code to create dynamic dataframe based on user selection in the slider
    predictions_subset = (
        predictions[
            (predictions["is_bad_1_PREDICTION"] >= threshold[0])
            & (predictions["is_bad_1_PREDICTION"] <= threshold[-1])
        ]
        .sort_values(by="is_bad_1_PREDICTION", ascending=False)
        .reset_index(drop=True)
        .head(display_rows)
    )
    # Plot to show top default reason
    plot_df = (
        predictions_subset["EXPLANATION_1_FEATURE_NAME"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Feature_name", "EXPLANATION_1_FEATURE_NAME": "customers"}).sort_values(by="customers"))
    fig = px.bar(
        plot_df,
        x="customers",
        y="Feature_name",
        orientation="h",
        title="Top default reason distribution",
    )

with st.container():
    st.subheader(":blue[Default score and top reason]")
    col1, col2 = st.columns([1, 1])
    with col1:
        # st.markdown("**Top default reasons**")
        tab1, tab2 = st.tabs(["View plot", "View data"])
        # Plot to show top reason for churn (prediction explanation ) by #customers
        threshold1 = [.14, 1]
        top = 100
        
        dfp_subset = predictions[(predictions["is_bad_1_PREDICTION"] >= threshold1[0])& (predictions["is_bad_1_PREDICTION"] <= threshold1[-1])].sort_values(by="is_bad_1_PREDICTION", ascending=False).reset_index(drop=True).head(top)
        dfp_subset['ex1_fn'] = dfp_subset['EXPLANATION_1_FEATURE_NAME'].astype(str) + ": " + dfp_subset['EXPLANATION_1_ACTUAL_VALUE'].astype(str)
        dfp_subset['ex2_fn'] = dfp_subset['EXPLANATION_2_FEATURE_NAME'].astype(str) + ": " + dfp_subset['EXPLANATION_2_ACTUAL_VALUE'].astype(str)
        dfp_subset['ex3_fn'] = dfp_subset['EXPLANATION_3_FEATURE_NAME'].astype(str) + ": " + dfp_subset['EXPLANATION_3_ACTUAL_VALUE'].astype(str)
        dfp_subset['ex4_fn'] = dfp_subset['EXPLANATION_4_FEATURE_NAME'].astype(str) + ": " + dfp_subset['EXPLANATION_4_ACTUAL_VALUE'].astype(str)
        i = 99
        import plotly.express as px
        fig1 = px.bar(pd.DataFrame({'feature' : dfp_subset.filter(regex="ex\d_fn").iloc[i].to_list(), 'impact' : dfp_subset.filter(regex="EXPLANATION_\d_STRENGTH").iloc[i].to_list()}), y = 'feature', x = 'impact', orientation="h")
        tab1.plotly_chart(fig1)
        
        # code to display the information in above plot as table
        tab2.markdown("")  # To skip a line in the UI
        tab2.markdown(":blue[**Top default reason by #customers**]")
        #tab2.table(plot_df.sort_values(by="customers", ascending=False))
    with col2:
        # st.markdown("**Top default reasons**")
        tab1, tab2 = st.tabs(["View plot", "View data"])
        # Plot to show top reason for default (prediction explanation ) by #customers
        tab1.plotly_chart(fig)
        # code to display the information in above plot as table
        #tab2.markdown("")  # To skip a line in the UI
        #tab2.markdown(":blue[**Top default reason by #customers**]")
        #tab2.table(plot_df.sort_values(by="customers", ascending=False))









st.title('Loan application inputs :moneybag:')

# Full example of using the with notation
# st.header('Loan application inputs :moneybag:')
st.subheader('Amazing Virtual Bank Hong Kong')

with st.form('my_form', clear_on_submit=True):
    st.subheader('**Loan application**')

    # Input widgets
    client = st.text_input('Enter your name?')
    loan_amnt = st.slider('Loan Amount', min_value=0, max_value=100000, value=(0, 10000))
    term = st.selectbox('For how long?', ['Until tomorrow', 'Until next year', 'Until next decade'])
    emp_length = st.selectbox('Years of employment', ['Unemployed', 'More that 5', 'More than 10'])
    annual_inc = st.selectbox('What is annual income', ['Zero', 'More than Zero', 'A lot!'])
    contract_agree = st.checkbox('Please check if you understood the terms')
    submitted = st.form_submit_button('Submit')

if submitted:
    st.markdown(f'''
         Thank you! Your application has been submitted:
        - Client Name: `{client}`
        - Loan Amount: `{loan_amnt}`
        - For how long?: `{term}`
        - Employment length: `{emp_length}`
        - Annual income: `{annual_inc}`
        - Agreed with terms: `{contract_agree}`
        ''')

    data = pd.DataFrame({'loan_amnt': [loan_amnt],
            'term': [term],
            'emp_length': [emp_length],
            'annual_inc': [annual_inc]})
    data_new = xgboost.DMatrix(data)
    prediction = model.predict(data_new)
    prediction[0]
else:
    st.write('☝️ Please, fill in the form!')


