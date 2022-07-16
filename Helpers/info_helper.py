import pandas as pd
import streamlit as st
import datetime


class OppConfig:

    def __init__(self):
        self.index_column = 33
        self.excel_file = './Assets/Opps-7-15-2022.xlsx'
        self.excel_sheet = 'opps'
        self.start_time = datetime.date(2022, 1, 1)
        self.end_time = datetime.date(2022, 12, 31)


@st.cache()
def read_data(excel_file, index_col) -> pd.DataFrame:
    """
    Opens and reads data from the specified Excel file.
    :param excel_file: The full name of the Excel file to be processed.
    :param index_col: The column to use as the dataframe index.
    :return: A dataframe containing the Excel data.
    """
    return pd.read_excel(excel_file, index_col=33, sheet_name='opps')


def build_summary(df) -> pd.DataFrame:
    """
    Create summary details for the supplied opportunity dataframe.
    :param df: The dataframe to use as a data source.
    :return: A dataframe containing summary data for the provided source.
    """
    opps_won = df[df['Status'] == 'Won'].shape[0]
    opps_lost = df[df['Status'] == 'Lost'].shape[0]
    opps_open = df[df['Status'] == 'Open'].shape[0]

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
