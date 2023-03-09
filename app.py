# All working code in one cell 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import streamlit as st


filenames = []
uploaded_files = st.file_uploader("Upload a Dataset", type=["csv", "txt" , "excel"], accept_multiple_files=True)
if uploaded_files: 
    for uploaded_file in uploaded_files:
       filenames.append(uploaded_file)
       st.write("Filename: ", uploaded_file.name)

if filenames is not None:
    df_main = pd.concat([pd.read_csv(filename) for filename in filenames])
    df_main['date'] = pd.to_datetime(df_main.order_date)
    df_main['Month_Year'] = df_main['date'].apply(lambda x: x.strftime('%m-%Y'))
    month_list  = df_main.Month_Year.unique()
    def Frequency(df , month):
        df2=df.query("new_user == 1")
        unique_user_id_list = df2.user_id.unique()
        new_user_month_wise_list = []
        for i in range(len(df)):
            x=df['user_id'].iloc[i]
            if x in unique_user_id_list:
                new_user_month_wise_list.append('Yes')
            else:
                new_user_month_wise_list.append('No')
        new_user_month_wise_column = pd.DataFrame(new_user_month_wise_list)
        df = pd.concat([df, new_user_month_wise_column], axis=1)
        df.rename(columns = {0:'New_user_month_wise'}, inplace = True)
        unique_order_number_1_count = df2.user_id.nunique()
        print(df.shape)
        st.write(df.shape)

        frequency_numbers = df.groupby('New_user_month_wise')[['user_id','order_number']].nunique()
        # print(frequency_numbers)
        # st.write(frequency_numbers)

        old_user_order_frequency = (frequency_numbers.order_number[0]) / frequency_numbers.user_id[0]
        New_user_order_frequency = frequency_numbers.order_number[1] / frequency_numbers.user_id[1]
        
        print(f' Count of orders ordered by new users :{unique_order_number_1_count}')
        print(f' New user order frequency : {New_user_order_frequency}')
        print(f' old user order frequency : {old_user_order_frequency}')
        st.write(f' Count of orders ordered by new users :{unique_order_number_1_count}')
        st.write(f' New user order frequency : {New_user_order_frequency}')
        st.write(f' old user order frequency : {old_user_order_frequency}')
        

    def Referral_orders(df , month):
        referral_orders_data=  df
        referral_orders_data['promocode'] = referral_orders_data['promocode'].str.lower()
        referral_orders_data  = referral_orders_data.loc[referral_orders_data["promocode"].str.startswith('pr', na=False)]
        Total_referral_data = referral_orders_data['order_number'].nunique()
        referral_orders_data_user = referral_orders_data.drop_duplicates(subset=['order_number'], keep='first')
        referral_orders_data_user_wise_split = referral_orders_data_user.device_type.value_counts() 
        referral_orders_data['order_date'] = pd.to_datetime(referral_orders_data['order_date'])
        referral_orders_data['order_date'] = referral_orders_data['order_date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        first_split ='10-'+month
        second_split = '21-'+month
        third_split_1 = '11-'+month
        third_split_2 = '20-'+month

        first_split_data = referral_orders_data.loc[referral_orders_data['order_date'] <= first_split]
        second_split_data = referral_orders_data.loc[referral_orders_data['order_date'] >= second_split]
        third_split_data = referral_orders_data.loc[(referral_orders_data['order_date'] >= third_split_1) & (referral_orders_data['order_date'] <= third_split_2)]
        first_referral_frequency_data = first_split_data['order_number'].nunique()
        second_referral_frequency_data = second_split_data['order_number'].nunique()
        third_referral_frequency_data = third_split_data['order_number'].nunique()
        column_names_for_gross_AOV = ['total_store_credit','total_shipping_charges','total_discount','total_order_amount']
        df['Gross_AOV']= df[column_names_for_gross_AOV].sum(axis=1)
        gross_AOV_data = df
        gross_AOV_data = gross_AOV_data.drop_duplicates(subset=['order_number'], keep='first')
        gross_AOV_final_value = gross_AOV_data.Gross_AOV.mean()
        net_AOV_final_value = gross_AOV_data.total_order_amount.mean()

        print(f' Total unique referral orders count (monthly) : {Total_referral_data}')
        print(f' referral orders count month wise split : {referral_orders_data_user_wise_split}')
        st.write(f' Total unique referral orders count (monthly) : {Total_referral_data}')
        st.write(f' referral orders count month wise split : {referral_orders_data_user_wise_split}')

        
        print(f' Referral users From date 1st to 10th  : {first_referral_frequency_data}')
        print(f' Referral users From date 11th to 20th   : {second_referral_frequency_data}')
        print(f' Referral users From date 21st to 30th   : {third_referral_frequency_data}')
        st.write(f' Referral users From date 1st to 10th  : {first_referral_frequency_data}')
        st.write(f' Referral users From date 11th to 20th   : {second_referral_frequency_data}')
        st.write(f' Referral users From date 21st to 30th   : {third_referral_frequency_data}')

        print(f' value of Gross AOV : {gross_AOV_final_value}')
        print(f' value of Net AOV : {net_AOV_final_value}')
        st.write(f' value of Gross AOV : {gross_AOV_final_value}')
        st.write(f' value of Net AOV : {net_AOV_final_value}')


    for i in range(len(month_list)):
        print("------------------------------------------------------------------------------------")

        print(month_list[i])
        st.write("------------------------------------------------------------------------------------")
        
        st.write(month_list[i])
        df= (df_main[df_main['Month_Year'] == month_list[i]])
        Frequency(df , month_list[i])
        Referral_orders(df , month_list[i])
        print("------------------------------------------------------------------------------------")
        st.write("------------------------------------------------------------------------------------")


