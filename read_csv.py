import pandas as pd
from json import dumps, loads


def get_news_json():
    data_frame = pd.read_csv('news.csv')
    news_pd_json = data_frame.to_json(orient='records')
    news_json = dumps(loads(news_pd_json), indent=2, ensure_ascii=False)
    return news_json
