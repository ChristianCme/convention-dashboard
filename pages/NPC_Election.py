import altair as alt
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
df = df.dropna(subset=['choice_1'])
df = df.drop(df[df['choice_1'].str.contains("Vote")].index)
df = df.reset_index(drop=True)

weighted_df = df.loc[df.index.repeat(df['Weight'])]

first_ballot = weighted_df.groupby('choice_1').count().reset_index()
first_ballot = first_ballot.rename(columns={"choice_1":"Candidate", 'Voter':'Votes'})
first_ballot = first_ballot[['Candidate', 'Votes']]

final_ballot = weighted_df.groupby('choice_41').count().reset_index()
final_ballot = final_ballot.rename(columns={"choice_41":"Candidate", 'Voter':'Votes'})
final_ballot = final_ballot[['Candidate', 'Votes']]

#Gets candidate ranked last on each ballot
last_ballot = weighted_df.replace('', np.nan).fillna(axis=1, method='ffill')
last_ballot = last_ballot.groupby('choice_41').count().reset_index()
last_ballot = last_ballot.rename(columns={"choice_41":"Candidate", 'Voter':'Votes'})
last_ballot = last_ballot[['Candidate', 'Votes']]

num_ranked = weighted_df.iloc[:, -41:].isnull().sum(axis=1).apply(lambda x: 41 - x).mean()


def gen_col_list(x):
    col_list = []
    for num in range(x):
        col_list.append('choice_' + str(num + 1))
    return col_list

def most_pop_x_ordered(x):
    return weighted_df.groupby(gen_col_list(x)).size().reset_index().rename(columns={0:'count'}).sort_values(['count'], axis=0, ascending=False)

def most_pop_x_unordered(x):
    unordered_pop_x = weighted_df.copy()
    unordered_pop_x = unordered_pop_x[unordered_pop_x[gen_col_list(x)[-1]].notna()]
    unordered_pop_x[gen_col_list(x)] = np.sort(unordered_pop_x[gen_col_list(x)], axis=1)
    return unordered_pop_x.groupby(gen_col_list(x)).size().reset_index().rename(columns={0:'count'}).sort_values(['count'], axis=0, ascending=False)


#VISUAL ELEMENTS
st.write("# NPC Election 2023")
st.warning('The 7 ballots anonymously counted due to techical errors are not represented. Empty ballots are discarded.', icon="⚠️")
met1, met2, met3 = st.columns(3)
met1.metric('Number of Unweighted Ballots Cast', df.shape[0])
met2.metric('Number of Weighed Ballots Cast', weighted_df.shape[0])
met3.metric('Average Number of Candidates Ranked (Weighted)', round(num_ranked, 2))
st.info('All further charts and data reflect weighted ballots.', icon="ℹ️")
st.write("## Candidates Ranked #1")
st.bar_chart(first_ballot, x="Candidate", y="Votes")

with st.expander("Raw First Ballot Counts"):
    st.dataframe(first_ballot.sort_values(['Votes'], axis=0, ascending=False), hide_index=True)


st.write("## Candidates Ranked Last")
st.bar_chart(last_ballot, x="Candidate", y="Votes")

with st.expander("Raw Last Ballot Counts"):
    st.dataframe(last_ballot.sort_values(['Votes'], axis=0, ascending=False), hide_index=True)

st.write("## Candidates Ranked #41")
st.write("Only ballots that ranked all candidates are counted for this chart")
st.bar_chart(final_ballot, x="Candidate", y="Votes")

with st.expander("Raw Ranked #41 Ballot Counts"):
    st.dataframe(final_ballot.sort_values(['Votes'], axis=0, ascending=False))


st.write("## Most Popular Combos")
control1, control2, control3 = st.columns(3)
groupsize = control1.slider("Combo Size", 1, 41, 3)
cutoff = control2.number_input("Cutoff", 1, 1000, 40)
ordered = control3.checkbox("Ordered?")

if ordered:
    st.write("Most Popular Combo Ordered")
    data = most_pop_x_ordered(groupsize)
    order_text = " Ordered"
else:
    st.write("Most Popular Combo Unordered")
    data = most_pop_x_unordered(groupsize)
    order_text = " Unordered"

chart_data = data.copy()
chart_data['combo'] = chart_data.iloc[:, :-1].astype(str).agg('|'.join,axis=1)
chart_data = chart_data[chart_data['count'] > cutoff]


c = alt.Chart(chart_data).encode(
    y=alt.Y('combo').title(None),
    #y='Top X' + order_text,
    x=alt.X('count').axis(None),
    text='count'
)
st.altair_chart((c.mark_bar() + c.mark_text(align='left', dx=5, color='white')).configure_axis(labelLimit=1000), use_container_width=True)
st.dataframe(data, hide_index=True)



st.write("## Raw Ballots")
with st.expander("Raw Data"):
    st.dataframe(df)

st.markdown(
    """
    This is actually the most difficult page to do. I'd like to do an animation showing how votes flowed, or maybe an interactive Sankey? Definitely seeking input.
    """
)