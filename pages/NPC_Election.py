import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="NPC Election",
)

#DATA HANDLING

# inital code from https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

first_ballot = df.groupby('choice_1').count().reset_index()
first_ballot = first_ballot.rename(columns={"choice_1":"Candidate", 'Voter':'Votes'})
first_ballot = first_ballot[['Candidate', 'Votes']]

final_ballot = df.groupby('choice_41').count().reset_index()
final_ballot = final_ballot.rename(columns={"choice_41":"Candidate", 'Voter':'Votes'})
final_ballot = final_ballot[['Candidate', 'Votes']]

#Gets candidate ranked last on each ballot
last_ballot = df.dropna(subset=['choice_1'])
last_ballot = last_ballot.replace('', np.nan).fillna(axis=1, method='ffill')
last_ballot = last_ballot.groupby('choice_41').count().reset_index()
last_ballot = last_ballot.rename(columns={"choice_41":"Candidate", 'Voter':'Votes'})
last_ballot = last_ballot[['Candidate', 'Votes']]

#VISUAL ELEMENTS

st.write("# NPC Election 2023")
st.warning('Ballot weights are not considered yet', icon="⚠️")
st.write("## Candidates Ranked #1")
st.bar_chart(first_ballot, x="Candidate", y="Votes")

with st.expander("Raw First Ballot Counts"):
    st.dataframe(first_ballot)


st.write("## Candidates Ranked Last")
st.bar_chart(last_ballot, x="Candidate", y="Votes")

with st.expander("Raw Last Ballot Counts"):
    st.dataframe(last_ballot)

st.write("## Candidates Ranked #41")
st.write("Only ballots that ranked all candidates are counted for this chart")
st.bar_chart(final_ballot, x="Candidate", y="Votes")

with st.expander("Raw Ranked #41 Ballot Counts"):
    st.dataframe(final_ballot)


st.write("## Raw Ballots")
with st.expander("Raw Data"):
    st.dataframe(df)

st.markdown(
    """
    This is actually the most difficult page to do. I'd like to do an animation showing how votes flowed, or maybe an interactive Sankey? Definitely seeking input.
    """
)