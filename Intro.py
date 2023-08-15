import streamlit as st

st.set_page_config(
    page_title="Intro",
)

st.write("# Unofficial DSA Vote Breakdown Dashboard")

st.markdown(
    """
    This is placeholder text writing what this dashboard does and explaining the context of DSA Convention.

    When you visit each page, right now its a list of ideas for each page and its operation.

    On this page, I think some high level charts like number of delegates seated vs actually attended and other stats that aren't votes specifically would fit well.

    Some big ideas that could  drive analysis on other pages:
    - A some sort of clustering algorithm (Kmeans?) and potentially also other heuristics to show how many groups should have been. Maybe a visualization? 
    """
)

with st.expander("Technical TODOs"):
    st.markdown(
        """
        - Initial data cleaning and formatting, if there's transformations we can do once and save somewhere, that's ideal. Streamlit isn't super performant.
        - Set up session state to load in data https://docs.streamlit.io/library/api-reference/session-state
        - Data can be easily loaded in from remote sources. https://docs.streamlit.io/knowledge-base/tutorials/databases
        """
        )