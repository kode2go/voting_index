import streamlit as st
import pandas as pd
import altair as alt

# Party names and criteria
parties = ['ANC', 'DA', 'EFF', 'Rise', 'AJ']
criteria = ["Justice (/10)", "Conservation of Religion (/5)", 
            "Conservation of Life (/5)", "Conservation of Sound Intellect (/5)"]

# Initialize session state to store submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

# Create a Streamlit form
st.title("Party Ranking Form")
with st.form(key='ranking_form'):
    name = st.text_input("Enter your name")

    # Create input boxes for ratings
    cols = st.columns(len(parties))
    scores = {}
    for idx, party in enumerate(parties):
        with cols[idx]:
            st.subheader(f"{party}")
            scores[party] = {}
            for criterion in criteria:
                # max_score = int(criterion.split('/')[1].strip(')'))
                scores[party][criterion] = st.number_input(
                    f"{criterion}", 
                    min_value=0, max_value=10, key=f"{party}_{criterion}"
                )
    
    submit_button = st.form_submit_button(label='Submit')

# Process the form submission
if submit_button:
    total_scores = {party: sum(scores[party].values()) for party in parties}
    submission = {'name': name, **total_scores}
    st.session_state.submissions.append(submission)
    
    st.subheader("Total Scores for Each Party")
    
    # Display metrics for each party in one row
    cols = st.columns(len(parties))
    for idx, party in enumerate(parties):
        cols[idx].metric(label=party, value=total_scores[party])
    
st.subheader("All Submissions")
if st.session_state.submissions:
    df = pd.DataFrame(st.session_state.submissions)
    st.dataframe(df,width=2000)
    
    # Calculate averages
    averages = df.mean(numeric_only=True).to_frame().T
    averages['name'] = 'Averages'
    averages = averages.set_index('name')
    
    # Display average scores
    st.subheader("Average Scores")
    st.dataframe(averages,width=2000)
    
    # Bar plot of the total scores
    st.subheader("Total Scores Bar Plot")
    df_melted = df.melt(id_vars=["name"], var_name="Party", value_name="Score")
    bar_chart = alt.Chart(df_melted).mark_bar().encode(
        x='Party:O',
        y='Score:Q',
        color='Party:N',
        tooltip=['name', 'Score']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(bar_chart, use_container_width=True)
