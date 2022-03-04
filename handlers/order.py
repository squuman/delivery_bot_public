import json

import requests
import retailcrm

import config
from config import *

client = retailcrm.v5(retail_url, retail_key)


async def get_orders(order_number):
     for site in config.sites:
        order = client.order(order_number, 'id', site)
        response = order.get_response()
        if response['success'] is True:
            return response['order']
        else:
            return False


