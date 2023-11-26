import pandas as pd
import streamlit as st
import sys 
sys.path.insert(0, "./../" )
from data_utils import get_overall_vote_results, get_chapter_vote_results
from kmodes.kmodes import KModes

st.set_page_config(
    page_title="Voter Clusters",
)

# inital code from https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_votes_url"])

pivoted = df[['name', 'dsa_chapter', 'vote', 'vote_name']].pivot(index=['name', 'dsa_chapter'], columns='vote_name', values='vote').fillna('abstain')


untrained_model=KModes(n_clusters=3)
pivoted['cluster'] = untrained_model.fit_predict(pivoted)

st.write(pivoted[pivoted.cluster == 1])

# #Elbow chart
# costs=[]
# K=range(2, 10)
# for k in K:
#     el_untrained_model=KModes(n_clusters=k)
#     el_trained_model=el_untrained_model.fit(pivoted)
#     costs.append(el_trained_model.cost_)
# elbow = pd.DataFrame(zip(K,costs), columns=['K', 'costs'])
# st.line_chart(elbow, x='K', y='costs', width=0, height=0, use_container_width=True)
