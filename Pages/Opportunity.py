import streamlit as st
import altair as alt
import Helpers.info_helper as ih
import math
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def render_summary(delta, df_opps2, end, start):
    """
    Display summary statistics for the opportunities dataframe.
    :param delta: Time between the first and last selected opportunities.
    :param df_opps2: Opportunities within the selected dates.
    :param end: The selected end date.
    :param start: The selected start date.
    """
    st.markdown('---')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Start", start)
    col2.metric("End", end)
    col3.metric("Duration", '{} days'.format(delta.days))
    col4.metric("Opp. Count", df_opps2.shape[0])


def process_dates(cfg, df_opps):
    """

    :param cfg:
    :param df_opps:
    :return:
    """
    min_date = pd.to_datetime(cfg.first_record(df_opps))
    max_date = pd.to_datetime(cfg.last_record(df_opps))
    min_date_str = min_date.strftime('%Y-%m-%d')
    max_date_str = max_date.strftime('%Y-%m-%d')
    min_dt_date = datetime.strptime(min_date_str, '%Y-%m-%d')
    max_dt_date = datetime.strptime(max_date_str, '%Y-%m-%d')

    return max_dt_date, min_dt_date


def create_opp_pivot(df_opps):
    """
    Creates a pivot of the opportunity data to display as a time-based heatmap.
    :param df_opps: The main opportunity dataset.
    :return: A pivoted dataframe.
    """
    # Create a pivot for opportunities and rename columns as months.
    df_opps_pivot = df_opps.pivot_table(columns=df_opps['Created'].dt.month,
                                        index=df_opps['Created'].dt.year, aggfunc='count', values='rec_count')
    cols = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_opps_pivot = df_opps_pivot.rename(columns=cols)

    # Change the value for the bulk loaded data in April 2019.
    average = sum(df_opps_pivot.mean(axis=1))
    non_blank_cells = int(df_opps_pivot.shape[1] - df_opps_pivot.iloc[0].isnull().sum())
    df_opps_pivot.iat[0, 3] = math.floor(average / non_blank_cells)

    return df_opps_pivot


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """
    cfg = ih.OppConfig()  # Get configuration details from the info_helper
    df_opps = ih.read_data(cfg.excel_file, cfg.index_column, cfg.excel_sheet)

    my = create_opp_pivot(df_opps)
    st.markdown("## Opportunity data between the specified dates")

    max_dt_date, min_dt_date = process_dates(cfg, df_opps)

    slider = st.slider('Select date range', min_value=min_dt_date,
                       value=(min_dt_date, max_dt_date),
                       max_value=max_dt_date)

    delta = slider[1] - slider[0]
    start = slider[0].strftime('%a %d %b %Y')
    end = slider[1].strftime('%a %d %b %Y')

    start_date = slider[0].strftime('%Y-%m-%d')
    end_date = slider[1].strftime('%Y-%m-%d')

    df_opps2 = df_opps[
        (df_opps.index >= start_date) &
        (df_opps.index <= end_date)
        ]

    render_summary(delta, df_opps2, end, start)

    # Select all opportunities

    st.dataframe(df_opps2)

    st.markdown("## Headline statistics")
    st.markdown('There are {} opportunities between {} and {}'.format(df_opps2.shape[0], start_date, end_date))
    summary = ih.build_summary(df_opps2)
    st.dataframe(summary)

    st.markdown('## Opportunity status')
    st.markdown('')

    line = alt.Chart(df_opps2).mark_bar().encode(
        x='Status',
        y='count()',
    ).properties(width=400, height=200).interactive()

    bar = alt.Chart(df_opps2).mark_bar().encode(
        alt.X('Status'),
        alt.Y('count()'),
        alt.Color('Type',
                  scale=alt.Scale(scheme='tableau10')),
    ).properties(width=400, height=200).interactive()

    obj = alt.hconcat(line, bar)  # Vertical Concatenation

    st.altair_chart(obj)

    p = alt.Chart(df_opps2).mark_line().encode(
        alt.X('month(EstCloseDate):T', title='Estimated close date'),
        alt.Y('mean(BlendedRate(Base)):Q', title='Mean blended rate'),
        alt.Color('year(EstCloseDate):T',
                  scale=alt.Scale(scheme='set1')
                  )
    ).properties(width=900, height=300, title='Blended rate over time').interactive()

    st.altair_chart(p)

    sns.set(font_scale=0.75)
    f, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))
    sns.heatmap(my, annot=True, linewidths=.5, ax=axes[0])
    sns.heatmap(my, annot=True, linewidths=.5, ax=axes[1])
    st.pyplot(f)





