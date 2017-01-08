from pypayant.base import BasePayantAPI


class Product(BasePayantAPI):
    def __init__(self, auth_key):
        super(Product, self).__init__(auth_key)
        self.key = "products"

    def add(self, name, description, unit_cost, type):
        """

        :param type:
        :param unit_cost:
        :param description:
        :param name:
        :return:
        """
        request_data = {
            "name": name,
            "description": description,
            "unit_cost": unit_cost,
            "type": type
        }
        return super(Product, self).add(**request_data)

    def get_one(self, product_id):
        """
        Get the details of a product with the id provided.
        :return:
        """
        return super(Product, self).get(product_id)

    def get_multiple(self):
        """
                Get the details of all products.
                :return:
                """
        url = self._path("{0}".format(self.key))
        return self._exec_request('GET', url)

    def edit(self, product_id, **kwargs):
        """
        Update a Payant client with the client_id provided
        :param product_id:
        :return:
        """
        url = self._path("{0}/{1}".format(self.key, product_id))
        request_data = {
            "name": kwargs.get('name'),
            "description": kwargs.get('description'),
            "unit_cost": kwargs.get('unit_cost'),
            "type": kwargs.get('type')
        }
        return self._exec_request('PUT', url, request_data)
