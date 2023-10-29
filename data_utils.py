import pandas as pd

def get_overall_vote_results(df):
	vote_results = df.groupby('vote_name')['vote'].value_counts().unstack(fill_value=0)
	vote_results['Yes_Percentage'] = (vote_results['Yes'] / (vote_results['Yes'] + vote_results['No'])) * 100
	vote_results['No_Percentage'] = (vote_results['No'] / (vote_results['Yes'] + vote_results['No'])) * 100
	vote_results['Abstain_Percentage'] = (vote_results['Abstain'] / (vote_results['Yes'] + vote_results['No'])) * 100
	return vote_results
	
def get_chapter_vote_results(df):
	vote_results_by_chapter = df.groupby(['vote_name', 'dsa_chapter', 'vote'])['vote'].count().unstack(fill_value=0)
	vote_results_by_chapter.reset_index(inplace=True)
	vote_results_by_chapter['Yes_Percentage'] = (vote_results_by_chapter['Yes'] / (vote_results_by_chapter['Yes'] + vote_results_by_chapter['No'])) * 100
	vote_results_by_chapter['No_Percentage'] = (vote_results_by_chapter['No'] / (vote_results_by_chapter['Yes'] + vote_results_by_chapter['No'])) * 100

	# Calculate the overall "Yes" percentage for each vote name
	overall_yes_percentage = df.groupby('vote_name')['vote'].apply(lambda x: (x == 'Yes').sum() / x.count() * 100).reset_index()
	overall_yes_percentage = overall_yes_percentage.rename(columns={'vote': 'Overall_Yes_Percentage'})

	# Merge the overall_yes_percentage with the vote_results_by_chapter DataFrame
	vote_results_by_chapter = pd.merge(vote_results_by_chapter, overall_yes_percentage, on='vote_name', how='left')

	# Calculate the difference between chapter's "Yes" percentage and overall "Yes" percentage
	vote_results_by_chapter['Yes_Percentage_Difference'] = vote_results_by_chapter['Yes_Percentage'] - vote_results_by_chapter['Overall_Yes_Percentage']
	return vote_results_by_chapter