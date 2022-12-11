import os
import random
from datetime import datetime

import pandas as pd
from numpy import int64

from util.experiment.singleton.EEGRecorderThread import EEGRecorderThread
from util.experiment.singleton.ScreenRecorderThread import ScreenRecorderThread


class AllAdsDataSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AllAdsDataSingleton(metaclass=AllAdsDataSingletonMeta):
    def __init__(self):
        data_metadata = pd.DataFrame()
        for csv_filename in os.listdir(path='data/metadata'):
            data_metadata = pd.concat(objs=[
                data_metadata,
                pd.read_csv(filepath_or_buffer=f"data/metadata/{csv_filename}",
                            dtype=str)
            ])
        media_ids = []
        for media_filename in os.listdir(path='data/media'):
            media_ids.append({
                'ad_archive_id': str.strip(media_filename.split('.')[0]),
                'media_type': media_filename.split('.')[1]
            })
        data_media = pd.DataFrame(media_ids)
        set(data_metadata['page_name'])
        self.data = data_metadata.merge(right=data_media,
                                        on='ad_archive_id',
                                        how='inner')
        self.data.index = self.data['ad_archive_id']

    def random_ad(self):
        return random.choice(seq=self.data['ad_archive_id'])

    def ad_by_id(self, ad_id: str):
        return self.data.loc[ad_id]
