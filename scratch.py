import requests
import pandas as pd
import send_me_email
import web


def get_caixin():
    """Get five most recent business and tech stories from Caixin Global"""
    url = 'https://gateway.caixin.com/api/data/getNewsListByPids?page=1&size=5&pids=101267062'
    res = requests.get(url)
    df = pd.DataFrame(res.json()['data']['list'])
    df = df[['desc','url']]

    return df

test = get_caixin()

import ipdb; ipdb.set_trace()
