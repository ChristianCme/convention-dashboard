import pandas as pd
import streamlit as st
import sys 
sys.path.insert(0, "./../" )
from data_utils import get_overall_vote_results, get_chapter_vote_results


st.set_page_config(
    page_title="Votes By Chapter",
)

st.write("# Votes by Chapter")

# inital code from https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_votes_url"])

vote_choice = st.selectbox("Choose a Vote", df['vote_name'].unique(), index=0)

vote_results = get_overall_vote_results(df)

vote_results_by_chapter = get_chapter_vote_results(df)



st.markdown(
    """
    This page I think could compare 2 or 3 chapters side by side to compare stats and certain votes. 

    Ideas for charts/stats (not in this order):
    - Breakdowns for how the chapter swung for each vote as well as the difference between them and convention vote total
    - An average deviation between the chapter votes and the convention results
    - A count of how many ballots fit into each caucus (see Shane's 2021 analysis)
    """
)