import streamlit as st

from PIL import Image
from util.experiment.singleton.AllAdsDataSingleton import AllAdsDataSingleton


def show_random_ad():
    ad_id = AllAdsDataSingleton().random_ad()
    show_ad(ad_id=ad_id)
    return ad_id


def show_ad(ad_id: str):
    ad_row = AllAdsDataSingleton().ad_by_id(ad_id=ad_id)
    st.write(ad_row['ad_creative_bodies'])
    if ad_row['media_type'] == 'jpg':
        image = Image.open(f'data/media/ {ad_id}.jpg')
        st.image(image=image)
    elif ad_row['media_type'] == 'mp4':
        st.video(data=open(f'data/media/ {ad_id}.mp4', 'rb', ).read())
    else:
        raise RuntimeError('Invalid media type.')


def show_adapted_ad(mode: str):
    if mode == 'Train':
        ad_id = AllAdsDataSingleton().random_ad()
        show_ad(ad_id=ad_id)
    elif mode == 'Test':
        raise NotImplementedError
    else:
        raise RuntimeError("Invalid experimental mode.")
    return ad_id
