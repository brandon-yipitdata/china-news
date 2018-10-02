from newsapi import NewsApiClient
import private
import psycopg2
import settings
import time
import web
import webhoseio


conn = psycopg2.connect(private.DB_CONNECTION_STRING)
run_id = int(time.time())

newsapi = NewsApiClient(api_key = private.API_KEY_NEWSAPI)
webhoseio.config(token=private.API_KEY_WEBHOSE)


# Tonghuashun ------------------------------------------------------------------

list_of_urls_tonghuashun = web.get_urls(conn, private.QUERY_TONGHUASHUN_GET_URLS)

list_of_tickers = settings.LIST_TICKERS

for ticker in list_of_tickers:
    try:
        web.get_tonghuashun(ticker, conn, run_id, list_of_urls_tonghuashun)
    except Exception as e:
        print ticker + e

# NewsAPI ----------------------------------------------------------------------

list_of_urls_newsapi = web.get_urls(conn, settings.QUERY_NEWSAPI_GET_URLS)

[web.get_newsapi(ticker, conn, run_id, newsapi, list_of_urls_newsapi) for ticker in settings.LIST_TICKERS]


# WebHose ----------------------------------------------------------------------

list_of_urls_webhose = web.get_urls(conn, settings.QUERY_WEBHOSE_GET_URLS)
list_of_tickers = settings.LIST_TICKERS

for org, ticker in settings.LIST_ORGANIZATIONS:
    print org
    print ticker
    web.get_webhose(conn, run_id, webhoseio, list_of_urls_webhose, org, ticker)

# Email Send -------------------------------------------------------------------
report = web.get_API_results(conn)

subject = "API Results Email"
recipient = private.EMAIL_RECIPIENTS
email_body = u'The Results:\n\n\n{}\n\n\nLove,\nYour China Email Bot'.format(report)

web.send_html_email(email_body, recipient, subject)

conn.close()
