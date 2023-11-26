import pandas as pd
import streamlit as st
import sys 
sys.path.insert(0, "./../" )
from data_utils import get_overall_vote_results, get_chapter_vote_results

st.set_page_config(
    page_title="Votes By Resolution",
)

#Turn metric arrows off
st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.write("# Votes by Resolution")

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


if vote_choice:
    col1, col2, col3 = st.columns(3)
    yes_perc = float(vote_results['Yes_Percentage'].loc[vote_choice])
    no_perc = float(vote_results['No_Percentage'].loc[vote_choice])
    abstain_perc = float(vote_results['Abstain_Percentage'].loc[vote_choice])
    col1.metric("% Vote Yes", "{:.2f}%".format(yes_perc), delta=vote_results['Yes'].loc[vote_choice].item(), delta_color="off", help=None, label_visibility="visible")
    col2.metric("% Vote No", "{:.2f}%".format(no_perc), delta=vote_results['No'].loc[vote_choice].item(), delta_color="off", help=None, label_visibility="visible")
    col3.metric("% Abstain", "{:.2f}%".format(abstain_perc), delta=vote_results['Abstain'].loc[vote_choice].item(), delta_color="off", help=None, label_visibility="visible")


