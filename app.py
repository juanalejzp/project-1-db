from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd
from campaigns_db_helper import get_all_the_campaigns
from workers_db_helper import insert_workers_in_bulk

load_dotenv()

st.title("Call Center")

st.title("Create Campaigns")
campaign_name = st.text_input('Campaign Name')
start_date = st.date_input(label="Start Date")
aim = st.text_input('Campaign Aim')
customer = st.text_input('Campaign Customer')
submit = st.button("Submit")

if submit:
  if not campaign_name or not start_date or not aim or not customer:
    st.error("Please fill in all fields.")
  else:
    st.write(f"Creating campaign: {campaign_name}")
    st.write(f"Database name: {os.getenv('DB_NAME')}")
    
    connection = None
    try:
      connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
      )
      if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        
        query = """
        INSERT INTO campaigns (campaign_name, start_date, aim, customer)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            campaign_name,
            start_date,
            aim,
            customer
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        st.success("The campaign has been successfully saved.")
    except Error as e:
      st.error(f"Error connecting to database: {e}")
    finally:
      if connection and connection.is_connected():
        connection.close()

st.title("Upload Workers")

def process_and_transform_df(df):
    try:
        df = df.rename(columns={
            'Codigo': 'code',
            'Nombre': 'first_name',
            'Apellidos': 'last_name',
            'Email': 'email',
            'Email Corporativo': 'corporate_email',
            'Cargo': 'position',
            'Horas del contrato': 'Contract hours'
        })
        
        df['code'] = df['code'].astype(str)
        df['fullName'] = df['first_name'] + ' ' + df['last_name']
        df['emails'] = df['email'].fillna('') + ',' + df['corporate_email'].fillna('')
        df['position'] = df['position']

        df = df[['code', 'fullName', 'emails', 'position']]
        
        return df
    
    except KeyError as e:
        st.error(f"Error processing columns: {e}")
        return pd.DataFrame()

def extract_Workers_from_excel(df, campaigns_id):
    try:
        
        df = process_and_transform_df(df)
        
        if df.empty:
            st.warning("No data to insert after processing.")
            return
        
        df['campaign_id'] = campaigns_id

        insert_workers_in_bulk(df, campaigns_id, table_name='workers')
        
        st.write("Workers have been created successfully")
        st.write(df)

    except Exception as e:
        st.error(f"Error processing the data: {e}")


campaigns = get_all_the_campaigns()

campaigns_dict = {campaign['id']: campaign['campaign_name'] for campaign in campaigns}
campaigns_ids = list(campaigns_dict.keys())

selected_campaigns_id = st.selectbox("Select a campaign", campaigns_ids, format_func=lambda id: campaigns_dict[id])

uploaded_file1 = st.file_uploader("Upload the first Excel file", type=["xls", "xlsx"])

uploaded_file2 = st.file_uploader("Upload the second Excel file", type=["xls", "xlsx"])

if st.button("Save workers"):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        try:
            df1 = pd.read_excel(uploaded_file1)
            df2 = pd.read_excel(uploaded_file2)
            
            combined_df = pd.concat([df1, df2], ignore_index=True)
            
            extract_Workers_from_excel(combined_df, selected_campaigns_id)
        
        except Exception as e:
            st.error(f"Error processing the files: {e}")
    else:
        st.warning("Please upload both Excel files.")
