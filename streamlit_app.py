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
predictions = pd.read_csv("prediction_output.csv", index_col=False)

max_rows = predictions.shape[0]  # calculates the number of rows in predictions dataset


# --------setting page config -------------------------------------------------------
#im = Image.open("/content/streamlit/DR_icon.jpeg")
st.set_page_config(
    page_title="Customer Churn Prediction",  # edit this for your usecase
    #page_icon=im,  # Adds datarobot logo to the app tab
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "App to access churn score and understand churn prediction explanations."
    },
)
col1, col2 = st.columns([8, 1])

with col1:
    st.header(":blue[Customer Churn prediction]")  # edit this for your usecase
    st.markdown(
        "_Allows you to access churn score/top churn reason (using Datarobot) and \
                drill down on customers based on their top churn reason_"
    )
with col2:
    #st.image("/content/streamlit/DR_icon.jpeg", width=50)  # Image for logo
    st.caption("**_Powered by Datarobot & NCS_**")


# st.sidebar.header("Customer Churn Prediction ") #uncomment and edit this for your usecase in case you need a sidebar


col3, col4 = st.columns([1, 1])
# ----------------------------------Code to show different visualizations in the app
with st.container():
    with st.expander("Make your criteria selections"):
        with col3:
            threshold = st.slider(
                "Select churn threshold", min_value=0.00, max_value=1.00, value=(0.0, 1.00)
            )
            max_rows = predictions[
                (predictions["Churn_Value_1_PREDICTION"] >= threshold[0])
                & (predictions["Churn_Value_1_PREDICTION"] <= threshold[-1])
            ].shape[
                0
            ]  # calculates the number of rows in predictions dataset based on churn threshold criteria
        with col4:
            display_rows = st.slider(
                "Select how many customers you want to see within the interval ",
                min_value=1,
                max_value=max_rows,
                value=max_rows,
            )

        # columns to display in churn scores table
        columns_to_display = ["Customer_ID_x", "Churn_Value_1_PREDICTION"]
        # code to create dynamic dataframe based on user selection in the slider
        predictions_subset = (
            predictions[
                (predictions["Churn_Value_1_PREDICTION"] >= threshold[0])
                & (predictions["Churn_Value_1_PREDICTION"] <= threshold[-1])
            ]
            .sort_values(by="Churn_Value_1_PREDICTION", ascending=False)
            .reset_index(drop=True)
            .head(display_rows)
        )
        # Plot to show top churn reason
        plot_df = (
            predictions_subset["EXPLANATION_1_FEATURE_NAME"]
            .value_counts()
            .reset_index()
            .rename(
                columns={"index": "Feature_name", "EXPLANATION_1_FEATURE_NAME": "customers"}
            )
            .sort_values(by="count")
        )
        fig = px.bar(
            plot_df,
            y = "customers",
            x = "count",
            orientation="h",
            title="Top churn reason distribution",
    )

with st.container():
    st.subheader(":blue[Churn score and top reason]")
    col1, col2 = st.columns([1, 1])
    with col1:
        # st.markdown("**Top churn reasons**")
        tab1, tab2 = st.tabs(["View plot", "View data"])
        # Plot to show top reason for churn (prediction explanation ) by #customers
        tab1.plotly_chart(fig)
        # code to display the information in above plot as table
        tab2.markdown("")  # To skip a line in the UI
        tab2.markdown(":blue[**Top churn reason by #customers**]")
        tab2.table(plot_df.sort_values(by="customers", ascending=False))
    with col2:
        # st.markdown("")  # To skip a line in the UI
        # st.markdown("")  # To skip a line in the UI
        # st.markdown("")  # To skip a line in the UI
        # st.markdown("")  # To skip a line in the UI
        # st.markdown("")  # To skip a line in the UI
        # code to show dataframe in the app
        # st.markdown("**Churn scores for customers**")
        # st.write('Churn risk score')
        
        # st.markdown("**Top churn reasons**")
        tab1, tab2 = st.tabs(["View plot", "View data"])
        # Plot to show top reason for churn (prediction explanation ) by #customers
        tab1.plotly_chart(fig)
        # code to display the information in above plot as table
        tab2.markdown("")  # To skip a line in the UI
        tab2.markdown(":blue[**Top churn reason by #customers**]")
        tab2.table(plot_df.sort_values(by="customers", ascending=False))

        st.dataframe(
            predictions_subset[columns_to_display].rename(
                columns={
                    "Customer_ID_x": "Customer_ID",
                    "Churn_Value_1_PREDICTION": "Churn score",
                }
            )
        )
        # st.markdown('**Note**: _Churn label in the table above is based on the defualt churn threshold set for the deployment_')


with st.container():
    st.subheader(":blue[Investigate customers based on their top churn reason]")
    # Cdoe to further drill down on customers based on their top reason to churn
    reason_select = st.selectbox(
        "Select churn reason to view customers",
        list(pd.unique(predictions_subset["EXPLANATION_1_FEATURE_NAME"])),
    )
    display_df = (
        predictions_subset[
            predictions_subset["EXPLANATION_1_FEATURE_NAME"] == reason_select
        ]
        .reset_index()
        .sort_values(by="Churn_Value_1_PREDICTION", ascending=False)
        .drop(
            columns=[
                "index",
                "DEPLOYMENT_APPROVAL_STATUS",
                "Customer_ID_y",
                "Churn_Value_0_PREDICTION",
                "Churn_Value_PREDICTION",
                "THRESHOLD",
                "POSITIVE_CLASS",
            ],
            axis=1,
        )
        .rename(
            columns={
                "Customer_ID_x": "Customer_ID",
                "Churn_Value_1_PREDICTION": "Churn score",
            }
        )
    )
    st.dataframe(display_df)






# data
items = ['item1', 'item2','item3']
processos = ['processo1','processo2','processo3']
artigos = ['artigo_x','artigo_y','artigo_z']

# appending data
if "pedidos" not in st.session_state:
    st.session_state['pedidos'] = []

def register_order(p):
    st.session_state['pedidos'].append(p)

# panel title
st.title('Loan application inputs :moneybag:')

# order register
with st.sidebar.form(key='cad_form', clear_on_submit=True):
    st.write("Would you like to apply for a loan?")

    client = st.text_input('Enter your name?', key='cli')
    # its = st.selectbox("Selecione o item",pd.Series(items),key='it')
    # article = st.selectbox("Selecione o artigo", pd.Series(artigos),key='art')
    # processes = st.multiselect("Selecione o(s) processo(s)", pd.Series(processos),key='proc')
    loan_amnt = st.number_input("loan amount",key='qt')
    term = st.number_input("months?",key='qtt')
    emp_length = st.number_input("years of employment",key='qtr')
    annual_inc = st.number_input("annual income",key='qty')
    # volume = st.number_input("Volume da peça (Kg)", key='v')
    new_ped = {'Cliente':client,'loan_amnt':loan_amnt,'term':term,'emp_length':emp_length, 'annual_inc':annual_inc}

    if st.form_submit_button("Submit your request :white_check_mark:"):
        register_order(new_ped)
        st.write("Thank you, your request is being processed! :heavy_check_mark:")
        
# check
if len(st.session_state["pedidos"]) > 0:
    st.write(pd.DataFrame(st.session_state["pedidos"]))
else:
    st.write("No applications in progress")
