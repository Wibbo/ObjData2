import streamlit as st
import altair as alt
import Helpers.info_helper as ih


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """

    cfg = ih.OppConfig()  # Get configuration details from the info_helper
    df_opps = ih.read_data(cfg.excel_file, cfg.index_column)
    df_opps.columns = df_opps.columns.str.replace(' ', '')
    df_opps.columns = df_opps.columns.str.replace('.', '')

    st.markdown("## Opportunity data between the specified dates")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date of first opportunity", cfg.start_time)
        start_date = start_date.strftime('%Y-%m-%d')
    with col2:
        end_date = st.date_input("Date of last opportunity", cfg.end_time)
        end_date = end_date.strftime('%Y-%m-%d')

    # df_opps2 = df_opps.loc[start_date:end_date]
    df_opps2 = df_opps[
        (df_opps.index >= start_date) &
        (df_opps.index <= end_date)
       ]

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
    ).properties(width=400, height=400).interactive()

    bar = alt.Chart(df_opps2).mark_bar().encode(
            alt.X('Status'),
            alt.Y('count()'),
            alt.Color('Type'),
        ).properties(width=400, height=400).interactive()

    obj = alt.hconcat(line, bar)  # Vertical Concatenation

    st.altair_chart(obj)

    p = alt.Chart(df_opps2).mark_bar().encode(
        alt.X('month(EstCloseDate):T'),
        alt.Y('mean(BlendedRate(Base)):Q'),
    ).properties(width=400, height=400).interactive()

    st.altair_chart(p)

   # timer = alt.Chart(df_opps2.reset_index()).mark_line().encode(
   #     x='index:T',
   #     y='value:Q'
   # ).properties(width=400, height=400).interactive()

 #   st.altair_chart(timer)

