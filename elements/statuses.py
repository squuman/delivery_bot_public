import retailcrm
import config


class Statuses:
    SEND_TO_ASSEMBLING = 'send-to-assembling'
    SEND_TO_DELIVERY = 'send-to-delivery'
    FOR_SHIPMENT = 'for-shipment'
    READY_TO_PICKUP = 'fa86f52f50'
    COMPLETE = 'complete'

    PAID = 'paid'

    client = retailcrm.v5(config.retail_url, config.retail_key)

    @staticmethod
    def get_statuses():
        return Statuses.client.statuses().get_response()['statuses']
