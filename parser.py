import pandas
from bs4 import BeautifulSoup

import requests


def get_news_urls():
    r = requests.get('https://www.rbc.ru/short_news')

    soup = BeautifulSoup(r.text, "lxml")
    news_soap_list = soup.findAll('div', class_='js-news-feed-item')

    news_urls = []
    categories = []
    allowed_categories = [
        'politics',
        'economics',
        'business',
        'technology',
        'technology_and_media',
        'society',
        'base',
        'rbcfreenews',
        'sport'
    ]

    for news in news_soap_list:
        item = news.find('a', class_='item__link')
        item_link = item.get('href')
        category = item_link.split('/')[3]
        if category not in categories and category in allowed_categories:
            categories.append(category)
            news_urls.append(item_link)
    return news_urls


def get_list_news(news_urls):
    news_list = []
    for news in news_urls:
        r = requests.get(news)
        soup = BeautifulSoup(r.text, "lxml")
        category = soup.find('a', class_='article__header__category').text.strip()
        title = soup.find('h1', class_='article__header__title-in').text.strip()
        description = soup.find('div', class_='article__text__overview')
        if description is not None:
            description = description.find('span').text.strip()
        link = news.replace('?from=short_news', '')
        news_list.append({'category': category, 'title': title, 'link': link, 'description': description})
    return news_list


def start_parse():
    news_urls = get_news_urls()
    news_list = get_list_news(news_urls)

    df = pandas.DataFrame(news_list)
    df.to_csv('news.csv', index=False, encoding='utf-8')
