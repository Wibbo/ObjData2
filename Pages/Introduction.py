import streamlit as st


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """
    st.markdown("## Introduction")

    # Upload the dataset and save as csv
    st.markdown("""This application presents a number of technology 
                   and data demonstrations. Please select a page
                   from the Site navigation dropdown in the sidebar
                   on the left hand side of the screen.
                """)

    st.markdown('## See also')
    st.markdown('[The Objectivity web site](https://www.objectivity.co.uk)')
    st.markdown('[The need for a data strategy infographic](https://tinyurl.com/ydob6etr)')
    st.markdown('[The need for a data strategy white paper](https://tinyurl.com/yhggsyht)')
    st.markdown('[Data in retail on Teams](https://tinyurl.com/yjvqu7xb)')