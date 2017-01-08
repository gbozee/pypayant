from pypayant.base import BasePayantAPI


class Payment(BasePayantAPI):
    def __init__(self, auth_key):
        super(Payment, self).__init__(auth_key)
        self.key = "payments"

    def add(self, reference_code, date, amount, channel):
        """
        :param reference_code:
        :param date:
        :param amount:
        :param channel:
        :return:
        """
        request_data = {
            "reference_code": reference_code,
            "date": date,
            "amount": amount,
            "channel": channel
        }
        return super(Payment, self).add(**request_data)
