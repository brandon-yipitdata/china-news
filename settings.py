## -*- coding: utf-8 -*-
LIST_TICKERS = ['BABA', 'JD', 'PDD', 'YY', 'HUYA', 'MOMO', 'BILI', 'IQ', 'EDU','TAL','VIPS','ZTP','BSTI']
LIST_ORGANIZATIONS = [('Alibaba', 'BABA'), ('JD', 'JD'),('Pinduoduo', 'PDD'),('YY', 'YY'),('HUYA','HUYA'),('MOMO', 'MOMO'), ('Bilibili', 'BILI'), ('iQiyi', 'IQ'), ('New Oriental', 'EDU'),('TAL EDUCATION','TAL'), ('VIP Shop', 'VIPS'), ('ZTO Express', 'ZTO'),('Best Inc', 'BSTI')]
LIST_ORGANIZATIONS_CHINESE = [('阿里巴巴', 'BABA'), ('京东', 'JD'),('拼多多', 'PDD'),('YY', 'YY'),('虎牙','HUYA'),('陌陌', 'MOMO'), ('哔哩哔哩', 'BILI'), ('爱奇艺', 'IQ'), ('新东方', 'EDU'),('好未来','TAL'), ('唯品会', 'VIPS'), ('中通快递', 'ZTO'),('百世集团', 'BSTI')]


QUERY_INSERT = '''INSERT INTO sandbox.china_news (run_id, uuid, date_story, source, title, url) VALUES (%(run_id)s,%(uuid)s,%(date_story)s,%(source)s,%(title)s,%(url)s)'''
QUERY_GET_NEWS_URLS = '''SELECT DISTINCT url FROM sandbox.china_news'''
QUERY_GET_THE_NEWS = '''
    SELECT
    	source,
    	title,
    	url
    FROM sandbox.china_news
    WHERE run_id IN (SELECT MAX(run_id) FROM sandbox.china_news)
    ORDER BY source, title
'''


QUERY_NEWSAPI_INSERT = '''INSERT INTO sandbox.china_news_newsapi (run_id, uuid, ticker, date_story, source, title, url, description) VALUES (%(run_id)s,%(uuid)s,%(ticker)s,%(date_story)s,%(source)s,%(title)s,%(url)s, %(description)s)'''
QUERY_NEWSAPI_GET_URLS = '''SELECT DISTINCT url FROM sandbox.china_news_newsapi'''

QUERY_WEBHOSE_GET_URLS = '''SELECT DISTINCT url FROM sandbox.china_news_webhose'''
QUERY_WEBHOSE_INSERT = '''INSERT INTO sandbox.china_news_webhose (run_id, uuid, ticker, date_story, source, title, url, description) VALUES (%(run_id)s,%(uuid)s,%(ticker)s,%(date_story)s,%(source)s,%(title)s,%(url)s, %(description)s)'''

QUERY_TONGHUASHUN_INSERT = '''INSERT INTO sandbox.china_news_tonghuashun (run_id, uuid, ticker, date_story, source, title, url) VALUES (%(run_id)s,%(uuid)s,%(ticker)s,%(date_story)s,%(source)s,%(title)s,%(url)s)'''
QUERY_TONGHUASHUN_GET_URLS = '''SELECT DISTINCT url FROM sandbox.china_news_tonghuashun'''


GET_NEWS_QUERY = '''
    SELECT
    	source,
    	title,
    	url
    FROM sandbox.china_news
    WHERE run_id IN (SELECT MAX(run_id) FROM sandbox.china_news)
    ORDER BY source, title
'''

QUERY_SUMMARIZE_API_RESULTS = '''
SELECT
	'WebHose' AS service,
	COUNT(*) AS new_stories
FROM sandbox.china_news_webhose
WHERE run_id IN (SELECT MAX(run_id) FROM sandbox.china_news_webhose)
UNION
SELECT
	'NewsApi' AS service,
	COUNT(*) AS new_stories
FROM sandbox.china_news_newsapi
WHERE run_id IN (SELECT MAX(run_id) FROM sandbox.china_news_newsapi)
'''
