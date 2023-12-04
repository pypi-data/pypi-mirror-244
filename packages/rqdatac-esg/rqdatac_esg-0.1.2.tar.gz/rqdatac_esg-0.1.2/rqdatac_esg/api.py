import pandas as pd
from rqdatac.validators import (
    ensure_date_range,
    check_items_in_container,
    ensure_order_book_ids,
    ensure_list_of_string,
)
from rqdatac.client import get_client
from rqdatac.decorators import export_as_api
from rqdatac_esg.utils import ensure_list

LEVELS = [0,1,2]
TYPES = ['E','S','G']

LEVEL_1_MAP = {
    'E': 'environmental',
    'S': 'social',
    'G': 'governance'
}
LEVEL_2_MAP = {
    'E': [
        'environment_management', 'resources_efficiency', 'environment_discharge', 'climate_change'
    ],
    'S': [
        'human_capital', 'health_and_safety', 'product_liability', 'business_innovation', 'social_capital'
    ],
    'G': [
        'governance_structure', 'shareholders', 'compliance', 'audit', 'transparency'
    ]
}

FIELD_TO_LEVEL_MAP = {
    'esg_overall': 0,
    ** { v: 1 for v in LEVEL_1_MAP.values()},
    ** { item: 2 for v in LEVEL_2_MAP.values() for item in v }
}
FIELD_TO_TYPE_MAP = {
    'esg_overall': '',
    ** {
        item: k
        for k,v in LEVEL_2_MAP.items()
        for item in v + [LEVEL_1_MAP[k]]
    }
}


@export_as_api(namespace='esg')
def get_rating(order_book_ids, start_date=None, end_date=None, level=None, type=None):
    ''' 获取 ESG 评价数据
    :param order_book_ids: str or str list, 沪深 A 股股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期，开始日期和结束日期都不传则默认返回所有时段数据
    :param level: int or int list, ESG评价级别，共三级。0为ESG综合评价，1为一级维度，2为二级维度，默认返回所有级别分类
    :param type: str or str list, ESG评价类别，E 表示环境，S表示社会责任，G表示治理。默认返回所有类别。
    
    :returns
        返回 DataFrame, Index (order_book_id, rating_date, name)
    '''
    order_book_ids = ensure_order_book_ids(order_book_ids, type='CS', market='cn')
    if start_date is not None or end_date is not None:
        start_date, end_date = ensure_date_range(start_date, end_date)
    if level is None:
        level = LEVELS
    else:
        level = ensure_list(level, int, 'level')
        check_items_in_container(level, LEVELS, 'level')
    if type is None:
        type = TYPES
    else:
        type = ensure_list_of_string(type, 'type')
        check_items_in_container(type, TYPES, 'type')

    fields = []
    if 0 in level:
        fields.append('esg_overall')
    if 1 in level:
        fields.extend([LEVEL_1_MAP[t] for t in type])
    if 2 in level:
        for t in type:
            fields.extend(LEVEL_2_MAP[t])
    df = get_client().execute("esg.get_rating", order_book_ids, start_date, end_date, fields)
    if not df:
        return
    
    df = pd.DataFrame(df)
    df.set_index(['order_book_id', 'rating_date'], inplace=True)
    df.columns = pd.MultiIndex.from_tuples(f.rsplit('_', 1) for f in df.columns)
    df = df.stack(level=0)
    df.index.set_names('name', level=2, inplace=True)
    df.sort_index(inplace=True)
    df['level'] = df.index.get_level_values(2).map(FIELD_TO_LEVEL_MAP)
    df['type'] = df.index.get_level_values(2).map(FIELD_TO_TYPE_MAP)

    return df
