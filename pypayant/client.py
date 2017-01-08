from __future__ import print_function  # (at top of module)
from .base import BasePayantAPI


class Client(BasePayantAPI):
    def __init__(self, auth_key, **kwargs):
        super(Client, self).__init__(auth_key, **kwargs)
        self.key = "clients"

    def add(self,
            first_name,
            last_name,
            email,
            phone,
            website=None,
            address=None,
            state=None,
            lga=None,
            company_name=None):
        """

        Creates a new payant client
        :param website:
        :param first_name:
        :param last_name:
        :param email:
        :param phone:
        :param address:
        :param state:
        :param lga:
        :param company_Name:
        :return:
        """
        request_data = {
            "company_name": company_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "website": website,
            "address": address,
            "state": state,
            "lga": lga
        }
        return super(Client, self).add(**request_data)

    def edit(self,
             client_id,
             first_name,
             last_name,
             email,
             phone,
             website=None,
             address=None,
             state=None,
             lga=None,
             company_Name=None):
        """
        Update a Payant client with the client_id provided
        :param client_id:
        :param first_name:
        :param last_name:
        :param email:
        :param phone:
        :param website:
        :param address:
        :param state:
        :param lga:
        :param company_Name:
        :return:
        """
        url = self._path("{0}/{1}".format(self.key, client_id))
        request_data = {
            "company_name": company_Name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "website": website,
            "address": address,
            "state": state,
            "lga": lga
        }
        return self._exec_request('PUT', url, request_data)
