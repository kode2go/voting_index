import streamlit as st
from streamlit_lottie import st_lottie
import json
import os
import pandas as pd
import plotly.express as px

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

# def style_dataframe(df):
#     # Apply CSS to each column with different colors
#     styled_df = df.style.map(lambda x: 'background-color: lightgreen', subset=pd.IndexSlice[:, 'ANC'])
#     styled_df = styled_df.map(lambda x: 'background-color: lightblue', subset=pd.IndexSlice[:, 'DA'])
#     styled_df = styled_df.map(lambda x: 'background-color: lightcoral', subset=pd.IndexSlice[:, 'EFF'])
#     styled_df = styled_df.map(lambda x: 'background-color: lightgrey', subset=pd.IndexSlice[:, 'Rise'])
#     styled_df = styled_df.format(precision=2)
#     return styled_df

# Custom colors for each column
colors = {
    'ANC': 'lightgreen',
    'DA': 'lightblue',
    'EFF': 'lightcoral',
    'Rise': 'lightgrey'
}

def base():
    #Header
    st.title('Islamicity Index')

    st.divider()

    # Create a sample DataFrame with the specified columns and index
    data = {
        'ANC': [0, 0, 0, 0, 0, 0, 0],
        'DA': [0, 0, 0, 0, 0, 0, 0],
        'EFF': [0, 0, 0, 0, 0, 0, 0],
        'Rise': [0, 0, 0, 0, 0, 0, 0],
        'AJ': [0, 0, 0, 0, 0, 0, 0]
    }
    index = ["Justice (/10)", "Conservation of Religion (/5)", 
    "Conservation of Life (/5)", 
    "Conservation of Religion (/5)", 
    "Conservation of Sound Intellect (/5)",
    "Conservation of Lineage (/5)", 
    "Conservation of Wealth (/5)"]
    df = pd.DataFrame(data, index=index)
    all_totals = pd.DataFrame()
    current_totals = pd.Series()

    # Display the data editor
    st.title('Index Input')
    edited_df = st.data_editor(df,width=2000)

    # Input for the submitter's name
    submitter_name = st.text_input("Enter your name")

    # Button to calculate the totals for each column
    if st.button('Calculate Totals'):
        totals = edited_df.sum().to_frame(name='Total').T
        if totals.drop(columns=['Submitter'], errors='ignore').values.sum() > 0 and submitter_name:
            totals['Submitter'] = submitter_name  # Add the submitter's name
            current_totals = totals
            if not os.path.exists('totals.csv'):
                totals.to_csv('totals.csv', index=False)
            else:
                totals.to_csv('totals.csv', mode='a', header=False, index=False)

            df_totals = pd.read_csv('totals.csv')
            # avg = df_totals.mean().to_frame(name='Avg').T
            avg = df_totals.iloc[:, :-1].mean().to_frame(name='Avg').T

            avg = avg.round(2)

            # Convert the average DataFrame to a format suitable for Plotly
            avg_melted = avg.melt(var_name='Party', value_name='Avg')



            st.write('Totals:')
            # st.dataframe(style_dataframe(totals),width=2000)
            st.dataframe(totals,width=2000)

            st.write('All Totals:')
            # st.dataframe(style_dataframe(df_totals),width=2000)
            st.dataframe(df_totals,width=2000)

            st.write('Average:')
            # st.dataframe(style_dataframe(avg),width=2000)
            st.dataframe(avg,width=2000)

            # Plot the average values
            # st.bar_chart(avg.T)

            # print(avg.T)

            fig = px.bar(avg_melted, x='Party', y='Avg', color='Party', 
             color_discrete_map=colors, 
             title='Average by Party')

            # Update layout to match the style
            fig.update_layout(showlegend=False)

            # Display the bar chart in Streamlit
            st.plotly_chart(fig)
        else:
            st.write("Cannot have 0 values for all, must enter name")

# if st.button('Submit'):




# To run this app, save it to a file (e.g., app.py) and run it using:
# streamlit run app.py
