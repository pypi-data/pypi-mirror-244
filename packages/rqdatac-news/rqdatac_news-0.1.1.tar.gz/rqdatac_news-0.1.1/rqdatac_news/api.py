import pandas as pd
from dateutil.relativedelta import relativedelta
from rqdatac.validators import (
    ensure_date_range,
    check_items_in_container,
    ensure_order_book_ids,
    ensure_list_of_string
)
from rqdatac.client import get_client
from rqdatac.decorators import export_as_api


STOCK_NEWS_FIELDS = [
    'news_id',
    'title',
    'original_time',
    'url',
    'source',
    'news_emotion_indicator',
    'news_neutral_weight',
    'news_positive_weight',
    'news_negative_weight',
    'company_relevance',
    'company_emotion_indicator',
    'company_neutral_weight',
    'company_positive_weight',
    'company_negative_weight'
]


def get_emotion_detail(emotion_details):
    ''' 根据数据库的 emotiondetail 序列生成中性，正向，负向权重序列
    params:
        emotion_details: list, 从数据库中获取的 emotiondetail 序列
    return:
        (
            neutral_weight: list(float),
            positive_weight: list(float),
            negative_weight: list(float)
        )
    '''
    if not emotion_details:
        return []
    results = []
    # 原格式：{0=*, 1=*, 2=*}，0：中性，1：正向，2：负向
    for detail in emotion_details:
        detail = detail[1:-1].split(',')
        detail = [float(item.split('=')[1]) for item in detail]
        results.append(detail)
    return (list(x) for x in zip(*results))


@export_as_api(namespace='news')
def get_stock_news(order_book_ids, start_date=None, end_date=None, fields=None):
    ''' 获取个股新闻情绪指标
    :param order_book_ids: str or str list, 沪深 A 股股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期，开始日期和结束日期都不传则返回最近一个月的数据
    :param fields: str or str list, 可选参数，默认为所有字段

    :returns
        返回 DataFrame, Index (order_book_id, datetime)
    '''
    order_book_ids = ensure_order_book_ids(order_book_ids, type='CS', market='cn')
    start_date, end_date = ensure_date_range(start_date, end_date, delta=relativedelta(months=1))
    if fields is None:
        fields = STOCK_NEWS_FIELDS
    else:
        fields = ensure_list_of_string(fields, 'fields')
        check_items_in_container(fields, STOCK_NEWS_FIELDS, 'fields')

    df = get_client().execute("news.get_stock_news", order_book_ids, start_date, end_date, fields)
    if not df:
        return
    
    df = pd.DataFrame(df)
    # 原指标 0：中性，1：正向，2：负向，转换为 -1：负向，0：中性，1：正向
    if 'news_emotion_indicator' in fields:
        df['news_emotion_indicator'] = df['news_emotion_indicator'].map({1: 1, 0: 0, 2: -1})
    if 'company_emotion_indicator' in fields:
        df['company_emotion_indicator'] = df['company_emotion_indicator'].map({1: 1, 0: 0, 2: -1})
    if 'news_emotion_detail' in df.columns:
        df['news_neutral_weight'], df['news_positive_weight'], df['news_negative_weight'] = get_emotion_detail(df['news_emotion_detail'].to_list())
    if 'company_emotion_detail' in df.columns:
        df['company_neutral_weight'], df['company_positive_weight'], df['company_negative_weight'] = get_emotion_detail(df['company_emotion_detail'].to_list())
    df.set_index(['order_book_id', 'datetime'], inplace=True)
    df.sort_index(inplace=True)
    df = df[fields]

    return df