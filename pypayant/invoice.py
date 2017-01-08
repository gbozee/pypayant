from .base import BasePayantAPI


class Invoice(BasePayantAPI):

    def __init__(self, auth_key, **kwargs):
        super(Invoice, self).__init__(auth_key, **kwargs)
        self.key = "invoices"

    def add(self, new=False, **kwargs):
        """

        Create a new invoice
        :param client_id: Client ID
        :param due_date:  Invoice due date
        :param fee_bearer: Invoice fee bearer account or client
        :param items: Invoice items
        :param new: False by default but True if the client is new
        :param client: Client Data
        :return:
        """
        if new:
            kwargs.pop('client_id', None)
        else:
            kwargs.pop('client', None)
        return super(Invoice, self).add(**kwargs)
        
    def send(self, reference_code):
        """
        Send an invoice
        :param reference_code:
        :return:
        """
        _send_base = "send"
        url = self._path("{0}/{1}/{2}".format(self.key,
                                              _send_base, reference_code))
        return self._exec_request('GET', url)

    def history(self, period, start, end):
        """
        Return invoice history from start to end within specified period
        :param period:
        :param start:
        :param end:
        :return:
        """
        _history_base = "history"
        url = self._path("{0}/{1}/".format(self.key,
                                           _history_base))
        request_data = {"period": period, "start": start, "end": end}
        return self._exec_request('GET', url, request_data)

    