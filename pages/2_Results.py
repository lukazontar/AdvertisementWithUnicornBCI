import streamlit as st

from util.experiment.enum.ExperimentalStepEnum import ExperimentalStepEnum

st.write("# Results")
st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.START_EXPERIMENT

