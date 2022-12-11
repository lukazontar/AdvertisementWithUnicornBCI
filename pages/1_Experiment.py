import csv
import datetime

import streamlit as st
import uuid

from lib.experiment.enum.ExperimentalStepEnum import ExperimentalStepEnum
from lib.experiment.singleton.RecorderSingleton import RecorderSingleton
from lib.experiment.util import *


def st_start_experiment():
    st.write("""
    # Instructions

    Please, carefully read the following instructions. This experiment is designed to test correlations between EEG signals and political advertisements. During the experiment you will be shown political ads from the [Slovenian parliamentarian elections 2022](https://www.dvk-rs.si/volitve-in-referendumi/drzavni-zbor-rs/volitve-drzavnega-zbora-rs/volitve-v-dz-2022/).

    Please, fill the questionnaire below and start the experiment. The questionnaire is completely anonymous.

    The experiment consists of 4 steps:
    1. You will be shown a text unrelated to the following steps. Please, read the entire text.
        - Click 'Next'. 
    2. You will be shown an ad. Please, read the caption and if you are shown a video, click in the iframe to start playing.
        - Click 'Next'.
    3. You will be shown a different text, once again unrelated to any other step. Please, read the entire text.
        - Click 'Next'.
    4. You will see the final ad. As asked in step 2, please, read the caption and if you are shown a video, click in the iframe to start playing.
        - Click 'Next'.
    Finally, click 'End experiment' to finish the experiment.
    """)

    with st.form("experiment_form"):
        st.selectbox(label='In which age group do you belong?',
                     options=['19 years of age or younger', '20 - 23 years of age', '23 - 26 years of age',
                              '27 years of age or more', 'I prefer not to answer'],
                     key='age')
        st.selectbox(label='Gender:',
                     options=['Male', 'Female', 'Other', 'I prefer not to answer'],
                     key='gender')

        st.selectbox(
            label='If elections were held today and you were asked to only pick between parliamentarian parties, which of the parties would you vote for?',
            options=['GIBANJE SVOBODA',
                     'SLOVENSKA DEMOKRATSKA STRANKA - SDS',
                     'NOVA SLOVENIJA - KRŠČANSKI DEMOKRATI',
                     'SOCIALNI DEMOKRATI - SD',
                     'LEVICA', 'I prefer not to answer'],
            key='preferred_party')

        st.form_submit_button("Start experiment")
        st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.SHOW_TEXT_1


def st_show_ad_1():
    ad_id = show_random_ad()
    st.button(label='Next', key='btn-3')
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.SHOW_TEXT_2
    return ad_id


def st_show_ad_2():
    ad_id = show_adapted_ad(st.session_state.EXPERIMENTAL_MODE)
    st.button(label='Next', key='btn-5')
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.END_EXPERIMENT
    return ad_id


def st_show_text_1():
    if "PREFERRED_PARTY" not in st.session_state:
        st.session_state.PREFERRED_PARTY = st.session_state['preferred_party']
    if "AGE" not in st.session_state:
        st.session_state.AGE = st.session_state['age']
    if "GENDER" not in st.session_state:
        st.session_state.GENDER = st.session_state['gender']

    # A single ID that will be bound to:
    # - Screen recording file
    # - EEG recording file
    # - Questionnaire data
    # - App event data (used for visualization)
    if "EXPERIMENT_ID" not in st.session_state:
        st.session_state.EXPERIMENT_ID = uuid.uuid4()

    RecorderSingleton().set_experiment_id(experiment_id=st.session_state.EXPERIMENT_ID)
    RecorderSingleton().set_experimental_mode(experimental_mode=st.session_state.EXPERIMENTAL_MODE)
    RecorderSingleton().start_recording()

    st.markdown("""
    ## My Wonderful Family 
    
    I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best food!

    My family is very important to me. We do lots of things together. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much.
    """)
    st.button(label='Next', key='btn-2')
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.SHOW_AD_1


def st_show_text_2():
    st.write("""
    ## Likable
    
    She could see she was becoming a thoroughly unlikable person. Each time she opened her mouth she said something ugly, and whoever was nearby liked her a little less. These could be strangers, these could be people she loved, or people she knew only slightly whom she had hoped would one day be her friends. Even if she didn't say anything, even if all she did is seem a certain way, have a look on her face, or make a soft sound of reaction, it was always unlikable—except in the few cases that she fixed herself on being likable for the next four seconds (more than that was impossible) and sometimes that worked, but not always.
    
    Why couldn't she be more likable? What was the problem? Did she just not enjoy the world anymore? Had the world gotten away from her? Had the world gotten worse? (Maybe, probably not. Or probably in some ways but not in the ways that were making her not like it). Did she not like herself? (Well, of course she didn't, but there was nothing new in that.)
    
    Or had she become less likable simply by growing older—so that she might be doing the same thing she always did, but because she was now forty-one, not twenty, it had become unlikable because any woman doing something at forty-one is more unlikable than a woman doing it at twenty? And does she sense this? Does she know she is intrinsically less likable and instead of resisting, does she lean into it, as into a cold wind? Maybe (likely) she used to resist, but now she sees the futility, so each morning when she opens her mouth she is unlikable, proudly so, and each evening before sleep she is unlikable, and each day it goes on this way, she getting more unlikable by the hour, until one morning she will be so unlikable, inconveniently unlikable, that she will have to be shoved into a hole and left there.
    """)
    st.button(label='Next', key='btn-4')
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.SHOW_AD_2


def st_reset_experiment():
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.START_EXPERIMENT


def st_end_experiment():
    RecorderSingleton().end_recording()
    st.write('Thank you for participating in this experiments! All results can be viewed on Results tab.')
    st.button(label='End experiment')
    st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.START_EXPERIMENT


def st_main():
    st.sidebar.radio(
        label="Experimental mode:",
        options=('Train', 'Test'),
        key='EXPERIMENTAL_MODE',
        on_change=st_reset_experiment)

    if st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.START_EXPERIMENT:
        st_start_experiment()

    elif st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.SHOW_TEXT_1:
        st_show_text_1()
        if "TEXT_1_SHOWN_TS" not in st.session_state:
            st.session_state.TEXT_1_SHOWN_TS = datetime.datetime.now()

    elif st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.SHOW_AD_1:
        ad_id = st_show_ad_1()
        if "AD_1_SHOWN_TS" not in st.session_state:
            st.session_state.AD_1_SHOWN_TS = datetime.datetime.now()
        if "AD_1_ID" not in st.session_state:
            st.session_state.AD_1_ID = ad_id

    elif st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.SHOW_TEXT_2:
        st_show_text_2()
        if "TEXT_2_SHOWN_TS" not in st.session_state:
            st.session_state.TEXT_2_SHOWN_TS = datetime.datetime.now()

    elif st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.SHOW_AD_2:
        ad_id = st_show_ad_2()
        if "AD_2_SHOWN_TS" not in st.session_state:
            st.session_state.AD_2_SHOWN_TS = datetime.datetime.now()
        if "AD_2_ID" not in st.session_state:
            st.session_state.AD_2_ID = ad_id

    elif st.session_state.EXPERIMENTAL_STEP == ExperimentalStepEnum.END_EXPERIMENT:
        st_end_experiment()
        if "EXPERIMENT_ENDED" not in st.session_state:
            st.session_state.EXPERIMENT_ENDED = datetime.datetime.now()

    else:
        st_reset_experiment()

    if "EXPERIMENT_ENDED" in st.session_state and not st.session_state.EXPERIMENT_LOGGED:
        data = {
            'experiment_id': st.session_state.EXPERIMENT_ID,
            'text_1_shown_ts': st.session_state.TEXT_1_SHOWN_TS,
            'ad_1_shown_ts': st.session_state.AD_1_SHOWN_TS,
            'text_2_shown_ts': st.session_state.TEXT_2_SHOWN_TS,
            'ad_2_shown_ts': st.session_state.AD_2_SHOWN_TS,
            'experiment_ended': st.session_state.EXPERIMENT_ENDED,
            'ad_1_id': st.session_state.AD_1_ID,
            'ad_2_id': st.session_state.AD_2_ID,
            'preferred_party': st.session_state.PREFERRED_PARTY,
            'gender': st.session_state.GENDER,
            'age': st.session_state.AGE
        }
        # Log experiment events from sessions state
        with open(f'data/{st.session_state.EXPERIMENTAL_MODE}/experiments.csv', 'a') as filedata:
            writer = csv.DictWriter(filedata, delimiter=',', fieldnames=data.keys())
            writer.writerow(data)
        st.session_state.EXPERIMENT_LOGGED = True


if __name__ == '__main__':
    if "EXPERIMENT_LOGGED" not in st.session_state:
        st.session_state.EXPERIMENT_LOGGED = False
    if "EXPERIMENTAL_STEP" not in st.session_state:
        st.session_state.EXPERIMENTAL_STEP = ExperimentalStepEnum.START_EXPERIMENT
    st_main()
