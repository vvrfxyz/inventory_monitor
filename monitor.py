import datetime
import requests
import logging
from bs4 import BeautifulSoup
from jsonpath_ng import jsonpath, parse

class Monitor:
    def __init__(self):
        self.session = requests.Session()
        self.response_format = ""

    def _send_request(self, config):
        try:
            method = config.method.upper()
            if method == "GET":
                response = self.session.get(config.url, headers=config.get('headers',{}),  params=config.get('params', {}))
            elif method == "POST":
                response = self.session.post(config.url, headers=config.get('headers',{}), json=config.data)
            else:
                raise ValueError("Unsupported method")

            response.raise_for_status()
            self.response_format = _determine_response_format(response)

            if self.response_format == 'html':
                return response.text
            elif self.response_format == 'json':
                return response.json()
            else:
                logging.warning(f"Unknown format type for URL {config.url}")
                return response.text
        except requests.RequestException as e:
            logging.error(f"Error during request : {e}")
            return None

    def _extract_stock_from_response(self, response, stock_expression):
        if self.response_format == 'json':
            jsonpath_expr = parse(stock_expression)
            match = jsonpath_expr.find(response)
            if match:
                return match[0].value
        elif self.response_format  == 'html':
            soup = BeautifulSoup(response, 'lxml')
            element = soup.select_one(stock_expression)
            if element:
                return element.text.strip()  # or any other attribute
        return None

    def monitor_stock(self, config):
        response = self._send_request(config)
        if response:
            stock = self._extract_stock_from_response(response, config.stock_expression)
            return stock

def _determine_response_format(response):
    content_type = response.headers.get('Content-Type')

    if 'application/json' in content_type:
        return 'json'
    elif 'text/html' in content_type:
        return 'html'
    else:
        return 'unknown'
def send_notification(bark, key, title, content):
    try:
        bark.notify(key=key, title=title, content=content)
        logging.info(f"Sent notification with title: {title}")
    except Exception as e:
        logging.error(f"Error sending notification with title {title}: {e}")

def is_within_time_range(start_str, end_str):
    start = datetime.datetime.strptime(start_str, "%H:%M").time()
    end = datetime.datetime.strptime(end_str, "%H:%M").time()
    current_time = datetime.datetime.now().time()
    return start <= current_time <= end
