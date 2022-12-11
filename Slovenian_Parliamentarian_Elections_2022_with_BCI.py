import pandas as pd
import streamlit as st

from util.experiment.enum.ExperimentalStepEnum import ExperimentalStepEnum


def st_main():
    st.write("# Political advertisements analysis with BCI")
    st.write("## Slovenian parliamentarian elections 2022 advertisement results")
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.START_EXPERIMENT

    df_election_results = pd.read_csv('data/Slovenian Parliamentarian Elections Data 2022 - Political Parties.csv')
    st.bar_chart(data=df_election_results, x='political_party_abbreviation', y='percentage_votes')


if __name__ == '__main__':
    st_main()
