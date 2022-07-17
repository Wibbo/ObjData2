import pandas as pd
import streamlit as st
from datetime import datetime as dt
import datetime


class OppConfig:

    def __init__(self):
        self.index_column = 33
        self.excel_file = './Assets/Opps-7-15-2022.xlsx'
        self.excel_sheet = 'opps'
        self.start_time = datetime.date(2022, 1, 1)
        self.end_time = datetime.date(2022, 12, 31)

    @staticmethod
    def first_record(df: pd.DataFrame):
        min_date = df.index.min()
        return min_date

    @staticmethod
    def last_record(df: pd.DataFrame):
        max_date = df.index.max()
        return max_date


def read_data(excel_file, col_index, worksheet) -> pd.DataFrame:
    """
    Reads opportunity data from an Excel file
    :param excel_file: Name of the file to read
    :param col_index: The column to use as an index
    :param worksheet: The name of the worksheet where data exists
    :return:
    """
    df_opps = pd.read_excel(excel_file, sheet_name=worksheet)

    # Remove spaces and punctuation from the column names
    df_opps.columns = df_opps.columns.str.replace(' ', '')
    df_opps.columns = df_opps.columns.str.replace('.', '')
    df_opps['Created'] = df_opps['CreatedOn']
    df_opps['rec_count'] = 1
    df_opps = df_opps.set_index(['CreatedOn'])
    df_opps.index = df_opps.index.astype('datetime64[ns]')
    return df_opps


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
