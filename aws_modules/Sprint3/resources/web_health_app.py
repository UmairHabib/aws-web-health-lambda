import urllib3
import datetime
from constants import URLS_TO_MONITOR, URL_MONItOR_NAMESPACE, URL_MONITOR_METRIC_NAME_LATENCY, URL_MONITOR_METRIC_NAME_AVAILABILITY
from cloudwatch_putmetric import CloudWatchPutMetric

def lambda_handler(event, context):

    cloud_watch =  CloudWatchPutMetric()
    arr = []
    for url in URLS_TO_MONITOR:
        dimension = [{'Name': 'url', "Value": url}]
        
        web_availability = get_availability(url)
        cloud_watch.put_data(URL_MONItOR_NAMESPACE, URL_MONITOR_METRIC_NAME_AVAILABILITY, dimension, web_availability)
        
        web_latency = get_latency(url)
        cloud_watch.put_data(URL_MONItOR_NAMESPACE, URL_MONITOR_METRIC_NAME_LATENCY, dimension, web_latency)
        arr.append({"url":url, "web_availability": web_availability, "web_latency": web_latency})

    return arr

# 200 =  OK
# 301 = Moved Permanently
# 400 = Bad Request
# 404 = Not Found
# 505 = Http version not supported

def get_availability(url):
    """
    gets web page from url and returns status of website using status code

    Args:
        url: web domain for checking availability
    """
    http = urllib3.PoolManager()  # using pool manager to get web page
    response = http.request("GET", url)

    if response.status == 200:
        return 1
    else:
        return 0



def get_latency(url):
    """
    gets web page from url and waits for web page to compute time of response

    Args:
        url: web domain for checking availability
    """
    http = urllib3.PoolManager()  # using pool manager to get web page
    start_time = datetime.datetime.now()
    response = http.request("GET", url)
    end_time = datetime.datetime.now()

    difference = end_time - start_time
    latency_sec = round(difference.microseconds * .000001, 6)
    return latency_sec



