import json
import subprocess
import webbrowser
import urllib.parse
import urllib.request

from wox import Wox
from wox import WoxAPI

# -*- coding: utf-8 -*-
# 固定写法，导入相关类库和函数
from util import WoxEx, WoxAPI, load_module, Log

# 统一加载模块
with load_module():
    import pyperclip

URL = {
    'USD CNY': ('convert USD', 'https://google.com'),
    'EUR CNY': ('convert Euro', 'https://github.com'),
    'C Y': ('convert RMB', 'https://reddit.com'),
}

currencies = ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'KRW', 'RUB', 'GBP', 'SGD', 'TWD', 'CAD', 'AUD', 'BRL', 'INR', 'CHF', 'THB', 'MOP', 'NZD', 'ZAR', 'SEK', 'IDR', 'MXN', 'ARS', 'MYR', 'OMR', 'EGP', 'PKR', 'PYG', 'BHD', 'PAB', 'BMD', 'BGN', 'ISK', 'PLN', 'BOB', 'BWP', 'DKK', 'PHP', 'COP', 'CUP', 'KZT', 'ANG', 'GHC', 'CZK', 'ZWL', 'QAR', 'KWD', 'HRK', 'KES', 'LVL', 'LAK', 'LBP', 'LTL', 'RON', 'MUR', 'MNT', 'BDT', 'PEN', 'BUK', 'MAD', 'NOK', 'SAR', 'LKR', 'SOS', 'TZS', 'TND', 'TRY', 'GTQ', 'UYU', 'HUF', 'JMD', 'ILS', 'JOD', 'VND', 'CLP', 'PGK', 'KPW', 'LSL', 'LYD', 'RWF', 'MMK', 'MRO', 'MWK', 'NIO', 'NPR', 'SBD', 'SCR', 'BND', 'SYP', 'DZD', 'AED', 'BBD', 'AFN', 'ALL', 'AMD', 'AOA', 'AWG', 'AZN', 'BAM', 'BIF', 'BSD', 'BTN', 'BYR', 'BYN', 'BZD', 'CDF', 'CRC', 'CUC', 'CVE', 'DJF', 'DOP', 'NGN', 'ERN', 'ETB', 'FJD', 'FKP', 'GEL', 'GIP', 'GMD', 'GNF', 'GYD', 'HNL', 'HTG', 'IQD', 'IRR', 'KGS', 'KHR', 'KMF', 'KYD', 'LRD', 'MDL', 'MGA', 'MKD', 'MVR', 'MZN', 'NAD', 'RSD', 'SDG', 'SHP', 'SLL', 'SRD', 'STD', 'SZL', 'TJS', 'TMT', 'TOP', 'TTD', 'UAH', 'UGX', 'UZS', 'VEF', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZMW', 'SVC', 'GHS', 'MRU']

URLBASE = 'https://api.jisuapi.com/exchange/convert'
URLCURRENCY = 'https://api.jisuapi.com/exchange/currency'
# params = dict(appkey='', from='USD', to='CNY', amount=100)
params = {}
params["appkey"] = "78c400c9b1ad0155"
params["from"] = "USD"
params["to"] = "CNY"
params["amount"] = 100

cu_params = {}
cu_params["appkey"] = "78c400c9b1ad0155"


class HelloWorld(WoxEx):
    """Example python plugin.
    Plugins must implement two method:
    - query(self, arg)
    - context_menu(self, arg)
    They must return a list of results.
    Other functions should not have return value.
    """
    def query(self, arg):
        """Function that is invoked when plugin is selected.
        The user can pass a query string, arg, that this function can use as input.
        This can be used to filter results or pass as input to the actions from results.
        
        In this example, the query will search for substring in title and subtitle.
        """
        def result(title, subtitle, url):
            return {
                'Title': title,
                'SubTitle': 'Subtitle: {}'.format(subtitle),
                'IcoPath': 'Images/app.png',
                'ContextData': title,  # Data that is passed to context_menu function call
                'JsonRPCAction': {
                    'method': 'open_webpage',  # Maps to function name that should be called if this action is selected.
                    'parameters': [url, False],  # N number of params that will be passed to function call
                }
            }

        search_term = arg.lower()

        usrdata = search_term.split()

        if len(usrdata) in (0,1,2):
            data = urllib.parse.urlencode(cu_params)
            url = URLCURRENCY + "?" + data
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                jsonarr = json.loads(the_page)
                if jsonarr["status"] != 0:
                    return [result('API calling error',str(jsonarr["status"]),'')]
                else:
                    tranmount =  jsonarr["result"]
                    return[result(val["currency"], val["name"], '') for val in tranmount]
        
        if len(usrdata) == 3:
            if usrdata[0].upper() in currencies:
                params["from"] = usrdata[0].upper()
            if usrdata[1].upper() in currencies:
                params["to"] = usrdata[1].upper()
            if usrdata[2].isnumeric():
                params["amount"] = int(usrdata[2])
            
            data = urllib.parse.urlencode(params)
            url = URLBASE + "?" + data
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                jsonarr = json.loads(the_page)
                if jsonarr["status"] != 0:
                    tranmount =  "error"
                else:
                    tranmount = "{:.2f}".format(jsonarr["result"]["camount"])
            #pyperclip.copy(str(tranmount))

            #return [result(str(tranmount),'','')]
            return [result('Currency', str(params["amount"]) + " " + params["from"] + " = " + str(tranmount) + " " + params["to"], '')]


        def search_criteria(key, value):
            key = key.lower()
            description = value[0].lower()

            return search_term in key or search_term in description
        #return [result(usrdata[0], *value) for key, value in URL.items() if search_criteria(key, value)]
        #return [result(usrdata[0], *value) for key, value in URL.items() if search_criteria(key, value)]
        #finalresults = []
        #for key, value in URL.items:
         #   if search_criteria(key, value):
          #      finalresults.insert(result(key, *value))
        #return finalresults

    def context_menu(self, ctx_data):
        """Function that is called when context menu is triggered (shift-enter).
        ctx_data is the value set in from ContextData from query.
        
        Note: The user's query in context menu is only for searching through the title of the following results.
        """
        site_title = ctx_data
        results = [
            {
                "Title": "Open up {} in a new window".format(site_title),
                'JsonRPCAction': {
                    'method': 'open_webpage',
                    'parameters': [URL[site_title][1]],
                },
            },
            {
                "Title": "Show notification",
                'JsonRPCAction': {
                    'method': 'show_notification',
                    'parameters': [site_title, 'some addiitional text'],
                },
            },
            {
                "Title": "Kick off whatever process you want",
                'JsonRPCAction': {
                    'method': 'run_process',
                    'parameters': [],
                },
            },
        ]
        return results

    def open_webpage(self, url, notification=True):
        """Trivial implementation of bookmarks in Wox
        Demonstrates how optional parameters in Json RPC are handled.
        """
        if notification:
            WoxAPI.show_msg('Heads up', 'We opened in new window')
            webbrowser.open_new(url)
        else:
            webbrowser.open(url)

    def show_notification(self, site, extra_message):
        """Custom handler that demonstrates how to call Wox api"""
        title = 'You chose {}'.format(site)
        sub_title = 'This the extra message you sent: {}'.format(extra_message)
        ico_path = ''

        # Wrappers for many common APIs are found in JsonRPC/wox.py
        # WoxAPI.show_msg(title, sub_title)

        # But you can invoke any arbitrary function in Wox dlls with JSON RPC
        print(json.dumps(
            {
                "method": "Wox.ShowMsg",
                "parameters": [ title, sub_title, ico_path ]
            },
        ))

    def run_process(self):
        """Custom handler to trigger any process to run."""
        subprocess.call(['/bin/true'])


if __name__ == "__main__":
    HelloWorld()