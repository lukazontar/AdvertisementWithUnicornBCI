import datetime
import pandas as pd

from lib.ad_scraper.FBAdLibraryPartyPageScraper import FBAdLibraryPartyPageScraper


def parliamentarian_election_data(data: pd.DataFrame):
    data['ad_delivery_start_time'] = pd.to_datetime(data['ad_delivery_start_time'])
    data['ad_delivery_end_time'] = pd.to_datetime(data['ad_delivery_start_time'])

    start_date = datetime.datetime(2022, 3, 1)
    end_date = datetime.datetime(2022, 4, 30)
    mask_start_date = (data['ad_delivery_start_time'] > start_date) & \
                      (data['ad_delivery_start_time'] <= end_date)
    mask_end_date = (data['ad_delivery_end_time'] > start_date) & \
                    (data['ad_delivery_end_time'] <= end_date)
    return data.loc[mask_start_date | mask_end_date]


def collect_media_political_party(political_party_abbreviation: str):
    df_party_metadata = pd.read_csv(f'data/metadata/{political_party_abbreviation}.csv')
    if len(set(df_party_metadata['page_id'])) > 1:
        raise RuntimeError("More than 1 page for a political party.")

    df_party_metadata_filtered = parliamentarian_election_data(data=df_party_metadata)

    scraper = FBAdLibraryPartyPageScraper(page_id=list(df_party_metadata['page_id'])[0],
                                          valid_ids=list(df_party_metadata_filtered['ad_archive_id']))
    scraper.scroll_to_bottom()
    scraper.collect_media()
    scraper.close()

collect_media_political_party(
    political_party_abbreviation='GS'
)