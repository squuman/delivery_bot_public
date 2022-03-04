import retailcrm
import config

client = retailcrm.v5(config.retail_url, config.retail_key)

order = client.order(2099, 'id', 'test').get_response()['order']

payments = order['payments']

paid = False

for id in payments:
    if 'status' in payments[id]:
        if payments[id]['status'] == 'paid':
            paid = True

print(paid)
