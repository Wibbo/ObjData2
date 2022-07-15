import streamlit as st
import pandas as pd
import seaborn as sns
from datetime import date as dt
import datetime


@st.cache()
def read_data(excel_file, index_col) -> pd.DataFrame:
    """
    Opens and reads data from the specified Excel file.
    :param excel_file: The full name of the Excel file to be processed.
    :param index_col: The column to use as the dataframe index.
    :return: A dataframe containing the Excel data.
    """
    return pd.read_excel(excel_file, index_col=index_col, sheet_name='opps')


def build_summary(df) -> pd.DataFrame:
    opps_won = df[df['Status'] == 'Won'].shape[0]
    opps_lost = df[df['Status'] == 'Lost'].shape[0]
    opps_open = df[df['Status'] == 'Open'].shape[0]
    opps_total = df.shape[0]

    opps_won_e = df[(df['Status'] == 'Won') & (df['Type'] == 'Existing Business')].shape[0]
    opps_won_n = df[(df['Status'] == 'Won') & (df['Type'] == 'New Business')].shape[0]
    opps_won_c = df[(df['Status'] == 'Won') & (df['Type'] == 'Continuation')].shape[0]

    opps_lost_e = df[(df['Status'] == 'Lost') & (df['Type'] == 'Existing Business')].shape[0]
    opps_lost_n = df[(df['Status'] == 'Lost') & (df['Type'] == 'New Business')].shape[0]
    opps_lost_c = df[(df['Status'] == 'Lost') & (df['Type'] == 'Continuation')].shape[0]

    opps_open_e = df[(df['Status'] == 'Open') & (df['Type'] == 'Existing Business')].shape[0]
    opps_open_n = df[(df['Status'] == 'Open') & (df['Type'] == 'New Business')].shape[0]
    opps_open_c = df[(df['Status'] == 'Open') & (df['Type'] == 'Continuation')].shape[0]

    data = {'Opportunities measure': ['Opportunities won', 'Opportunities lost', 'Opportunities open'],
            'Count': [opps_won, opps_lost, opps_open],
            'New': [opps_won_n, opps_lost_n, opps_open_n],
            'Existing': [opps_won_e, opps_lost_e, opps_open_e],
            'Continuation': [opps_won_c, opps_lost_c, opps_open_c],
            }

    return pd.DataFrame(data)


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """
    st.markdown("## A few sample opportunities")
    st.markdown('Showing 12 sample records from the opportunity database')

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Date of first opportunity", datetime.date(2019, 7, 6))
        start_datetime = dt(start_date.year, start_date.month, start_date.day)
)


        print(type(start_date))
        print(type(start_datetime))


    with col2:
        end_date = st.date_input("Date of last opportunity", datetime.date(2019, 7, 6))

    df_opps = read_data('./Assets/Opps-7-15-2022.xlsx', 33)

    df_opps = df_opps[
        (df_opps.index >= start_date) &
        (df_opps.index <= end_date)
       ]

    st.dataframe(df_opps.head(n=12))

    st.markdown("## Headline statistics")
    summary = build_summary(df_opps)
    st.dataframe(summary)


